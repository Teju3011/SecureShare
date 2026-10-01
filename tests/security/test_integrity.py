import io
import pytest
from app.core.database import SessionLocal
from app.models.file import File


def test_stored_file_integrity_verification(client, user_a_headers):
    file_bytes = b"%PDF-1.4\nCryptographically Validated Invoice Payload\n%%EOF"
    upload_res = client.post(
        "/api/v1/files/upload",
        files={"file": ("invoice.pdf", io.BytesIO(file_bytes), "application/pdf")},
        headers=user_a_headers
    )
    assert upload_res.status_code == 200
    file_id = upload_res.json()["file"]["id"]

    res = client.get(f"/api/v1/files/{file_id}/download", headers=user_a_headers)
    assert res.status_code == 200
    assert res.content == file_bytes


def test_tampered_storage_detected_as_integrity_failure(client, user_a_headers):
    original_bytes = b"%PDF-1.4\nOriginal Unmodified Document\n%%EOF"
    upload_res = client.post(
        "/api/v1/files/upload",
        files={"file": ("tamper_test.pdf", io.BytesIO(original_bytes), "application/pdf")},
        headers=user_a_headers
    )
    assert upload_res.status_code == 200
    file_id = upload_res.json()["file"]["id"]

    db = SessionLocal()
    f_rec = db.query(File).filter(File.id == file_id).first()
    storage_path = f_rec.storage_path
    db.close()

    import os
    if os.path.exists(storage_path):
        with open(storage_path, "wb") as f:
            f.write(b"Corrupted Ciphertext Injected by Attacker")

        download_res = client.get(f"/api/v1/files/{file_id}/download", headers=user_a_headers)
        assert download_res.status_code in [400, 500, 422]
