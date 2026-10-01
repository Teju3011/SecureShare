from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.file import File
from app.models.permission import Permission
from app.security.rbac import get_current_user
from app.audit.logger import log_security_event

router = APIRouter(prefix="/permissions", tags=["Permissions"])


class PermissionCreate(BaseModel):
    user_email: EmailStr
    role_preset: str = "VIEWER"  # VIEWER, DOWNLOADER, EDITOR, COLLABORATOR, OWNER
    can_view: bool = True
    can_download: bool = False
    can_edit: bool = False
    can_share: bool = False


class PermissionOut(BaseModel):
    id: int
    file_id: int
    user_id: int
    user_email: str
    user_name: str
    role_preset: str
    can_view: bool
    can_download: bool
    can_edit: bool
    can_share: bool
    granted_at: datetime
    revoked_at: Optional[datetime] = None

    class Config:
        from_attributes = True


@router.get("/{file_id}", response_model=List[PermissionOut])
def get_file_permissions(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found.")

    # Only owner or admin can view permission table
    if file.user_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Unauthorized to view permissions for this file.")

    perms = db.query(Permission).filter(Permission.file_id == file_id).all()
    out = []
    for p in perms:
        u = db.query(User).filter(User.id == p.user_id).first()
        out.append(PermissionOut(
            id=p.id,
            file_id=p.file_id,
            user_id=p.user_id,
            user_email=u.email if u else "unknown",
            user_name=u.full_name if u else "unknown",
            role_preset=p.role_preset,
            can_view=p.can_view,
            can_download=p.can_download,
            can_edit=p.can_edit,
            can_share=p.can_share,
            granted_at=p.granted_at,
            revoked_at=p.revoked_at
        ))
    return out


@router.post("/{file_id}", response_model=PermissionOut, status_code=status.HTTP_201_CREATED)
def grant_permission(
    file_id: int,
    req: PermissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found.")

    if file.user_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Unauthorized to grant permissions on this file.")

    target_user = db.query(User).filter(User.email == req.user_email).first()
    if not target_user:
        raise HTTPException(status_code=404, detail=f"User with email '{req.user_email}' not found.")

    if target_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot assign permission to yourself (you are already the owner).")

    # Preset normalization
    preset = req.role_preset.upper()
    can_v = req.can_view
    can_d = req.can_download
    can_e = req.can_edit
    can_s = req.can_share

    if preset == "VIEWER":
        can_v, can_d, can_e, can_s = True, False, False, False
    elif preset == "DOWNLOADER":
        can_v, can_d, can_e, can_s = True, True, False, False
    elif preset == "EDITOR":
        can_v, can_d, can_e, can_s = True, True, True, False
    elif preset in ["COLLABORATOR", "OWNER"]:
        can_v, can_d, can_e, can_s = True, True, True, True

    # Upsert permission
    existing = db.query(Permission).filter(
        Permission.file_id == file_id,
        Permission.user_id == target_user.id
    ).first()

    if existing:
        existing.can_view = can_v
        existing.can_download = can_d
        existing.can_edit = can_e
        existing.can_share = can_s
        existing.role_preset = preset
        existing.revoked_at = None
        perm = existing
    else:
        perm = Permission(
            file_id=file_id,
            user_id=target_user.id,
            can_view=can_v,
            can_download=can_d,
            can_edit=can_e,
            can_share=can_s,
            role_preset=preset
        )
        db.add(perm)

    db.commit()
    db.refresh(perm)

    log_security_event(
        db=db,
        action="PERMISSION_GRANTED",
        resource_type="permission",
        resource_id=str(perm.id),
        actor_id=current_user.id,
        actor_email=current_user.email,
        result="SUCCESS",
        metadata={
            "file_id": file_id,
            "target_user": target_user.email,
            "preset": preset,
            "can_download": can_d
        }
    )

    return PermissionOut(
        id=perm.id,
        file_id=perm.file_id,
        user_id=perm.user_id,
        user_email=target_user.email,
        user_name=target_user.full_name,
        role_preset=perm.role_preset,
        can_view=perm.can_view,
        can_download=perm.can_download,
        can_edit=perm.can_edit,
        can_share=perm.can_share,
        granted_at=perm.granted_at,
        revoked_at=perm.revoked_at
    )


@router.delete("/{permission_id}", status_code=status.HTTP_200_OK)
def revoke_permission(
    permission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    perm = db.query(Permission).filter(Permission.id == permission_id).first()
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found.")

    file = db.query(File).filter(File.id == perm.file_id).first()
    if not file or (file.user_id != current_user.id and current_user.role != "ADMIN"):
        raise HTTPException(status_code=403, detail="Unauthorized to revoke permission for this file.")

    perm.revoked_at = datetime.utcnow()
    perm.can_view = False
    perm.can_download = False
    perm.can_edit = False
    perm.can_share = False
    db.commit()

    log_security_event(
        db=db,
        action="PERMISSION_REVOKED",
        resource_type="permission",
        resource_id=str(permission_id),
        actor_id=current_user.id,
        actor_email=current_user.email,
        result="SUCCESS",
        metadata={"file_id": file.id, "revoked_user_id": perm.user_id}
    )

    return {"detail": f"Permission {permission_id} revoked immediately."}
