import pytest
from app.models.audit import AuditLog
from tests.conftest import TestingSessionLocal


def test_admin_dashboard_stats(client, admin_headers):
    response = client.get("/api/v1/admin/dashboard/stats", headers=admin_headers)
    assert response.status_code == 200
    stats = response.json()
    assert "total_users" in stats
    assert "total_files" in stats
    assert "threats_detected" in stats
    assert "status_counts" in stats


def test_audit_log_cryptographic_verification(client, admin_headers):
    # Verify valid chain
    verify_resp = client.get("/api/v1/admin/audit-logs/verify", headers=admin_headers)
    assert verify_resp.status_code == 200
    res = verify_resp.json()
    assert res["is_valid"] is True
    assert res["tampered_sequence_num"] is None


def test_audit_log_tamper_detection(client, admin_headers):
    # Deliberately modify an existing record in the test database to simulate attacker tampering
    db = TestingSessionLocal()
    target_log = db.query(AuditLog).first()
    assert target_log is not None
    original_action = target_log.action
    target_seq = target_log.sequence_num
    target_id = target_log.id

    target_log.action = "TAMPERED_ACTION_NAME"
    db.commit()
    db.close()

    # Verify that the audit verification engine detects the cryptographic mismatch
    verify_resp = client.get("/api/v1/admin/audit-logs/verify", headers=admin_headers)
    assert verify_resp.status_code == 200
    res = verify_resp.json()
    assert res["is_valid"] is False
    assert res["tampered_sequence_num"] == target_seq

    # Restore action so subsequent tests are clean
    db2 = TestingSessionLocal()
    restored_log = db2.query(AuditLog).filter(AuditLog.id == target_id).first()
    restored_log.action = original_action
    db2.commit()
    db2.close()


def test_cicd_pipeline_security_gate(client, admin_headers):
    # 1. Trigger passing scan
    pass_resp = client.post(
        "/api/v1/admin/pipeline-runs/trigger",
        json={"branch": "main", "simulate_fail": False},
        headers=admin_headers
    )
    assert pass_resp.status_code == 200
    pass_run = pass_resp.json()
    assert pass_run["status"] == "PASSED"
    assert pass_run["is_blocked"] is False

    # 2. Trigger failing scan with Critical vulnerability
    fail_resp = client.post(
        "/api/v1/admin/pipeline-runs/trigger",
        json={"branch": "feature/risky-code", "simulate_fail": True},
        headers=admin_headers
    )
    assert fail_resp.status_code == 200
    fail_run = fail_resp.json()
    assert fail_run["status"] == "BLOCKED"
    assert fail_run["is_blocked"] is True
    assert fail_run["critical_count"] > 0
