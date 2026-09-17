import hashlib
from typing import Tuple, Optional, Dict

# Known magic byte signatures: (prefix_bytes, detected_mime, allowed_declared_mimes)
FILE_SIGNATURES: Dict[str, Tuple[bytes, str]] = {
    "pdf": (b"%PDF", "application/pdf"),
    "png": (b"\x89PNG\r\n\x1a\n", "image/png"),
    "jpeg": (b"\xff\xd8\xff", "image/jpeg"),
    "gif87": (b"GIF87a", "image/gif"),
    "gif89": (b"GIF89a", "image/gif"),
    "zip_or_office": (b"PK\x03\x04", "application/zip"),
    "gz": (b"\x1f\x8b", "application/gzip"),
    "pe_exec": (b"MZ", "application/x-dosexec"),
    "elf_exec": (b"\x7fELF", "application/x-executable"),
}


def calculate_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def detect_magic_signature(data: bytes, declared_mime: str, filename: str) -> Tuple[str, str, bool, Optional[str]]:
    """
    Inspects raw file bytes to determine actual signature, previews magic bytes,
    and checks for MIME spoofing or extension mismatch.
    Returns:
        (detected_mime, magic_bytes_preview_hex, is_valid, mismatch_reason)
    """
    magic_preview = data[:16].hex().upper() if len(data) >= 16 else data.hex().upper()
    ext = filename.split(".")[-1].lower() if "." in filename else ""

    # Check known binary signatures
    if data.startswith(b"%PDF"):
        detected_mime = "application/pdf"
    elif data.startswith(b"\x89PNG\r\n\x1a\n"):
        detected_mime = "image/png"
    elif data.startswith(b"\xff\xd8\xff"):
        detected_mime = "image/jpeg"
    elif data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        detected_mime = "image/gif"
    elif data.startswith(b"PK\x03\x04"):
        # Could be docx, xlsx, pptx, or plain zip
        if ext in ["docx", "doc"]:
            detected_mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif ext in ["xlsx", "xls"]:
            detected_mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif ext in ["pptx", "ppt"]:
            detected_mime = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        else:
            detected_mime = "application/zip"
    elif data.startswith(b"\x1f\x8b"):
        detected_mime = "application/gzip"
    elif data.startswith(b"MZ"):
        detected_mime = "application/x-dosexec"
    elif data.startswith(b"\x7fELF"):
        detected_mime = "application/x-executable"
    elif len(data) >= 8 and data[4:8] in [b"ftyp", b"moov"]:
        detected_mime = "video/mp4"
    else:
        # Check if plain text / json / csv
        try:
            data[:4096].decode("utf-8")
            if ext == "json":
                detected_mime = "application/json"
            elif ext == "csv":
                detected_mime = "text/csv"
            elif ext in ["html", "htm"]:
                detected_mime = "text/html"
            else:
                detected_mime = "text/plain"
        except UnicodeDecodeError:
            detected_mime = "application/octet-stream"

    # Validate against declared MIME and file extension
    norm_declared = declared_mime.lower().split(";")[0].strip()

    # Mismatch detection: e.g. .jpg file declared as image/jpeg but actually containing MZ / PE header
    if detected_mime == "application/x-dosexec" and "image" in norm_declared:
        return detected_mime, magic_preview, False, "MIME Spoofing detected: Executable binary disguised as image!"

    if detected_mime == "application/x-executable" and ("image" in norm_declared or "text" in norm_declared):
        return detected_mime, magic_preview, False, "MIME Spoofing detected: ELF executable disguised as document!"

    # PDF claimed to be image or vice versa
    if "image" in norm_declared and detected_mime == "application/pdf":
        return detected_mime, magic_preview, False, "MIME mismatch: PDF document declared as image."

    if "pdf" in norm_declared and detected_mime.startswith("image/"):
        return detected_mime, magic_preview, False, "MIME mismatch: Image file declared as PDF."

    return detected_mime, magic_preview, True, None
