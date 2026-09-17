from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from app.core.config import settings

ALGORITHM = settings.ALGORITHM


def create_access_token(
    subject: str,
    role: str,
    email: str,
    mfa_verified: bool = True,
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "role": role,
        "email": email,
        "mfa_verified": mfa_verified,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_temp_mfa_token(user_id: int, email: str) -> str:
    """Creates a temporary short-lived token to complete MFA verification."""
    expire = datetime.utcnow() + timedelta(minutes=5)
    to_encode = {
        "sub": str(user_id),
        "email": email,
        "mfa_verified": False,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "mfa_pending"
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (jwt.PyJWTError, Exception):
        return None
