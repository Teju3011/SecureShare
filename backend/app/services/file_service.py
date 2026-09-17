from typing import Tuple, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.file import File, FileStatus
from app.models.user import User, UserRole
from app.models.scan import ScanResult
from app.security.encryption import file_encryptor
from app.storage import storage
from app.audit.logger import log_security_event


class FileService:
    @staticmethod
    def get_user_files(db: Session, user: User) -> List[File]:
        """Admins see all files, standard users see only their own."""
        if user.role == UserRole.ADMIN:
            return db.query(File).order_by(File.created_at.desc()).all()
        return db.query(File).filter(File.user_id == user.id).order_by(File.created_at.desc()).all()

    @staticmethod
    def get_file_by_id(db: Session, file_id: int, user: User) -> File:
        file = db.query(File).filter(File.id == file_id).first()
        if not file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
        if file.user_id != user.id and user.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
        return file

    @staticmethod
    def download_file(
        db: Session,
        file_id: int,
        user: User,
        client_ip: str = "127.0.0.1",
        user_agent: str = "SecureShare-Web"
    ) -> Tuple[bytes, str, str]:
        """
        Secure file download flow:
        1. Validates ownership or admin privileges.
        2. Strict verification: file MUST have status CLEAN and NOT quarantined.
        3. Fetches encrypted bytes from storage.
        4. Decrypts AES-256-GCM in memory.
        5. Logs tamper-evident audit record.
        """
        file = FileService.get_file_by_id(db, file_id, user)

        # Strict security gate: NEVER download unvalidated or quarantined files
        if file.is_quarantined or file.status != FileStatus.CLEAN:
            log_security_event(
                db=db,
                action="DOWNLOAD_BLOCKED",
                resource_type="file",
                resource_id=str(file.id),
                actor_id=user.id,
                actor_email=user.email,
                ip_address=client_ip,
                user_agent=user_agent,
                result="BLOCKED",
                metadata={"reason": "File is quarantined or failed security scan.", "status": file.status.value}
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Security Policy: This file cannot be downloaded because its status is {file.status.value}."
            )

        # Retrieve ciphertext and decrypt
        try:
            ciphertext = storage.get_file(file.storage_path, is_quarantined=False)
            plaintext = file_encryptor.decrypt(file.encryption_iv, ciphertext)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to decrypt file: {str(e)}"
            )

        log_security_event(
            db=db,
            action="FILE_DOWNLOAD",
            resource_type="file",
            resource_id=str(file.id),
            actor_id=user.id,
            actor_email=user.email,
            ip_address=client_ip,
            user_agent=user_agent,
            result="SUCCESS",
            metadata={"filename": file.original_filename, "size": file.file_size}
        )

        return plaintext, file.original_filename, file.detected_mime

    @staticmethod
    def delete_file(
        db: Session,
        file_id: int,
        user: User,
        client_ip: str = "127.0.0.1",
        user_agent: str = "SecureShare-Web"
    ) -> bool:
        file = FileService.get_file_by_id(db, file_id, user)
        # Remove from storage
        storage.delete_file(file.storage_path, is_quarantined=file.is_quarantined)

        log_security_event(
            db=db,
            action="FILE_DELETE",
            resource_type="file",
            resource_id=str(file.id),
            actor_id=user.id,
            actor_email=user.email,
            ip_address=client_ip,
            user_agent=user_agent,
            result="SUCCESS",
            metadata={"filename": file.original_filename}
        )

        db.delete(file)
        db.commit()
        return True
