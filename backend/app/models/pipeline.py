import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class PipelineStatus(str, enum.Enum):
    RUNNING = "RUNNING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


class FindingSeverity(str, enum.Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Informational"


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id = Column(Integer, primary_key=True, index=True)
    commit_hash = Column(String(40), nullable=False)
    branch = Column(String(100), default="main", nullable=False)
    triggered_by = Column(String(255), nullable=False)
    status = Column(Enum(PipelineStatus), default=PipelineStatus.RUNNING, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    total_findings = Column(Integer, default=0, nullable=False)
    critical_count = Column(Integer, default=0, nullable=False)
    high_count = Column(Integer, default=0, nullable=False)
    medium_count = Column(Integer, default=0, nullable=False)
    low_count = Column(Integer, default=0, nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)

    findings = relationship("SecurityFinding", back_populates="pipeline_run", cascade="all, delete-orphan")


class SecurityFinding(Base):
    __tablename__ = "security_findings"

    id = Column(Integer, primary_key=True, index=True)
    pipeline_run_id = Column(Integer, ForeignKey("pipeline_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    tool_name = Column(String(50), nullable=False)  # Semgrep, pip-audit, npm-audit, OWASP ZAP
    severity = Column(Enum(FindingSeverity), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    file_path = Column(String(255), nullable=True)
    line_number = Column(Integer, nullable=True)
    cve_id = Column(String(64), nullable=True)
    status = Column(String(32), default="OPEN", nullable=False)  # OPEN, RESOLVED, SUPPRESSED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    pipeline_run = relationship("PipelineRun", back_populates="findings")
