import uuid
from typing import Tuple, List, Dict, Any
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.file import File, FileStatus
from app.models.scan import ScanResult, ScanStatus, ThreatLevel
from app.scanners.validator import calculate_sha256, detect_magic_signature
from app.scanners.dangerous_file import check_dangerous_file
from app.scanners.clamav import clamav_scanner
from app.security.encryption import file_encryptor
from app.storage import storage
from app.audit.logger import log_security_event


def run_security_pipeline(
    db: Session,
    user_id: int,
    user_email: str,
    original_filename: str,
    declared_mime: str,
    raw_data: bytes,
    client_ip: str = "127.0.0.1",
    user_agent: str = "SecureShare-Web"
) -> File:
    """
    Executes the comprehensive 6-stage security pipeline on an uploaded file:
    1. Size & SHA-256 Hash Validation
    2. MIME & Magic Byte Signature Verification
    3. Dangerous Executable & Script Inspection
    4. ClamAV Malware Scan (including EICAR detection)
    5. Security Decision (CLEAN vs QUARANTINE)
    6. AES-256-GCM Encryption at Rest & Storage Isolation
    """
    file_size = len(raw_data)
    stored_uuid = str(uuid.uuid4())
    stored_filename = f"{stored_uuid}_{original_filename}"

    # Stage 1: File Size Check
    if file_size > settings.MAX_FILE_SIZE_BYTES:
        raise ValueError(f"File size ({file_size} bytes) exceeds maximum limit of {settings.MAX_FILE_SIZE_BYTES} bytes.")

    sha256_hash = calculate_sha256(raw_data)

    # Stage 2: MIME & Magic Byte Signature Check
    detected_mime, magic_preview, mime_valid, mime_reason = detect_magic_signature(
        raw_data, declared_mime, original_filename
    )

    # Create initial File record in database
    file_record = File(
        user_id=user_id,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_size=file_size,
        declared_mime=declared_mime,
        detected_mime=detected_mime,
        magic_bytes_preview=magic_preview,
        sha256_hash=sha256_hash,
        status=FileStatus.SCANNING,
        storage_path="pending",
        is_quarantined=False,
        encryption_iv="0" * 24,
    )
    db.add(file_record)
    db.commit()
    db.refresh(file_record)

    # Record Stage 2 Scan Result
    mime_scan = ScanResult(
        file_id=file_record.id,
        scanner_name="mime_signature_validator",
        scan_status=ScanStatus.PASSED if mime_valid else ScanStatus.FAILED,
        threat_level=ThreatLevel.CLEAN if mime_valid else ThreatLevel.HIGH,
        threat_name="MIME_SPOOFING_MISMATCH" if not mime_valid else None,
        details=mime_reason or f"Signature verified. Magic bytes: {magic_preview}"
    )
    db.add(mime_scan)

    # Stage 3: Dangerous Executable & Script Detection
    is_dangerous, danger_cat, danger_details = check_dangerous_file(raw_data, original_filename)
    danger_scan = ScanResult(
        file_id=file_record.id,
        scanner_name="dangerous_file_detector",
        scan_status=ScanStatus.HIGH_RISK if is_dangerous else ScanStatus.PASSED,
        threat_level=ThreatLevel.HIGH if is_dangerous else ThreatLevel.CLEAN,
        threat_name=danger_cat if is_dangerous else None,
        details=danger_details or "No prohibited executables, scripts, or embedded macros found."
    )
    db.add(danger_scan)

    # Stage 4: ClamAV Malware Scan (including EICAR test file)
    clamav_clean, clamav_threat, clamav_msg = clamav_scanner.scan_bytes(raw_data)
    clamav_scan = ScanResult(
        file_id=file_record.id,
        scanner_name="clamav_scanner",
        scan_status=ScanStatus.PASSED if clamav_clean else ScanStatus.MALICIOUS,
        threat_level=ThreatLevel.CLEAN if clamav_clean else ThreatLevel.CRITICAL,
        threat_name=clamav_threat,
        details=clamav_msg
    )
    db.add(clamav_scan)
    db.commit()

    # Stage 5: Security Decision
    is_quarantined = False
    quarantine_reasons = []

    if not clamav_clean:
        is_quarantined = True
        quarantine_reasons.append(f"Malware detected: {clamav_threat} ({clamav_msg})")
        file_record.status = FileStatus.MALICIOUS

    elif is_dangerous:
        is_quarantined = True
        quarantine_reasons.append(f"Dangerous file detected: {danger_details}")
        file_record.status = FileStatus.HIGH_RISK

    elif not mime_valid:
        is_quarantined = True
        quarantine_reasons.append(f"File validation failed: {mime_reason}")
        file_record.status = FileStatus.HIGH_RISK

    else:
        file_record.status = FileStatus.CLEAN

    # Stage 6: AES-256-GCM Encryption at Rest & Storage
    nonce_hex, ciphertext = file_encryptor.encrypt(raw_data)
    file_record.encryption_iv = nonce_hex
    file_record.is_quarantined = is_quarantined
    file_record.quarantine_reason = " | ".join(quarantine_reasons) if quarantine_reasons else None

    # Save encrypted payload to appropriate storage partition
    storage_path = storage.save_file(
        filename=stored_filename,
        data=ciphertext,
        is_quarantined=is_quarantined
    )
    file_record.storage_path = storage_path
    if is_quarantined:
        file_record.status = FileStatus.QUARANTINED if file_record.status != FileStatus.MALICIOUS else FileStatus.MALICIOUS

    db.commit()
    db.refresh(file_record)

    # Audit Logging
    log_security_event(
        db=db,
        action="FILE_UPLOAD_SCAN",
        resource_type="file",
        resource_id=str(file_record.id),
        actor_id=user_id,
        actor_email=user_email,
        ip_address=client_ip,
        user_agent=user_agent,
        result="QUARANTINE" if is_quarantined else "SUCCESS",
        metadata={
            "filename": original_filename,
            "sha256": sha256_hash,
            "file_size": file_size,
            "status": file_record.status.value,
            "is_quarantined": is_quarantined,
            "quarantine_reason": file_record.quarantine_reason
        }
    )

    return file_record
