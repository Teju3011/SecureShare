from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, get_client_ip, get_user_agent
from app.core.rate_limit import rate_limit_check
from app.models.user import User
from app.models.share import ShareLink
from app.schemas.share import (
    ShareCreateRequest,
    ShareCreateResponse,
    ShareLinkResponse,
    SharePublicInfoResponse,
    ShareAccessRequest,
)
from app.services.share_service import ShareService
from app.audit.logger import log_security_event

router = APIRouter(prefix="/shares", tags=["Secure File Sharing"])


@router.post("/create", response_model=ShareCreateResponse)
@router.post("", response_model=ShareCreateResponse)
def create_share(
    req: ShareCreateRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ip = get_client_ip(request)
    ua = get_user_agent(request)
    share, raw_token = ShareService.create_share_link(
        db=db,
        user=current_user,
        file_id=req.file_id,
        expires_in_hours=req.expires_in_hours,
        password=req.password,
        max_downloads=req.max_downloads,
        client_ip=ip,
        user_agent=ua
    )

    base_url = str(request.base_url).rstrip("/")
    # In browser client, points to frontend /share/<token>
    share_url = f"{base_url}/share/{raw_token}"

    return {
        "id": share.id,
        "file_id": share.file_id,
        "share_token": raw_token,
        "share_url": share_url,
        "expires_at": share.expires_at,
        "max_downloads": share.max_downloads,
        "is_password_protected": bool(share.password_hash),
        "created_at": share.created_at
    }


@router.get("/my-shares", response_model=List[ShareLinkResponse])
def get_user_shares(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shares = db.query(ShareLink).filter(ShareLink.user_id == current_user.id).order_by(ShareLink.created_at.desc()).all()
    results = []
    for s in shares:
        results.append({
            "id": s.id,
            "file_id": s.file_id,
            "original_filename": s.file.original_filename if s.file else "unknown",
            "expires_at": s.expires_at,
            "max_downloads": s.max_downloads,
            "download_count": s.download_count,
            "is_active": s.is_active,
            "is_password_protected": bool(s.password_hash),
            "created_at": s.created_at
        })
    return results


@router.delete("/{share_id}")
def revoke_share(
    share_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    share = db.query(ShareLink).filter(ShareLink.id == share_id, ShareLink.user_id == current_user.id).first()
    if not share:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Share link not found.")
    share.is_active = False
    db.commit()

    ip = get_client_ip(request)
    ua = get_user_agent(request)
    log_security_event(
        db=db,
        action="SHARE_REVOKED",
        resource_type="share",
        resource_id=str(share.id),
        actor_id=current_user.id,
        actor_email=current_user.email,
        ip_address=ip,
        user_agent=ua,
        result="SUCCESS"
    )
    return {"message": "Share link revoked successfully."}


@router.get(
    "/public/{token}/info",
    response_model=SharePublicInfoResponse,
    dependencies=[Depends(rate_limit_check("share_info", max_requests=60, window_seconds=60))]
)
@router.get(
    "/public/{token}",
    response_model=SharePublicInfoResponse,
    dependencies=[Depends(rate_limit_check("share_info", max_requests=60, window_seconds=60))]
)
def get_public_share_info(
    token: str,
    db: Session = Depends(get_db)
):
    return ShareService.get_public_share_info(db, token)


@router.post(
    "/public/{token}/download",
    dependencies=[Depends(rate_limit_check("share_download", max_requests=20, window_seconds=60))]
)
def download_shared_file(
    token: str,
    request: Request,
    body: ShareAccessRequest = None,
    db: Session = Depends(get_db)
):
    password = body.password if body else None
    ip = get_client_ip(request)
    ua = get_user_agent(request)
    data, filename, mime_type = ShareService.download_shared_file(
        db=db,
        token=token,
        password=password,
        client_ip=ip,
        user_agent=ua
    )
    return Response(
        content=data,
        media_type=mime_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Content-Type-Options": "nosniff"
        }
    )
