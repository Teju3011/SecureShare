from typing import Generator, Optional
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.security.rbac import get_current_user, require_admin


def get_client_ip(request: Request) -> str:
    # Handle reverse proxy headers if present
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"


def get_user_agent(request: Request) -> str:
    return request.headers.get("user-agent", "Unknown-Agent")[:250]


__all__ = [
    "get_db",
    "get_current_user",
    "require_admin",
    "get_client_ip",
    "get_user_agent",
]
