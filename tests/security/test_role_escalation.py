import pytest


def test_user_cannot_escalate_own_role(client, user_a_headers):
    # Try calling admin user status update endpoint with regular user credentials
    res = client.put(
        "/api/v1/admin/users/1/status",
        json={"is_active": True},
        headers=user_a_headers
    )
    assert res.status_code == 403


def test_user_cannot_release_quarantined_file(client, user_a_headers):
    res = client.post(
        "/api/v1/admin/quarantine/1/release",
        headers=user_a_headers
    )
    assert res.status_code == 403


def test_user_cannot_purge_quarantine(client, user_a_headers):
    res = client.delete(
        "/api/v1/admin/quarantine/1/purge",
        headers=user_a_headers
    )
    assert res.status_code == 403
