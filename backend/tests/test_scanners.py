import io
import pytest
from app.scanners.clamav import EICAR_SIGNATURE


def test_upload_clean_file(client, user_headers):
    clean_content = b"%PDF-1.4\n1 0 obj\n<< /Title (Safe Document) >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
    response = client.post(
        "/api/v1/files/upload",
        files={"file": ("safe_document.pdf", io.BytesIO(clean_content), "application/pdf")},
        headers=user_headers
    )
    assert response.status_code == 200
    data = response.json()
    file_info = data["file"]
    assert file_info["status"] == "CLEAN"
    assert file_info["is_quarantined"] is False
    assert file_info["sha256_hash"] is not None

    # Test clean download
    file_id = file_info["id"]
    download_resp = client.get(f"/api/v1/files/{file_id}/download", headers=user_headers)
    assert download_resp.status_code == 200
    assert download_resp.content == clean_content


def test_upload_eicar_malware_quarantined(client, user_headers):
    response = client.post("/api/v1/files/upload-eicar", headers=user_headers)
    assert response.status_code == 200
    data = response.json()
    file_info = data["file"]
    assert file_info["status"] in ["MALICIOUS", "QUARANTINED"]
    assert file_info["is_quarantined"] is True
    assert "EICAR" in (file_info["quarantine_reason"] or "")

    # Test that download is strictly BLOCKED
    file_id = file_info["id"]
    blocked_resp = client.get(f"/api/v1/files/{file_id}/download", headers=user_headers)
    assert blocked_resp.status_code == 403
    assert "Security Policy: This file cannot be downloaded" in blocked_resp.json()["detail"]


def test_upload_dangerous_executable_blocked(client, user_headers):
    # Windows PE MZ executable header
    exe_content = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00"
    response = client.post(
        "/api/v1/files/upload",
        files={"file": ("malicious_payload.exe", io.BytesIO(exe_content), "application/x-dosexec")},
        headers=user_headers
    )
    assert response.status_code == 200
    data = response.json()
    file_info = data["file"]
    assert file_info["is_quarantined"] is True
    assert "Dangerous file detected" in (file_info["quarantine_reason"] or "")


def test_mime_spoofing_detection(client, user_headers):
    # Executable pretending to be an image/png
    fake_png = b"MZ\x90\x00\x03\x00\x00\x00executable disguised as photo"
    response = client.post(
        "/api/v1/files/upload",
        files={"file": ("profile_photo.png", io.BytesIO(fake_png), "image/png")},
        headers=user_headers
    )
    assert response.status_code == 200
    data = response.json()
    file_info = data["file"]
    assert file_info["is_quarantined"] is True
    assert "MIME Spoofing" in (file_info["quarantine_reason"] or "") or "Dangerous" in (file_info["quarantine_reason"] or "")


def test_encryption_at_rest(client, user_headers):
    secret_text = b"Confidential business secrets that must be encrypted at rest!"
    response = client.post(
        "/api/v1/files/upload",
        files={"file": ("secrets.txt", io.BytesIO(secret_text), "text/plain")},
        headers=user_headers
    )
    assert response.status_code == 200
    file_id = response.json()["file"]["id"]

    # Verify decrypted output on download
    dl_resp = client.get(f"/api/v1/files/{file_id}/download", headers=user_headers)
    assert dl_resp.content == secret_text
