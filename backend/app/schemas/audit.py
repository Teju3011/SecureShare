from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: int
    sequence_num: int
    actor_id: Optional[int]
    actor_email: Optional[str]
    action: str
    resource_type: str
    resource_id: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    result: str
    metadata_json: Optional[str]
    timestamp: datetime
    previous_hash: str
    entry_hash: str

    class Config:
        from_attributes = True


class AuditVerificationResult(BaseModel):
    is_valid: bool
    total_records: int
    tampered_sequence_num: Optional[int] = None
    expected_hash: Optional[str] = None
    actual_hash: Optional[str] = None
    message: str
