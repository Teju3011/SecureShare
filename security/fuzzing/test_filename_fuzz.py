import io
import pytest

MALFORMED_FILENAMES = [
    "../../../../etc/passwd",
    "..\\..\\..\\windows\\system32\\cmd.exe",
    "test\x00file.pdf",
    "CON.pdf",
    "PRN.txt",
    "AUX.png",
    "NUL.docx",
    "COM1.pdf",
    "LPT1.pdf",
    " " * 100 + "evil.pdf",
    "normal.pdf" + ".exe" * 50,
    "invoice\u202Efdp.exe",  # Right-to-Left Override spoofing
    "test;rm -rf /;.pdf",
    "`id`.pdf",
    "$(whoami).pdf",
    "A" * 300 + ".pdf",
]


def test_filename_fuzzing(client, user_a_headers):
    for fname in MALFORMED_FILENAMES:
        content = b"%PDF-1.4\nTest Document Content\n%%EOF"
        res = client.post(
            "/api/v1/files/upload",
            files={"file": (fname, io.BytesIO(content), "application/pdf")},
            headers=user_a_headers
        )
        # Server must reject with 400 or sanitize safely and return 200 without directory traversal
        assert res.status_code in [200, 201, 400, 422], f"Crash 500 on filename: {repr(fname)}"
