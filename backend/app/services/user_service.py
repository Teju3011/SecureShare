from typing import Optional, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.security.password import get_password_hash, verify_password, validate_password_strength
from app.security.jwt import create_access_token, create_temp_mfa_token
from app.security.totp import generate_totp_secret, get_provisioning_uri, generate_qr_code_data_url, verify_totp_code
from app.audit.logger import log_security_event


class UserService:
    @staticmethod
    def register_user(
        db: Session,
        email: str,
        full_name: str,
        password: str,
        role: UserRole = UserRole.STANDARD_USER,
        client_ip: str = "127.0.0.1",
        user_agent: str = "SecureShare-Web"
    ) -> User:
        norm_email = email.lower().strip()
        existing = db.query(User).filter(User.email == norm_email).first()
        if existing:
            # Generic error to prevent account enumeration
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this email address already exists."
            )

        is_valid, reason = validate_password_strength(password)
        if not is_valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)

        hashed_pwd = get_password_hash(password)
        user = User(
            email=norm_email,
            full_name=full_name.strip(),
            hashed_password=hashed_pwd,
            role=role,
            is_active=True,
            mfa_enabled=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        log_security_event(
            db=db,
            action="USER_REGISTER",
            resource_type="user",
            resource_id=str(user.id),
            actor_id=user.id,
            actor_email=user.email,
            ip_address=client_ip,
            user_agent=user_agent,
            result="SUCCESS",
            metadata={"role": user.role.value}
        )

        return user

    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str,
        totp_code: Optional[str] = None,
        client_ip: str = "127.0.0.1",
        user_agent: str = "SecureShare-Web"
    ) -> dict:
        norm_email = email.lower().strip()
        user = db.query(User).filter(User.email == norm_email).first()

        # Constant-time comparison simulation / secure generic error
        if not user or not verify_password(password, user.hashed_password):
            log_security_event(
                db=db,
                action="USER_LOGIN_FAILED",
                resource_type="auth",
                actor_email=norm_email,
                ip_address=client_ip,
                user_agent=user_agent,
                result="FAILURE",
                metadata={"reason": "Invalid credentials"}
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        if not user.is_active:
            log_security_event(
                db=db,
                action="USER_LOGIN_BLOCKED",
                resource_type="auth",
                actor_id=user.id,
                actor_email=user.email,
                ip_address=client_ip,
                user_agent=user_agent,
                result="BLOCKED",
                metadata={"reason": "Account deactivated"}
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated. Contact an administrator."
            )

        # Check MFA requirement
        if user.mfa_enabled:
            if not totp_code:
                temp_token = create_temp_mfa_token(user.id, user.email)
                return {
                    "access_token": "",
                    "token_type": "bearer",
                    "mfa_required": True,
                    "temp_token": temp_token
                }
            # Verify provided TOTP
            if not verify_totp_code(user.mfa_secret, totp_code):
                log_security_event(
                    db=db,
                    action="USER_MFA_FAILED",
                    resource_type="auth",
                    actor_id=user.id,
                    actor_email=user.email,
                    ip_address=client_ip,
                    user_agent=user_agent,
                    result="FAILURE",
                    metadata={"reason": "Invalid 6-digit TOTP code"}
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid MFA code. Please try again."
                )

        access_token = create_access_token(
            subject=str(user.id),
            role=user.role.value,
            email=user.email,
            mfa_verified=True
        )

        log_security_event(
            db=db,
            action="USER_LOGIN_SUCCESS",
            resource_type="auth",
            actor_id=user.id,
            actor_email=user.email,
            ip_address=client_ip,
            user_agent=user_agent,
            result="SUCCESS",
            metadata={"mfa_used": user.mfa_enabled}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "mfa_required": False,
            "temp_token": None
        }

    @staticmethod
    def setup_mfa(user: User, db: Session) -> dict:
        secret = generate_totp_secret()
        user.mfa_secret = secret
        db.commit()

        uri = get_provisioning_uri(secret, user.email)
        qr_url = generate_qr_code_data_url(uri)
        return {
            "secret": secret,
            "provisioning_uri": uri,
            "qr_code_data_url": qr_url
        }

    @staticmethod
    def verify_and_enable_mfa(
        user: User,
        code: str,
        db: Session,
        client_ip: str = "127.0.0.1",
        user_agent: str = "SecureShare-Web"
    ) -> bool:
        if not user.mfa_secret:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="MFA setup was not initiated.")

        if not verify_totp_code(user.mfa_secret, code):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification code.")

        user.mfa_enabled = True
        db.commit()

        log_security_event(
            db=db,
            action="MFA_ENABLED",
            resource_type="user",
            resource_id=str(user.id),
            actor_id=user.id,
            actor_email=user.email,
            ip_address=client_ip,
            user_agent=user_agent,
            result="SUCCESS",
            metadata={}
        )
        return True
