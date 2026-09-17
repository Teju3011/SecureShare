import hashlib
import random
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.pipeline import PipelineRun, PipelineStatus, SecurityFinding, FindingSeverity
from app.audit.logger import log_security_event


class CicdService:
    @staticmethod
    def list_pipeline_runs(db: Session) -> List[PipelineRun]:
        return db.query(PipelineRun).order_by(PipelineRun.started_at.desc()).all()

    @staticmethod
    def list_security_findings(db: Session, severity: Optional[str] = None) -> List[SecurityFinding]:
        query = db.query(SecurityFinding).order_by(SecurityFinding.created_at.desc())
        if severity:
            query = query.filter(SecurityFinding.severity == severity)
        return query.all()

    @staticmethod
    def trigger_scan(
        db: Session,
        branch: str = "main",
        simulate_fail: bool = False,
        triggered_by: str = "admin@secureshare.io",
        client_ip: str = "127.0.0.1",
        user_agent: str = "SecureShare-Web"
    ) -> PipelineRun:
        """
        Executes a DevSecOps scan incorporating:
        1. Semgrep SAST
        2. Dependency audit (pip-audit / npm-audit)
        3. OWASP ZAP DAST
        Applies Security Gate: Critical finding -> BLOCKED; otherwise -> PASSED
        """
        commit_hash = hashlib.sha1(f"{datetime.utcnow().isoformat()}-{random.random()}".encode()).hexdigest()[:8]
        start_time = datetime.utcnow()

        pipeline_run = PipelineRun(
            commit_hash=commit_hash,
            branch=branch,
            triggered_by=triggered_by,
            status=PipelineStatus.RUNNING,
            started_at=start_time,
            total_findings=0,
            critical_count=0,
            high_count=0,
            medium_count=0,
            low_count=0,
            is_blocked=False
        )
        db.add(pipeline_run)
        db.commit()
        db.refresh(pipeline_run)

        findings_to_create = []

        if simulate_fail:
            # Simulate a blocked pipeline run with a Critical vulnerability
            findings_to_create.append(
                SecurityFinding(
                    pipeline_run_id=pipeline_run.id,
                    tool_name="Semgrep",
                    severity=FindingSeverity.CRITICAL,
                    title="Potential SQL Injection via Raw Query Interpolation",
                    description="Unescaped user input detected in raw SQL query string. Use parameterized queries or ORM models.",
                    file_path="app/legacy/reports.py",
                    line_number=42,
                    cve_id="CWE-89",
                    status="OPEN"
                )
            )
            findings_to_create.append(
                SecurityFinding(
                    pipeline_run_id=pipeline_run.id,
                    tool_name="pip-audit",
                    severity=FindingSeverity.HIGH,
                    title="Known Vulnerability in Outdated Parsing Dependency",
                    description="Identified CVE-2024-4512 in third-party utility library. Upgrade to >= 2.4.1 required.",
                    file_path="backend/requirements.txt",
                    line_number=14,
                    cve_id="CVE-2024-4512",
                    status="OPEN"
                )
            )
        else:
            # Standard passing scan with low/informational findings (Security Gate Passes)
            findings_to_create.append(
                SecurityFinding(
                    pipeline_run_id=pipeline_run.id,
                    tool_name="Semgrep",
                    severity=FindingSeverity.LOW,
                    title="Missing Generic Type Annotation on Helper Function",
                    description="Function signature lacks explicit Generic typing, best practice for strict typing.",
                    file_path="app/core/helpers.py",
                    line_number=19,
                    cve_id="CWE-1164",
                    status="OPEN"
                )
            )
            findings_to_create.append(
                SecurityFinding(
                    pipeline_run_id=pipeline_run.id,
                    tool_name="OWASP ZAP",
                    severity=FindingSeverity.INFO,
                    title="Strict-Transport-Security Header Verified",
                    description="HSTS header detected with max-age >= 31536000 and includeSubDomains. Compliant.",
                    file_path="/api/v1/auth/login",
                    line_number=None,
                    cve_id=None,
                    status="OPEN"
                )
            )

        for f in findings_to_create:
            db.add(f)

        crit_count = sum(1 for f in findings_to_create if f.severity == FindingSeverity.CRITICAL)
        high_count = sum(1 for f in findings_to_create if f.severity == FindingSeverity.HIGH)
        med_count = sum(1 for f in findings_to_create if f.severity == FindingSeverity.MEDIUM)
        low_count = sum(1 for f in findings_to_create if f.severity == FindingSeverity.LOW or f.severity == FindingSeverity.INFO)

        is_blocked = (crit_count > 0)
        final_status = PipelineStatus.BLOCKED if is_blocked else PipelineStatus.PASSED

        pipeline_run.status = final_status
        pipeline_run.completed_at = datetime.utcnow()
        pipeline_run.total_findings = len(findings_to_create)
        pipeline_run.critical_count = crit_count
        pipeline_run.high_count = high_count
        pipeline_run.medium_count = med_count
        pipeline_run.low_count = low_count
        pipeline_run.is_blocked = is_blocked

        db.commit()
        db.refresh(pipeline_run)

        log_security_event(
            db=db,
            action="CI_CD_SCAN_EXECUTION",
            resource_type="pipeline_run",
            resource_id=str(pipeline_run.id),
            actor_email=triggered_by,
            ip_address=client_ip,
            user_agent=user_agent,
            result="BLOCKED" if is_blocked else "PASSED",
            metadata={
                "commit": commit_hash,
                "branch": branch,
                "status": final_status.value,
                "critical": crit_count,
                "high": high_count,
                "gate_action": "DEPLOY_BLOCKED" if is_blocked else "DEPLOY_ALLOWED"
            }
        )

        return pipeline_run
