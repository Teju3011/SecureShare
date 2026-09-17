import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class ScanStatus(str, enum.Enum):
    PASSED = "PASSED"
    MALICIOUS = "MALICIOUS"
    HIGH_RISK = "HIGH_RISK"
    FAILED = "FAILED"
    ERROR = "ERROR"


class ThreatLevel(str, enum.Enum):
    CLEAN = "CLEAN"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id", ondelete="CASCADE"), nullable=False, index=True)
    scanner_name = Column(String(100), nullable=False)
    scan_status = Column(Enum(ScanStatus), nullable=False)
    threat_level = Column(Enum(ThreatLevel), default=ThreatLevel.CLEAN, nullable=False)
    threat_name = Column(String(255), nullable=True)
    details = Column(Text, nullable=True)
    scanned_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    file = relationship("File", back_populates="scan_results")
