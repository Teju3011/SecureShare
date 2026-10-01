from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.folder import Folder
from app.models.file import File
from app.security.rbac import get_current_user
from app.audit.logger import log_security_event

router = APIRouter(prefix="/folders", tags=["Folders"])


class FolderCreate(BaseModel):
    folder_name: str
    parent_folder_id: Optional[int] = None


class FolderOut(BaseModel):
    id: int
    folder_name: str
    owner_id: int
    parent_folder_id: Optional[int] = None
    created_at: datetime
    file_count: Optional[int] = 0

    class Config:
        from_attributes = True


class MoveFileRequest(BaseModel):
    folder_id: Optional[int] = None


@router.post("", response_model=FolderOut, status_code=status.HTTP_201_CREATED)
def create_folder(
    req: FolderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not req.folder_name.strip():
        raise HTTPException(status_code=400, detail="Folder name cannot be empty.")

    if req.parent_folder_id:
        parent = db.query(Folder).filter(
            Folder.id == req.parent_folder_id,
            Folder.owner_id == current_user.id
        ).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent folder not found.")

    folder = Folder(
        owner_id=current_user.id,
        parent_folder_id=req.parent_folder_id,
        folder_name=req.folder_name.strip()
    )
    db.add(folder)
    db.commit()
    db.refresh(folder)

    log_security_event(
        db=db,
        action="FOLDER_CREATED",
        resource_type="folder",
        resource_id=str(folder.id),
        actor_id=current_user.id,
        actor_email=current_user.email,
        result="SUCCESS",
        metadata={"folder_name": folder.folder_name}
    )

    return folder


@router.get("", response_model=List[FolderOut])
def list_folders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    folders = db.query(Folder).filter(Folder.owner_id == current_user.id).all()
    results = []
    for f in folders:
        f_count = db.query(File).filter(File.folder_id == f.id, File.is_quarantined == False).count()
        results.append(FolderOut(
            id=f.id,
            folder_name=f.folder_name,
            owner_id=f.owner_id,
            parent_folder_id=f.parent_folder_id,
            created_at=f.created_at,
            file_count=f_count
        ))
    return results


@router.delete("/{folder_id}", status_code=status.HTTP_200_OK)
def delete_folder(
    folder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    folder = db.query(Folder).filter(Folder.id == folder_id, Folder.owner_id == current_user.id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found or unauthorized.")

    # Unlink files in folder (move to root)
    db.query(File).filter(File.folder_id == folder_id).update({"folder_id": None})
    db.delete(folder)
    db.commit()

    log_security_event(
        db=db,
        action="FOLDER_DELETED",
        resource_type="folder",
        resource_id=str(folder_id),
        actor_id=current_user.id,
        actor_email=current_user.email,
        result="SUCCESS"
    )

    return {"detail": f"Folder {folder_id} deleted successfully."}
