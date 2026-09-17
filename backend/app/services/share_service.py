import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.file import File, FileStatus
from app.models.share import ShareLink
from app.models.user import User
from app.security.password import get_password_hash, verify_password
from app.security.encryption import file_encryptor
from app.storage import storage
from app.audit.logger import log_security_event


class ShareService:
    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @staticmethod
    def create_share_link(
        db: Session,
        user: User,
        file_id: int,
        expires_in_hours: Optional[int] = 24,
        password: Optional[str] = None,
        max_downloads: Optional[int] = None,
        client_ip: str = "127.0.0.1",
        user_agent: str = "SecureShare-Web"
    ) -> Tuple[ShareLink, str]:
        # 1. Verify file ownership and status
        file = db.query(File).filter(File.id == file_id).first()
        if not file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found.")
        if file.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this file.")

        # Zero-trust check: NEVER allow unvalidated or quarantined files to be shared!
        if file.status != FileStatus.CLEAN or file.is_quarantined:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Security Policy: Only files verified as CLEAN can be shared."
            )

        # 2. Generate cryptographically random token (32 bytes url-safe = 43 chars)
        raw_token = secrets.token_urlsafe(32)
        token_hash = ShareService._hash_token(raw_token)

        # 3. Handle optional password
        pwd_hash = get_password_hash(password) if password else None

        # 4. Expiry
        expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours) if expires_in_hours else None

        share = ShareLink(
            file_id=file.id,
            user_id=user.id,
            token_hash=token_hash,
            password_hash=pwd_hash,
            expires_at=expires_at,
            max_downloads=max_downloads,
            download_count=0,
            is_active=True,
        )
        db.add(share)
        db.commit()
        db.refresh(share)

        log_security_event(
            db=db,
            action="SHARE_CREATE",
            resource_type="share",
            resource_id=str(share.id),
            actor_id=user.id,
            actor_email=user.email,
            ip_address=client_ip,
            user_agent=user_agent,
            result="SUCCESS",
            metadata={
                "file_id": file.id,
                "filename": file.original_filename,
                "has_password": bool(password),
                "max_downloads": max_downloads,
                "expires_at": expires_at.isoformat() if expires_at else None
            }
        )

        return share, raw_token

    @staticmethod
    def get_public_share_info(db: Session, token: str) -> dict:
        token_hash = ShareService._hash_token(token)
        share = db.query(ShareLink).filter(ShareLink.token_hash == token_hash, ShareLink.is_active == True).first()
        if not share:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Share link not found or inactive.")

        file = share.file
        is_expired = bool(share.expires_at and datetime.utcnow() > share.expires_at)
        is_limit_reached = bool(share.max_downloads and share.download_count >= share.max_downloads)
        remaining = max(0, share.max_downloads - share.download_count) if share.max_downloads else None

        return {
            "file_id": file.id,
            "original_filename": file.original_filename,
            "file_size": file.file_size,
            "detected_mime": file.detected_mime,
            "is_password_protected": bool(share.password_hash),
            "is_expired": is_expired,
            "is_limit_reached": is_limit_reached,
            "expires_at": share.expires_at,
            "remaining_downloads": remaining,
        }

    @staticmethod
    def download_shared_file(
        db: Session,
        token: str,
        password: Optional[str] = None,
        client_ip: str = "127.0.0.1",
        user_agent: str = "SecureShare-Web"
    ) -> Tuple[bytes, str, str]:
        token_hash = ShareService._hash_token(token)
        share = db.query(ShareLink).filter(ShareLink.token_hash == token_hash, ShareLink.is_active == True).first()
        if not share:
            log_security_event(
                db=db,
                action="SHARE_ACCESS_FAILED",
                resource_type="share",
                result="FAILURE",
                ip_address=client_ip,
                user_agent=user_agent,
                metadata={"reason": "Invalid or inactive token"}
            )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Share link invalid or inactive.")

        # Check expiration
        if share.expires_at and datetime.utcnow() > share.expires_at:
            log_security_event(
                db=db,
                action="SHARE_ACCESS_FAILED",
                resource_type="share",
                resource_id=str(share.id),
                result="BLOCKED",
                ip_address=client_ip,
                user_agent=user_agent,
                metadata={"reason": "Share link has expired"}
            )
            raise HTTPException(status_code=status.HTTP_410_GONE, detail="This share link has expired.")

        # Check download limit
        if share.max_downloads and share.download_count >= share.max_downloads:
            log_security_event(
                db=db,
                action="SHARE_ACCESS_FAILED",
                resource_type="share",
                resource_id=str(share.id),
                result="BLOCKED",
                ip_address=client_ip,
                user_agent=user_agent,
                metadata={"reason": "Download limit reached"}
            )
            raise HTTPException(status_code=status.HTTP_410_GONE, detail="Download limit for this link has been reached.")

        # Verify password if required
        if share.password_hash:
            if not password or not verify_password(password, share.password_hash):
                log_security_event(
                    db=db,
                    action="SHARE_ACCESS_FAILED",
                    resource_type="share",
                    resource_id=str(share.id),
                    result="FAILURE",
                    ip_address=client_ip,
                    user_agent=user_agent,
                    metadata={"reason": "Incorrect share password attempt"}
                )
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password for this file share.")

        file = share.file
        # Verify file is still clean and not quarantined
        if file.status != FileStatus.CLEAN or file.is_quarantined:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="File is currently restricted or quarantined.")

        # Increment download count
        share.download_count += 1
        db.commit()

        # Decrypt payload
        try:
            ciphertext = storage.get_file(file.storage_path, is_quarantined=False)
            plaintext = file_encryptor.decrypt(file.encryption_iv, ciphertext)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Decryption failure.")

        log_security_event(
            db=db,
            action="SHARE_DOWNLOAD_SUCCESS",
            resource_type="share",
            resource_id=str(share.id),
            result="SUCCESS",
            ip_address=client_ip,
            user_agent=user_agent,
            metadata={"filename": file.original_filename, "download_count": share.download_count}
        )

        return plaintext, file.original_filename, file.detected_mime
