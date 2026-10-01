import io
import pytest


def test_download_clean_file_success(client, user_a_headers):
    pdf_bytes = b"%PDF-1.4\nClean Printable Document Content\n%%EOF"
    upload_res = client.post(
        "/api/v1/files/upload",
        files={"file": ("printable.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
        headers=user_a_headers
    )
    assert upload_res.status_code == 200
    data = upload_res.json()
    file_id = data.get("file", data)["id"]

    download_res = client.get(f"/api/v1/files/{file_id}/download", headers=user_a_headers)
    assert download_res.status_code == 200
    assert download_res.content == pdf_bytes


def test_download_quarantined_file_forbidden(client, user_a_headers, admin_headers):
    q_res = client.get("/api/v1/admin/quarantine", headers=admin_headers)
    assert q_res.status_code == 200
    items = q_res.json()
    if items:
        q_id = items[0]["id"]
        res = client.get(f"/api/v1/files/{q_id}/download", headers=user_a_headers)
        assert res.status_code == 403
