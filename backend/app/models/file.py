import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class FileStatus(str, enum.Enum):
    UPLOADING = "UPLOADING"
    VALIDATING = "VALIDATING"
    SCANNING = "SCANNING"
    CLEAN = "CLEAN"
    HIGH_RISK = "HIGH_RISK"
    MALICIOUS = "MALICIOUS"
    QUARANTINED = "QUARANTINED"
    FAILED = "FAILED"


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    folder_id = Column(Integer, ForeignKey("folders.id", ondelete="SET NULL"), nullable=True, index=True)
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False, unique=True, index=True)
    file_size = Column(BigInteger, nullable=False)
    declared_mime = Column(String(128), nullable=False)
    detected_mime = Column(String(128), nullable=False)
    magic_bytes_preview = Column(String(64), nullable=True)
    sha256_hash = Column(String(64), nullable=False, index=True)
    status = Column(Enum(FileStatus), default=FileStatus.UPLOADING, nullable=False, index=True)
    storage_path = Column(String(512), nullable=False)
    is_quarantined = Column(Boolean, default=False, nullable=False, index=True)
    quarantine_reason = Column(Text, nullable=True)
    encryption_status = Column(String(64), default="AES-256-GCM", nullable=False)
    encryption_iv = Column(String(64), nullable=False)  # 12-byte nonce hex for AES-256-GCM
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    owner = relationship("User", back_populates="files")
    folder = relationship("Folder", back_populates="files")
    versions = relationship("FileVersion", back_populates="file", cascade="all, delete-orphan")
    scan_results = relationship("ScanResult", back_populates="file", cascade="all, delete-orphan")
    share_links = relationship("ShareLink", back_populates="file", cascade="all, delete-orphan")


class FileVersion(Base):
    __tablename__ = "file_versions"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id", ondelete="CASCADE"), nullable=False, index=True)
    version_num = Column(Integer, default=1, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    sha256_hash = Column(String(64), nullable=False)
    storage_path = Column(String(512), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    file = relationship("File", back_populates="versions")
