import io
from datetime import datetime, timedelta
import pytest


def test_secure_share_lifecycle(client, user_headers):
    # 1. Upload clean file
    file_resp = client.post(
        "/api/v1/files/upload",
        files={"file": ("shared_doc.txt", io.BytesIO(b"Hello Shared World!"), "text/plain")},
        headers=user_headers
    )
    file_id = file_resp.json()["file"]["id"]

    # 2. Create password-protected share with max 1 download
    create_resp = client.post(
        "/api/v1/shares/create",
        json={
            "file_id": file_id,
            "expires_in_hours": 2,
            "password": "SecretPassword123!",
            "max_downloads": 1
        },
        headers=user_headers
    )
    assert create_resp.status_code == 200
    share_data = create_resp.json()
    token = share_data["share_token"]
    assert token is not None

    # 3. Public info preview
    info_resp = client.get(f"/api/v1/shares/public/{token}/info")
    assert info_resp.status_code == 200
    info = info_resp.json()
    assert info["is_password_protected"] is True
    assert info["is_expired"] is False
    assert info["remaining_downloads"] == 1

    # 4. Attempt download with wrong password -> 401
    bad_dl = client.post(
        f"/api/v1/shares/public/{token}/download",
        json={"password": "WrongPassword!"}
    )
    assert bad_dl.status_code == 401

    # 5. Download with correct password -> 200
    good_dl = client.post(
        f"/api/v1/shares/public/{token}/download",
        json={"password": "SecretPassword123!"}
    )
    assert good_dl.status_code == 200
    assert good_dl.content == b"Hello Shared World!"

    # 6. Attempt download again -> 410 (limit exceeded)
    exceeded_dl = client.post(
        f"/api/v1/shares/public/{token}/download",
        json={"password": "SecretPassword123!"}
    )
    assert exceeded_dl.status_code == 410


def test_cannot_share_quarantined_file(client, user_headers):
    # Upload EICAR file
    malware_resp = client.post("/api/v1/files/upload-eicar", headers=user_headers)
    malware_id = malware_resp.json()["file"]["id"]

    # Attempt to share quarantined file
    share_resp = client.post(
        "/api/v1/shares/create",
        json={"file_id": malware_id, "expires_in_hours": 24},
        headers=user_headers
    )
    assert share_resp.status_code == 400
    assert "Only files verified as CLEAN can be shared" in share_resp.json()["detail"]
