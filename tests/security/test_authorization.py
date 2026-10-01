import io
import pytest


def test_user_cannot_access_admin_dashboard(client, user_a_headers):
    res = client.get("/api/v1/admin/stats", headers=user_a_headers)
    assert res.status_code == 403


def test_admin_can_access_admin_dashboard(client, admin_headers):
    res = client.get("/api/v1/admin/stats", headers=admin_headers)
    assert res.status_code == 200
    data = res.json()
    assert "total_files" in data
    assert "total_users" in data


def test_unauthenticated_request_rejected(client):
    res = client.get("/api/v1/files", headers={})
    assert res.status_code == 401
