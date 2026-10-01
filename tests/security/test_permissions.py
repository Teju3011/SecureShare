import io
import pytest


def test_permission_grant_and_revocation(client, user_a_headers, user_b_headers):
    # 1. User A uploads a file
    pdf_bytes = b"%PDF-1.4\nMulti-User Collaboration Document\n%%EOF"
    upload_res = client.post(
        "/api/v1/files/upload",
        files={"file": ("collab.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
        headers=user_a_headers
    )
    assert upload_res.status_code == 200
    file_id = upload_res.json()["file"]["id"]

    # 2. User A grants permission to User B as VIEWER
    grant_res = client.post(
        f"/api/v1/permissions/{file_id}",
        json={
            "user_email": "userb@example.com",
            "role_preset": "VIEWER",
            "can_view": True,
            "can_download": False
        },
        headers=user_a_headers
    )
    assert grant_res.status_code == 201
    perm_id = grant_res.json()["id"]
    assert grant_res.json()["can_view"] is True
    assert grant_res.json()["can_download"] is False

    # 3. User A lists permissions for the file
    list_res = client.get(f"/api/v1/permissions/{file_id}", headers=user_a_headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # 4. User A revokes permission
    revoke_res = client.delete(f"/api/v1/permissions/{perm_id}", headers=user_a_headers)
    assert revoke_res.status_code == 200

    # 5. Check permissions list shows revoked
    list_after = client.get(f"/api/v1/permissions/{file_id}", headers=user_a_headers)
    revoked_entry = [p for p in list_after.json() if p["id"] == perm_id][0]
    assert revoked_entry["can_view"] is False
    assert revoked_entry["revoked_at"] is not None
