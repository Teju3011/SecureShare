import io
import pytest


def test_share_link_lifecycle_and_password(client, user_a_headers):
    file_bytes = b"%PDF-1.4\nSecure Shared Whitepaper Content\n%%EOF"
    upload_res = client.post(
        "/api/v1/files/upload",
        files={"file": ("whitepaper.pdf", io.BytesIO(file_bytes), "application/pdf")},
        headers=user_a_headers
    )
    assert upload_res.status_code == 200
    file_id = upload_res.json()["file"]["id"]

    create_res = client.post(
        "/api/v1/shares",
        json={
            "file_id": file_id,
            "password": "SecretShareKey1!",
            "expires_in_hours": 24,
            "max_downloads": 1
        },
        headers=user_a_headers
    )
    assert create_res.status_code == 201 or create_res.status_code == 200
    raw_token = create_res.json()["share_token"]

    meta_res = client.get(f"/api/v1/shares/public/{raw_token}")
    assert meta_res.status_code == 200
    assert meta_res.json()["is_password_protected"] is True

    fail_res = client.post(f"/api/v1/shares/public/{raw_token}/download", json={"password": "WrongPassword"})
    assert fail_res.status_code == 401

    success_res = client.post(f"/api/v1/shares/public/{raw_token}/download", json={"password": "SecretShareKey1!"})
    assert success_res.status_code == 200
    assert success_res.content == file_bytes

    second_res = client.post(f"/api/v1/shares/public/{raw_token}/download", json={"password": "SecretShareKey1!"})
    assert second_res.status_code == 410
