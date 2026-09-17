from typing import List
from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, HTTPException, status, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, get_client_ip, get_user_agent
from app.core.rate_limit import rate_limit_check
from app.models.user import User
from app.schemas.file import FileResponse, FileDetailResponse, FileUploadResponse
from app.scanners.pipeline import run_security_pipeline
from app.scanners.clamav import EICAR_SIGNATURE
from app.services.file_service import FileService

router = APIRouter(prefix="/files", tags=["File Management & Security Pipeline"])


@router.post(
    "/upload",
    response_model=FileUploadResponse,
    dependencies=[Depends(rate_limit_check("file_upload", max_requests=30, window_seconds=60))]
)
async def upload_file(
    request: Request,
    file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ip = get_client_ip(request)
    ua = get_user_agent(request)
    raw_data = await file.read()

    try:
        processed_file = run_security_pipeline(
            db=db,
            user_id=current_user.id,
            user_email=current_user.email,
            original_filename=file.filename or "unknown_file",
            declared_mime=file.content_type or "application/octet-stream",
            raw_data=raw_data,
            client_ip=ip,
            user_agent=ua
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    status_msg = (
        f"File security scan completed: status is {processed_file.status.value}. "
        + ("File quarantined due to security findings." if processed_file.is_quarantined else "File verified CLEAN and encrypted.")
    )

    return {
        "file": processed_file,
        "message": status_msg,
        "pipeline_status": processed_file.status.value
    }


@router.post(
    "/upload-eicar",
    response_model=FileUploadResponse,
    dependencies=[Depends(rate_limit_check("file_upload_eicar", max_requests=20, window_seconds=60))]
)
def upload_eicar_test_file(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Demo action: Uploads a standard, benign EICAR Antivirus Test File to verify
    real-time automated malware detection and quarantine isolation.
    """
    ip = get_client_ip(request)
    ua = get_user_agent(request)
    processed_file = run_security_pipeline(
        db=db,
        user_id=current_user.id,
        user_email=current_user.email,
        original_filename="eicar_antivirus_test.com",
        declared_mime="application/x-dosexec",
        raw_data=EICAR_SIGNATURE,
        client_ip=ip,
        user_agent=ua
    )

    return {
        "file": processed_file,
        "message": "EICAR Antivirus Test File intercepted. Malware signature detected; file isolated to quarantine.",
        "pipeline_status": processed_file.status.value
    }


@router.get("/", response_model=List[FileResponse])
def list_files(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return FileService.get_user_files(db, current_user)


@router.get("/{file_id}", response_model=FileDetailResponse)
def get_file_details(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return FileService.get_file_by_id(db, file_id, current_user)


@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ip = get_client_ip(request)
    ua = get_user_agent(request)
    data, filename, mime_type = FileService.download_file(
        db=db,
        file_id=file_id,
        user=current_user,
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


@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ip = get_client_ip(request)
    ua = get_user_agent(request)
    success = FileService.delete_file(
        db=db,
        file_id=file_id,
        user=current_user,
        client_ip=ip,
        user_agent=ua
    )
    return {"success": success, "message": "File successfully deleted."}
