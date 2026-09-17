from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ShareCreateRequest(BaseModel):
    file_id: int
    expires_in_hours: Optional[int] = Field(24, ge=1, le=720)  # Up to 30 days
    password: Optional[str] = Field(None, min_length=4, max_length=128)
    max_downloads: Optional[int] = Field(None, ge=1, le=1000)


class ShareCreateResponse(BaseModel):
    id: int
    file_id: int
    share_token: str  # Raw token returned ONCE upon creation
    share_url: str
    expires_at: Optional[datetime]
    max_downloads: Optional[int]
    is_password_protected: bool
    created_at: datetime


class ShareLinkResponse(BaseModel):
    id: int
    file_id: int
    original_filename: str
    expires_at: Optional[datetime]
    max_downloads: Optional[int]
    download_count: int
    is_active: bool
    is_password_protected: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SharePublicInfoResponse(BaseModel):
    file_id: int
    original_filename: str
    file_size: int
    detected_mime: str
    is_password_protected: bool
    is_expired: bool
    is_limit_reached: bool
    expires_at: Optional[datetime]
    remaining_downloads: Optional[int]


class ShareAccessRequest(BaseModel):
    password: Optional[str] = None
