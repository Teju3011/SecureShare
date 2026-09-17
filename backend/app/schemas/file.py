from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.models.file import FileStatus
from app.models.scan import ScanStatus, ThreatLevel


class ScanResultResponse(BaseModel):
    id: int
    scanner_name: str
    scan_status: ScanStatus
    threat_level: ThreatLevel
    threat_name: Optional[str] = None
    details: Optional[str] = None
    scanned_at: datetime

    class Config:
        from_attributes = True


class FileResponse(BaseModel):
    id: int
    user_id: int
    original_filename: str
    file_size: int
    declared_mime: str
    detected_mime: str
    magic_bytes_preview: Optional[str] = None
    sha256_hash: str
    status: FileStatus
    is_quarantined: bool
    quarantine_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FileDetailResponse(FileResponse):
    scan_results: List[ScanResultResponse] = []


class FileUploadResponse(BaseModel):
    file: FileResponse
    message: str
    pipeline_status: str
