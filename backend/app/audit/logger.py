import hashlib
import json
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.audit import AuditLog

GENESIS_HASH = "0" * 64


def calculate_entry_hash(
    previous_hash: str,
    sequence_num: int,
    timestamp_iso: str,
    actor_email: Optional[str],
    action: str,
    resource_type: str,
    resource_id: Optional[str],
    result: str,
    metadata_json: Optional[str]
) -> str:
    """
    Cryptographic hash chain calculation:
    SHA-256(previous_hash || sequence_num || timestamp_iso || actor_email || action || resource_type || resource_id || result || metadata_json)
    """
    raw_payload = (
        f"{previous_hash}|"
        f"{sequence_num}|"
        f"{timestamp_iso}|"
        f"{actor_email or 'anonymous'}|"
        f"{action}|"
        f"{resource_type}|"
        f"{resource_id or ''}|"
        f"{result}|"
        f"{metadata_json or ''}"
    )
    return hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()


def log_security_event(
    db: Session,
    action: str,
    resource_type: str,
    result: str,
    actor_id: Optional[int] = None,
    actor_email: Optional[str] = None,
    resource_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> AuditLog:
    """
    Appends a new event to the tamper-evident audit chain.
    Atomically determines next sequence number and previous hash.
    """
    metadata_json = json.dumps(metadata, sort_keys=True) if metadata else None
    now = datetime.utcnow()
    timestamp_iso = now.isoformat()

    # Retrieve latest audit record for sequence & previous_hash
    last_record = db.query(AuditLog).order_by(AuditLog.sequence_num.desc()).first()
    if last_record:
        sequence_num = last_record.sequence_num + 1
        previous_hash = last_record.entry_hash
    else:
        sequence_num = 1
        previous_hash = GENESIS_HASH

    entry_hash = calculate_entry_hash(
        previous_hash=previous_hash,
        sequence_num=sequence_num,
        timestamp_iso=timestamp_iso,
        actor_email=actor_email,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        result=result,
        metadata_json=metadata_json
    )

    audit_entry = AuditLog(
        sequence_num=sequence_num,
        actor_id=actor_id,
        actor_email=actor_email,
        action=action,
        resource_type=resource_type,
        resource_id=str(resource_id) if resource_id is not None else None,
        ip_address=ip_address,
        user_agent=user_agent,
        result=result,
        metadata_json=metadata_json,
        timestamp=now,
        previous_hash=previous_hash,
        entry_hash=entry_hash,
    )

    db.add(audit_entry)
    db.commit()
    db.refresh(audit_entry)
    return audit_entry
