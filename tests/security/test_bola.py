import io
import pytest


def test_bola_prevented_between_users(client, user_a_headers, user_b_headers):
    # 1. User A uploads a private file
    file_bytes = b"%PDF-1.4\nUser A Private Confidential Document\n%%EOF"
    upload_res = client.post(
        "/api/v1/files/upload",
        files={"file": ("confidential_usera.pdf", io.BytesIO(file_bytes), "application/pdf")},
        headers=user_a_headers
    )
    assert upload_res.status_code == 200
    file_id = upload_res.json()["file"]["id"]

    # 2. User A can view details
    res_a = client.get(f"/api/v1/files/{file_id}", headers=user_a_headers)
    assert res_a.status_code == 200

    # 3. User B tries to view User A's file details by tampering with file_id (BOLA)
    res_b = client.get(f"/api/v1/files/{file_id}", headers=user_b_headers)
    assert res_b.status_code in [403, 404]

    # 4. User B tries to download User A's file directly (BOLA)
    download_res_b = client.get(f"/api/v1/files/{file_id}/download", headers=user_b_headers)
    assert download_res_b.status_code in [403, 404]
