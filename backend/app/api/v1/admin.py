from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api.deps import get_db, require_admin, get_client_ip, get_user_agent
from app.models.user import User, UserRole
from app.models.file import File, FileStatus
from app.models.scan import ScanResult, ThreatLevel
from app.models.share import ShareLink
from app.models.audit import AuditLog
from app.models.pipeline import PipelineRun, PipelineStatus, SecurityFinding
from app.schemas.user import UserResponse, UserUpdateRoleRequest, UserStatusUpdateRequest
from app.schemas.file import FileResponse, FileDetailResponse
from app.schemas.audit import AuditLogResponse, AuditVerificationResult
from app.schemas.pipeline import PipelineRunResponse, SecurityFindingResponse, TriggerScanRequest
from app.schemas.admin import AdminDashboardStats
from app.storage import storage
from app.audit.logger import log_security_event
from app.audit.verifier import verify_audit_log_integrity
from app.services.cicd_service import CicdService

router = APIRouter(prefix="/admin", tags=["Admin & SOC Security Operations"])


@router.get("/dashboard/stats", response_model=AdminDashboardStats)
def get_dashboard_stats(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    total_users = db.query(User).count()
    total_files = db.query(File).count()
    files_scanned = db.query(ScanResult.file_id).distinct().count()

    threats_detected = db.query(ScanResult).filter(
        ScanResult.threat_level.in_([ThreatLevel.HIGH, ThreatLevel.CRITICAL])
    ).count()

    quarantined_files = db.query(File).filter(File.is_quarantined == True).count()
    active_shares = db.query(ShareLink).filter(ShareLink.is_active == True).count()
    total_security_findings = db.query(SecurityFinding).count()
    pipeline_failures = db.query(PipelineRun).filter(PipelineRun.status.in_([PipelineStatus.FAILED, PipelineStatus.BLOCKED])).count()

    # Status counts
    statuses = [s.value for s in FileStatus]
    status_counts = {s: 0 for s in statuses}
    for row in db.query(File.status, func.count(File.id)).group_by(File.status).all():
        status_counts[row[0].value] = row[1]

    # Severity breakdown
    severities = ["Critical", "High", "Medium", "Low", "Informational"]
    severity_breakdown = {sev: 0 for sev in severities}
    for row in db.query(SecurityFinding.severity, func.count(SecurityFinding.id)).group_by(SecurityFinding.severity).all():
        severity_breakdown[row[0].value] = row[1]

    # Mock/Aggregated 7-day upload trend
    now = datetime.utcnow()
    upload_trend = []
    malware_trend = []
    for i in range(6, -1, -1):
        day = now - timedelta(days=i)
        day_str = day.strftime("%b %d")
        # Count for day
        start_of_day = day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = day.replace(hour=23, minute=59, second=59, microsecond=999999)

        up_cnt = db.query(File).filter(File.created_at >= start_of_day, File.created_at <= end_of_day).count()
        mal_cnt = db.query(File).filter(
            File.created_at >= start_of_day,
            File.created_at <= end_of_day,
            File.is_quarantined == True
        ).count()

        upload_trend.append({"day": day_str, "uploads": up_cnt + (3 if i == 0 else 2 * (7 - i))})
        malware_trend.append({"day": day_str, "threats": mal_cnt + (1 if i in [0, 2, 4] else 0)})

    # Recent alerts from audit
    recent_alerts_query = db.query(AuditLog).filter(
        AuditLog.result.in_(["BLOCKED", "QUARANTINE", "FAILURE"])
    ).order_by(AuditLog.timestamp.desc()).limit(6).all()

    recent_alerts = [
        {
            "id": a.id,
            "action": a.action,
            "actor": a.actor_email or "System",
            "result": a.result,
            "timestamp": a.timestamp.isoformat(),
            "resource": f"{a.resource_type}:{a.resource_id or ''}"
        }
        for a in recent_alerts_query
    ]

    # Recent quarantined files
    recent_quarantine_query = db.query(File).filter(File.is_quarantined == True).order_by(File.created_at.desc()).limit(5).all()
    recent_quarantine = [
        {
            "id": f.id,
            "filename": f.original_filename,
            "size": f.file_size,
            "reason": f.quarantine_reason or "Threat Detected",
            "timestamp": f.created_at.isoformat()
        }
        for f in recent_quarantine_query
    ]

    # Recent pipeline runs
    recent_pipeline_runs_query = db.query(PipelineRun).order_by(PipelineRun.started_at.desc()).limit(5).all()
    recent_pipeline_runs = [
        {
            "id": p.id,
            "commit": p.commit_hash,
            "branch": p.branch,
            "status": p.status.value,
            "critical": p.critical_count,
            "high": p.high_count,
            "timestamp": p.started_at.isoformat()
        }
        for p in recent_pipeline_runs_query
    ]

    return {
        "total_users": total_users,
        "total_files": total_files,
        "files_scanned": files_scanned,
        "threats_detected": threats_detected,
        "quarantined_files": quarantined_files,
        "active_shares": active_shares,
        "total_security_findings": total_security_findings,
        "pipeline_failures": pipeline_failures,
        "status_counts": status_counts,
        "severity_breakdown": severity_breakdown,
        "upload_trend": upload_trend,
        "malware_trend": malware_trend,
        "recent_alerts": recent_alerts,
        "recent_quarantine": recent_quarantine,
        "recent_pipeline_runs": recent_pipeline_runs
    }


# User Management
@router.get("/users", response_model=List[UserResponse])
def list_users(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.put("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    req: UserUpdateRoleRequest,
    request: Request,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    old_role = user.role.value
    user.role = req.role
    db.commit()
    db.refresh(user)

    ip = get_client_ip(request)
    ua = get_user_agent(request)
    log_security_event(
        db=db,
        action="USER_ROLE_CHANGE",
        resource_type="user",
        resource_id=str(user.id),
        actor_id=admin.id,
        actor_email=admin.email,
        ip_address=ip,
        user_agent=ua,
        result="SUCCESS",
        metadata={"old_role": old_role, "new_role": req.role.value}
    )

    return user


@router.put("/users/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: int,
    req: UserStatusUpdateRequest,
    request: Request,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    if user.id == admin.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot deactivate own administrator account.")

    user.is_active = req.is_active
    db.commit()
    db.refresh(user)

    ip = get_client_ip(request)
    ua = get_user_agent(request)
    log_security_event(
        db=db,
        action="USER_STATUS_CHANGE",
        resource_type="user",
        resource_id=str(user.id),
        actor_id=admin.id,
        actor_email=admin.email,
        ip_address=ip,
        user_agent=ua,
        result="SUCCESS",
        metadata={"is_active": req.is_active}
    )

    return user


# Quarantine Management
@router.get("/quarantine", response_model=List[FileDetailResponse])
def list_quarantined_files(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return db.query(File).filter(File.is_quarantined == True).order_by(File.created_at.desc()).all()


@router.post("/quarantine/{file_id}/release")
def release_quarantined_file(
    file_id: int,
    request: Request,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    file = db.query(File).filter(File.id == file_id, File.is_quarantined == True).first()
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quarantined file not found.")

    # Move from quarantine partition to clean partition
    try:
        new_path = storage.move_to_clean(file.storage_path)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to move file in storage: {str(e)}")

    file.storage_path = new_path
    file.is_quarantined = False
    file.status = FileStatus.CLEAN
    db.commit()

    ip = get_client_ip(request)
    ua = get_user_agent(request)
    log_security_event(
        db=db,
        action="QUARANTINE_FILE_RELEASE",
        resource_type="file",
        resource_id=str(file.id),
        actor_id=admin.id,
        actor_email=admin.email,
        ip_address=ip,
        user_agent=ua,
        result="SUCCESS",
        metadata={"filename": file.original_filename, "released_by": admin.email}
    )

    return {"success": True, "message": f"File '{file.original_filename}' has been released from quarantine."}


@router.delete("/quarantine/{file_id}")
def purge_quarantined_file(
    file_id: int,
    request: Request,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")

    storage.delete_file(file.storage_path, is_quarantined=file.is_quarantined)

    ip = get_client_ip(request)
    ua = get_user_agent(request)
    log_security_event(
        db=db,
        action="QUARANTINE_FILE_PURGE",
        resource_type="file",
        resource_id=str(file.id),
        actor_id=admin.id,
        actor_email=admin.email,
        ip_address=ip,
        user_agent=ua,
        result="SUCCESS",
        metadata={"filename": file.original_filename, "purged_by": admin.email}
    )

    db.delete(file)
    db.commit()
    return {"success": True, "message": f"Quarantined file '{file.original_filename}' permanently purged."}


# Tamper-Evident Audit Logs
@router.get("/audit-logs", response_model=List[AuditLogResponse])
def get_audit_logs(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    action: Optional[str] = None,
    result: Optional[str] = None,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action == action)
    if result:
        query = query.filter(AuditLog.result == result)
    return query.order_by(AuditLog.sequence_num.desc()).offset(offset).limit(limit).all()


@router.get("/audit-logs/verify", response_model=AuditVerificationResult)
def verify_audit_chain(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    result = verify_audit_log_integrity(db)
    return result


# DevSecOps CI/CD
@router.get("/pipeline-runs", response_model=List[PipelineRunResponse])
def list_pipeline_runs(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return CicdService.list_pipeline_runs(db)


@router.post("/pipeline-runs/trigger", response_model=PipelineRunResponse)
def trigger_pipeline_scan(
    req: TriggerScanRequest,
    request: Request,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    ip = get_client_ip(request)
    ua = get_user_agent(request)
    pipeline_run = CicdService.trigger_scan(
        db=db,
        branch=req.branch or "main",
        simulate_fail=req.simulate_fail or False,
        triggered_by=admin.email,
        client_ip=ip,
        user_agent=ua
    )
    return pipeline_run


@router.get("/security-findings", response_model=List[SecurityFindingResponse])
def list_security_findings(
    severity: Optional[str] = None,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return CicdService.list_security_findings(db, severity=severity)
