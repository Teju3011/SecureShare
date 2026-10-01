import io
import pytest


def test_upload_valid_clean_pdf(client, user_a_headers):
    pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Title (Test) >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
    res = client.post(
        "/api/v1/files/upload",
        files={"file": ("report.pdf", io.BytesIO(pdf_content), "application/pdf")},
        headers=user_a_headers
    )
    assert res.status_code == 200
    data = res.json()
    file_info = data.get("file", data)
    assert file_info["status"] == "CLEAN"
    assert file_info["is_quarantined"] is False
    assert "sha256_hash" in file_info


def test_upload_dangerous_pe_executable_blocked(client, user_a_headers):
    exe_content = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00"
    res = client.post(
        "/api/v1/files/upload",
        files={"file": ("malware.exe", io.BytesIO(exe_content), "application/x-msdownload")},
        headers=user_a_headers
    )
    assert res.status_code == 200
    data = res.json()
    file_info = data.get("file", data)
    assert file_info["is_quarantined"] is True
    assert "Dangerous file" in (file_info.get("quarantine_reason") or "")


def test_upload_mime_spoofing_detected(client, user_a_headers):
    fake_png = b"MZ\x90\x00\x03\x00\x00\x00executable disguised as photo"
    res = client.post(
        "/api/v1/files/upload",
        files={"file": ("fake_document.png", io.BytesIO(fake_png), "image/png")},
        headers=user_a_headers
    )
    assert res.status_code == 200
    data = res.json()
    file_info = data.get("file", data)
    assert file_info["is_quarantined"] is True


def test_upload_eicar_antivirus_quarantined(client, user_a_headers):
    from app.scanners.clamav import EICAR_SIGNATURE
    res = client.post(
        "/api/v1/files/upload",
        files={"file": ("eicar_test.com", io.BytesIO(EICAR_SIGNATURE), "application/x-dosexec")},
        headers=user_a_headers
    )
    assert res.status_code == 200
    data = res.json()
    file_info = data.get("file", data)
    assert file_info["is_quarantined"] is True
