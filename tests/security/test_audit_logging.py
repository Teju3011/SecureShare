import pytest
from app.core.database import SessionLocal
from app.models.audit import AuditLog
from app.audit.verifier import verify_audit_log_integrity


def test_audit_logs_integrity_clean(client, admin_headers):
    # Retrieve audit verify endpoint
    res = client.get("/api/v1/admin/audit-logs/verify", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["is_valid"] is True


def test_audit_log_tamper_detection_in_chain():
    db = SessionLocal()
    # Check chain is valid
    res_initial = verify_audit_log_integrity(db)
    assert res_initial["is_valid"] is True

    # Tamper with an audit entry's action
    log = db.query(AuditLog).first()
    if log:
        original_action = log.action
        log.action = "TAMPERED_ACTION_ATTACK"
        db.commit()

        # Chain verification must fail
        tampered_res = verify_audit_log_integrity(db)
        assert tampered_res["is_valid"] is False
        assert tampered_res["tampered_sequence_num"] == log.sequence_num

        # Restore
        log.action = original_action
        db.commit()
    db.close()
