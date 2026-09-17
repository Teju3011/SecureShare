from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.file import File, FileStatus
from app.models.share import ShareLink
from app.models.audit import AuditLog
from app.schemas.admin import UserDashboardStats
from app.schemas.audit import AuditLogResponse

router = APIRouter(prefix="/users", tags=["User Dashboard & Activity"])


@router.get("/dashboard", response_model=UserDashboardStats)
def get_user_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_files = db.query(File).filter(File.user_id == current_user.id).count()
    safe_files = db.query(File).filter(File.user_id == current_user.id, File.status == FileStatus.CLEAN).count()
    scanning_files = db.query(File).filter(
        File.user_id == current_user.id,
        File.status.in_([FileStatus.UPLOADING, FileStatus.VALIDATING, FileStatus.SCANNING])
    ).count()
    quarantined_files = db.query(File).filter(
        File.user_id == current_user.id,
        File.is_quarantined == True
    ).count()
    active_shares = db.query(ShareLink).filter(
        ShareLink.user_id == current_user.id,
        ShareLink.is_active == True
    ).count()

    recent_files_query = db.query(File).filter(File.user_id == current_user.id).order_by(File.created_at.desc()).limit(5).all()
    recent_files = [
        {
            "id": f.id,
            "filename": f.original_filename,
            "size": f.file_size,
            "mime": f.detected_mime,
            "status": f.status.value,
            "is_quarantined": f.is_quarantined,
            "created_at": f.created_at.isoformat()
        }
        for f in recent_files_query
    ]

    recent_activity_query = db.query(AuditLog).filter(
        AuditLog.actor_id == current_user.id
    ).order_by(AuditLog.timestamp.desc()).limit(8).all()

    recent_activity = [
        {
            "id": a.id,
            "action": a.action,
            "resource": f"{a.resource_type}:{a.resource_id or ''}",
            "result": a.result,
            "timestamp": a.timestamp.isoformat()
        }
        for a in recent_activity_query
    ]

    return {
        "total_files": total_files,
        "safe_files": safe_files,
        "scanning_files": scanning_files,
        "quarantined_files": quarantined_files,
        "active_shares": active_shares,
        "recent_files": recent_files,
        "recent_activity": recent_activity
    }


@router.get("/activity", response_model=List[AuditLogResponse])
def get_user_activity(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(AuditLog).filter(
        AuditLog.actor_id == current_user.id
    ).order_by(AuditLog.timestamp.desc()).limit(100).all()
