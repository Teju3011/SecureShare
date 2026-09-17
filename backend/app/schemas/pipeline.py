from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.models.pipeline import PipelineStatus, FindingSeverity


class SecurityFindingResponse(BaseModel):
    id: int
    pipeline_run_id: int
    tool_name: str
    severity: FindingSeverity
    title: str
    description: str
    file_path: Optional[str]
    line_number: Optional[int]
    cve_id: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class PipelineRunResponse(BaseModel):
    id: int
    commit_hash: str
    branch: str
    triggered_by: str
    status: PipelineStatus
    started_at: datetime
    completed_at: Optional[datetime]
    total_findings: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    is_blocked: bool
    findings: List[SecurityFindingResponse] = []

    class Config:
        from_attributes = True


class TriggerScanRequest(BaseModel):
    branch: Optional[str] = "main"
    simulate_fail: Optional[bool] = False
