from typing import Dict, Any
from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from app.audit.logger import calculate_entry_hash, GENESIS_HASH


def verify_audit_log_integrity(db: Session) -> Dict[str, Any]:
    """
    Verifies the cryptographic integrity of the entire audit log hash chain.
    Returns whether the chain is intact, the count of verified records,
    and identifies any tampered record and sequence number if compromised.
    """
    logs = db.query(AuditLog).order_by(AuditLog.sequence_num.asc()).all()
    if not logs:
        return {
            "is_valid": True,
            "total_records": 0,
            "tampered_sequence_num": None,
            "expected_hash": None,
            "actual_hash": None,
            "message": "Audit chain is empty. Integrity verified."
        }

    expected_prev_hash = GENESIS_HASH

    for log in logs:
        # Check linkage to previous record
        if log.previous_hash != expected_prev_hash:
            return {
                "is_valid": False,
                "total_records": len(logs),
                "tampered_sequence_num": log.sequence_num,
                "expected_hash": expected_prev_hash,
                "actual_hash": log.previous_hash,
                "message": f"Broken chain link at sequence #{log.sequence_num}: previous_hash mismatch."
            }

        # Recalculate hash of current record
        recalculated_hash = calculate_entry_hash(
            previous_hash=log.previous_hash,
            sequence_num=log.sequence_num,
            timestamp_iso=log.timestamp.isoformat(),
            actor_email=log.actor_email,
            action=log.action,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            result=log.result,
            metadata_json=log.metadata_json
        )

        if recalculated_hash != log.entry_hash:
            return {
                "is_valid": False,
                "total_records": len(logs),
                "tampered_sequence_num": log.sequence_num,
                "expected_hash": recalculated_hash,
                "actual_hash": log.entry_hash,
                "message": f"Cryptographic integrity violation at sequence #{log.sequence_num}: record data has been altered!"
            }

        expected_prev_hash = log.entry_hash

    return {
        "is_valid": True,
        "total_records": len(logs),
        "tampered_sequence_num": None,
        "expected_hash": None,
        "actual_hash": None,
        "message": f"All {len(logs)} audit log records verified intact. Cryptographic hash chain is valid."
    }
