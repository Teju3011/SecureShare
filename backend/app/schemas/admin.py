from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class AdminDashboardStats(BaseModel):
    total_users: int
    total_files: int
    files_scanned: int
    threats_detected: int
    quarantined_files: int
    active_shares: int
    total_security_findings: int
    pipeline_failures: int
    status_counts: Dict[str, int]
    severity_breakdown: Dict[str, int]
    upload_trend: List[Dict[str, Any]]
    malware_trend: List[Dict[str, Any]]
    recent_alerts: List[Dict[str, Any]]
    recent_quarantine: List[Dict[str, Any]]
    recent_pipeline_runs: List[Dict[str, Any]]


class UserDashboardStats(BaseModel):
    total_files: int
    safe_files: int
    scanning_files: int
    quarantined_files: int
    active_shares: int
    recent_files: List[Dict[str, Any]]
    recent_activity: List[Dict[str, Any]]
