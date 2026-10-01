import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserRole(str, enum.Enum):
    USER = "USER"
    STANDARD_USER = "STANDARD_USER"
    ADMIN = "ADMIN"
    SECURITY_AUDITOR = "SECURITY_AUDITOR"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STANDARD_USER, nullable=False)
    account_status = Column(String(32), default="ACTIVE", nullable=False)  # ACTIVE, SUSPENDED, DISABLED
    is_active = Column(Boolean, default=True, nullable=False)
    mfa_secret = Column(String(64), nullable=True)
    mfa_enabled = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    files = relationship("File", back_populates="owner", cascade="all, delete-orphan")
    shares = relationship("ShareLink", back_populates="creator", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="actor", foreign_keys="AuditLog.actor_id")
