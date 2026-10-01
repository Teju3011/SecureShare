import os
import sys
import hashlib
from datetime import datetime, timedelta

# Ensure backend directory is in pythonpath
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.folder import Folder
from app.models.file import File, FileStatus
from app.models.permission import Permission
from app.models.login_attempt import LoginAttempt
from app.models.scan import ScanResult, ScanStatus, ThreatLevel
from app.models.share import ShareLink
from app.models.audit import AuditLog
from app.models.pipeline import PipelineRun, PipelineStatus, SecurityFinding, FindingSeverity
from app.security.password import get_password_hash
from app.security.encryption import file_encryptor
from app.scanners.clamav import EICAR_SIGNATURE
from app.storage import storage
from app.audit.logger import log_security_event


def seed_database():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded with sushmitha
        existing_sushmitha = db.query(User).filter(User.email == "sushmitha@example.com").first()
        if existing_sushmitha:
            print("Database already contains required demo seed data. Skipping creation.")
            return

        print("Seeding Users (Admin, Auditor, Demo Personas: Sushmitha, Rahul, Priya, Arjun, Alice, Bob)...")
        # 1 Admin
        admin = User(
            email="admin@secureshare.io",
            full_name="Chief Security Officer (Admin)",
            hashed_password=get_password_hash("Admin@SecureShare2026!"),
            role=UserRole.ADMIN,
            account_status="ACTIVE",
            is_active=True,
            mfa_enabled=False
        )
        db.add(admin)

        # 1 Security Auditor
        auditor = User(
            email="auditor@secureshare.io",
            full_name="Security Compliance Auditor",
            hashed_password=get_password_hash("Auditor@SecureShare2026!"),
            role=UserRole.SECURITY_AUDITOR,
            account_status="ACTIVE",
            is_active=True,
            mfa_enabled=False
        )
        db.add(auditor)

        # Demo Users specified in Section 51
        sushmitha = User(
            email="sushmitha@example.com",
            full_name="Sushmitha Reddy",
            hashed_password=get_password_hash("User@SecureShare2026!"),
            role=UserRole.USER,
            account_status="ACTIVE",
            is_active=True,
            mfa_enabled=False
        )
        rahul = User(
            email="rahul@example.com",
            full_name="Rahul Kumar",
            hashed_password=get_password_hash("User@SecureShare2026!"),
            role=UserRole.USER,
            account_status="ACTIVE",
            is_active=True,
            mfa_enabled=False
        )
        priya = User(
            email="priya@example.com",
            full_name="Priya Sharma",
            hashed_password=get_password_hash("User@SecureShare2026!"),
            role=UserRole.USER,
            account_status="ACTIVE",
            is_active=True,
            mfa_enabled=False
        )
        arjun = User(
            email="arjun@example.com",
            full_name="Arjun Rao",
            hashed_password=get_password_hash("User@SecureShare2026!"),
            role=UserRole.USER,
            account_status="ACTIVE",
            is_active=True,
            mfa_enabled=False
        )

        # Backward compatibility for existing automated tests
        alice = User(
            email="alice@example.com",
            full_name="Alice Senior Developer",
            hashed_password=get_password_hash("User@SecureShare2026!"),
            role=UserRole.USER,
            account_status="ACTIVE",
            is_active=True,
            mfa_enabled=False
        )
        bob = User(
            email="bob@example.com",
            full_name="Bob Systems Analyst",
            hashed_password=get_password_hash("User@SecureShare2026!"),
            role=UserRole.USER,
            account_status="ACTIVE",
            is_active=True,
            mfa_enabled=False
        )
        tester = User(
            email="security.tester@example.com",
            full_name="Security Auditor (PenTester)",
            hashed_password=get_password_hash("User@SecureShare2026!"),
            role=UserRole.USER,
            account_status="ACTIVE",
            is_active=True,
            mfa_enabled=False
        )

        db.add_all([sushmitha, rahul, priya, arjun, alice, bob, tester])
        db.commit()
        db.refresh(admin)
        db.refresh(auditor)
        db.refresh(sushmitha)
        db.refresh(rahul)
        db.refresh(priya)
        db.refresh(arjun)
        db.refresh(alice)
        db.refresh(bob)
        db.refresh(tester)

        print("Seeding Audit Log Genesis & User Provisioning...")
        log_security_event(
            db=db,
            action="SYSTEM_INITIALIZE",
            resource_type="system",
            resource_id="1",
            actor_email="system@secureshare.local",
            result="SUCCESS",
            metadata={"environment": "production-hardened", "version": "2.0.0", "standard": "IEEE 29148"}
        )

        log_security_event(
            db=db,
            action="USER_PROVISIONED",
            resource_type="user",
            resource_id=str(sushmitha.id),
            actor_email="admin@secureshare.io",
            result="SUCCESS",
            metadata={"role": "USER", "email": sushmitha.email, "name": sushmitha.full_name}
        )

        # Seed Folders for Sushmitha (Section 51)
        print("Seeding Folders (Project Documents, Research, Reports)...")
        folder_proj = Folder(owner_id=sushmitha.id, folder_name="Project Documents")
        folder_research = Folder(owner_id=sushmitha.id, folder_name="Research")
        folder_reports = Folder(owner_id=sushmitha.id, folder_name="Reports")
        db.add_all([folder_proj, folder_research, folder_reports])
        db.commit()
        db.refresh(folder_proj)
        db.refresh(folder_research)
        db.refresh(folder_reports)

        print("Seeding Files & Security Validation Pipeline...")
        # 1. Security_Report.pdf (Sushmitha -> Reports)
        sec_report_bytes = b"%PDF-1.5\n%SecureShare Security Audit Report 2026\n1 0 obj\n<< /Title (SecureShare Security Audit) >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
        sec_iv, sec_enc = file_encryptor.encrypt(sec_report_bytes)
        sec_stored = f"sec_report_{sushmitha.id}.pdf"
        sec_path = storage.save_file(sec_stored, sec_enc, is_quarantined=False)
        sec_hash = hashlib.sha256(sec_report_bytes).hexdigest()

        f_sec_report = File(
            user_id=sushmitha.id,
            folder_id=folder_reports.id,
            original_filename="Security_Report.pdf",
            stored_filename=sec_stored,
            file_size=len(sec_report_bytes),
            declared_mime="application/pdf",
            detected_mime="application/pdf",
            magic_bytes_preview="255044462D312E35",
            sha256_hash=sec_hash,
            status=FileStatus.CLEAN,
            storage_path=sec_path,
            is_quarantined=False,
            encryption_status="AES-256-GCM",
            encryption_iv=sec_iv,
        )
        db.add(f_sec_report)
        db.commit()
        db.refresh(f_sec_report)

        db.add_all([
            ScanResult(
                file_id=f_sec_report.id,
                scanner_name="mime_signature_validator",
                scan_status=ScanStatus.PASSED,
                threat_level=ThreatLevel.CLEAN,
                details="Magic bytes match application/pdf header (%PDF)."
            ),
            ScanResult(
                file_id=f_sec_report.id,
                scanner_name="dangerous_file_detector",
                scan_status=ScanStatus.PASSED,
                threat_level=ThreatLevel.CLEAN,
                details="No executable PE/ELF binaries or macro instructions detected."
            ),
            ScanResult(
                file_id=f_sec_report.id,
                scanner_name="clamav_scanner",
                scan_status=ScanStatus.PASSED,
                threat_level=ThreatLevel.CLEAN,
                details="ClamAV Antivirus: Zero signatures matched. Payload verified clean."
            )
        ])
        db.commit()

        # 2. SecureShare_SRS.docx (Sushmitha -> Project Documents)
        srs_bytes = b"PK\x03\x04\x14\x00\x06\x00SecureShare SRS Conforming to IEEE 29148 Standard [Content_Types].xml"
        srs_iv, srs_enc = file_encryptor.encrypt(srs_bytes)
        srs_stored = f"srs_doc_{sushmitha.id}.docx"
        srs_path = storage.save_file(srs_stored, srs_enc, is_quarantined=False)
        srs_hash = hashlib.sha256(srs_bytes).hexdigest()

        f_srs = File(
            user_id=sushmitha.id,
            folder_id=folder_proj.id,
            original_filename="SecureShare_SRS.docx",
            stored_filename=srs_stored,
            file_size=len(srs_bytes),
            declared_mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            detected_mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            magic_bytes_preview="504B030414000600",
            sha256_hash=srs_hash,
            status=FileStatus.CLEAN,
            storage_path=srs_path,
            is_quarantined=False,
            encryption_status="AES-256-GCM",
            encryption_iv=srs_iv,
        )
        db.add(f_srs)

        # 3. Project_Presentation.pptx (Sushmitha -> Project Documents)
        ppt_bytes = b"PK\x03\x04\x14\x00\x06\x00SecureShare Capstone Defense Presentation Slides"
        ppt_iv, ppt_enc = file_encryptor.encrypt(ppt_bytes)
        ppt_stored = f"proj_pres_{sushmitha.id}.pptx"
        ppt_path = storage.save_file(ppt_stored, ppt_enc, is_quarantined=False)
        ppt_hash = hashlib.sha256(ppt_bytes).hexdigest()

        f_ppt = File(
            user_id=sushmitha.id,
            folder_id=folder_proj.id,
            original_filename="Project_Presentation.pptx",
            stored_filename=ppt_stored,
            file_size=len(ppt_bytes),
            declared_mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            detected_mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            magic_bytes_preview="504B030414000600",
            sha256_hash=ppt_hash,
            status=FileStatus.CLEAN,
            storage_path=ppt_path,
            is_quarantined=False,
            encryption_status="AES-256-GCM",
            encryption_iv=ppt_iv,
        )
        db.add(f_ppt)

        # 4. AuthzGraph_Paper.pdf (Sushmitha -> Research)
        paper_bytes = b"%PDF-1.4\nAuthzGraph: Fine-Grained Object Authorization Research Paper\n%%EOF"
        paper_iv, paper_enc = file_encryptor.encrypt(paper_bytes)
        paper_stored = f"authz_paper_{sushmitha.id}.pdf"
        paper_path = storage.save_file(paper_stored, paper_enc, is_quarantined=False)
        paper_hash = hashlib.sha256(paper_bytes).hexdigest()

        f_paper = File(
            user_id=sushmitha.id,
            folder_id=folder_research.id,
            original_filename="AuthzGraph_Paper.pdf",
            stored_filename=paper_stored,
            file_size=len(paper_bytes),
            declared_mime="application/pdf",
            detected_mime="application/pdf",
            magic_bytes_preview="255044462D312E34",
            sha256_hash=paper_hash,
            status=FileStatus.CLEAN,
            storage_path=paper_path,
            is_quarantined=False,
            encryption_status="AES-256-GCM",
            encryption_iv=paper_iv,
        )
        db.add(f_paper)

        # 5. Network_Security_Notes.pdf (Sushmitha -> Research)
        notes_bytes = b"%PDF-1.4\nNetwork Security Notes: Zero-Trust and Cryptographic Hash Chaining\n%%EOF"
        notes_iv, notes_enc = file_encryptor.encrypt(notes_bytes)
        notes_stored = f"net_notes_{sushmitha.id}.pdf"
        notes_path = storage.save_file(notes_stored, notes_enc, is_quarantined=False)
        notes_hash = hashlib.sha256(notes_bytes).hexdigest()

        f_notes = File(
            user_id=sushmitha.id,
            folder_id=folder_research.id,
            original_filename="Network_Security_Notes.pdf",
            stored_filename=notes_stored,
            file_size=len(notes_bytes),
            declared_mime="application/pdf",
            detected_mime="application/pdf",
            magic_bytes_preview="255044462D312E34",
            sha256_hash=notes_hash,
            status=FileStatus.CLEAN,
            storage_path=notes_path,
            is_quarantined=False,
            encryption_status="AES-256-GCM",
            encryption_iv=notes_iv,
        )
        db.add(f_notes)
        db.commit()

        # Seed Permission: Sushmitha grants Rahul Kumar View + Download permission on Security_Report.pdf (Section 52)
        perm = Permission(
            file_id=f_sec_report.id,
            user_id=rahul.id,
            can_view=True,
            can_download=True,
            can_edit=False,
            can_share=False,
            role_preset="DOWNLOADER"
        )
        db.add(perm)
        db.commit()

        log_security_event(
            db=db,
            action="PERMISSION_GRANTED",
            resource_type="file",
            resource_id=str(f_sec_report.id),
            actor_id=sushmitha.id,
            actor_email=sushmitha.email,
            result="SUCCESS",
            metadata={"grantee": rahul.email, "preset": "DOWNLOADER", "file": f_sec_report.original_filename}
        )

        # Quarantined EICAR Malware Test File
        eicar_iv, eicar_encrypted = file_encryptor.encrypt(EICAR_SIGNATURE)
        eicar_stored_name = f"seed_quarantine_eicar_{tester.id}.com"
        eicar_path = storage.save_file(eicar_stored_name, eicar_encrypted, is_quarantined=True)

        eicar_file = File(
            user_id=tester.id,
            original_filename="eicar_test_virus_sample.com",
            stored_filename=eicar_stored_name,
            file_size=len(EICAR_SIGNATURE),
            declared_mime="application/x-dosexec",
            detected_mime="application/x-dosexec",
            magic_bytes_preview="58354F2150254041",
            sha256_hash="275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
            status=FileStatus.MALICIOUS,
            storage_path=eicar_path,
            is_quarantined=True,
            quarantine_reason="Malware detected: EICAR-Test-Signature (Standard Antivirus Test File signature detected.)",
            encryption_status="AES-256-GCM",
            encryption_iv=eicar_iv,
        )
        db.add(eicar_file)
        db.commit()
        db.refresh(eicar_file)

        db.add_all([
            ScanResult(
                file_id=eicar_file.id,
                scanner_name="dangerous_file_detector",
                scan_status=ScanStatus.HIGH_RISK,
                threat_level=ThreatLevel.HIGH,
                threat_name="DANGEROUS_EXTENSION",
                details="Disallowed executable file extension (.com)."
            ),
            ScanResult(
                file_id=eicar_file.id,
                scanner_name="clamav_scanner",
                scan_status=ScanStatus.MALICIOUS,
                threat_level=ThreatLevel.CRITICAL,
                threat_name="EICAR-Test-Signature",
                details="Standard Antivirus Test File signature detected."
            )
        ])
        db.commit()

        log_security_event(
            db=db,
            action="MALWARE_DETECTED_QUARANTINE",
            resource_type="file",
            resource_id=str(eicar_file.id),
            actor_id=tester.id,
            actor_email=tester.email,
            result="QUARANTINE",
            metadata={"threat": "EICAR-Test-Signature", "filename": eicar_file.original_filename}
        )

        # Seed Login Attempts
        db.add_all([
            LoginAttempt(
                user_id=sushmitha.id,
                email="sushmitha@example.com",
                ip_address="192.168.1.100",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                success=True,
                timestamp=datetime.utcnow() - timedelta(minutes=45)
            ),
            LoginAttempt(
                user_id=None,
                email="attacker@malicious.xyz",
                ip_address="203.0.113.45",
                user_agent="python-requests/2.28.1",
                success=False,
                failure_reason="Invalid credentials or non-existent user",
                timestamp=datetime.utcnow() - timedelta(minutes=15)
            )
        ])
        db.commit()

        # Seed Share Link
        demo_token = "secureshare_demo_token_77a9c2"
        demo_token_hash = hashlib.sha256(demo_token.encode("utf-8")).hexdigest()
        demo_share = ShareLink(
            file_id=f_sec_report.id,
            user_id=sushmitha.id,
            token_hash=demo_token_hash,
            password_hash=get_password_hash("SharePass123!"),
            expires_at=datetime.utcnow() + timedelta(days=7),
            max_downloads=5,
            download_count=1,
            is_active=True
        )
        db.add(demo_share)
        db.commit()

        # DevSecOps Pipeline Runs
        blocked_run = PipelineRun(
            commit_hash="a1c4e9b",
            branch="feature/file-compression",
            triggered_by="sushmitha@example.com",
            status=PipelineStatus.BLOCKED,
            started_at=datetime.utcnow() - timedelta(hours=5),
            completed_at=datetime.utcnow() - timedelta(hours=4, minutes=58),
            total_findings=3,
            critical_count=1,
            high_count=1,
            medium_count=1,
            low_count=0,
            is_blocked=True
        )
        db.add(blocked_run)
        db.commit()
        db.refresh(blocked_run)

        db.add_all([
            SecurityFinding(
                pipeline_run_id=blocked_run.id,
                tool_name="Semgrep",
                severity=FindingSeverity.CRITICAL,
                title="CWE-89: Raw SQL Query String Concatenation",
                description="Detected user input concatenated directly into raw database query string in backend/reports/export.py:84. Security Gate blocked deployment.",
                file_path="backend/reports/export.py",
                line_number=84,
                cve_id="CWE-89",
                status="OPEN"
            ),
            SecurityFinding(
                pipeline_run_id=blocked_run.id,
                tool_name="pip-audit",
                severity=FindingSeverity.HIGH,
                title="CVE-2024-4200: Vulnerable Dependency in Archive Helper",
                description="High severity tar archive path traversal vulnerability discovered in sub-dependency archive-extractor 0.8.2.",
                file_path="backend/requirements.txt",
                line_number=22,
                cve_id="CVE-2024-4200",
                status="OPEN"
            ),
            SecurityFinding(
                pipeline_run_id=blocked_run.id,
                tool_name="OWASP ZAP",
                severity=FindingSeverity.MEDIUM,
                title="Missing Anti-Clickjacking Frame Option on Legacy Route",
                description="Route /legacy/ping returned response without X-Frame-Options or CSP frame-ancestors header.",
                file_path="/legacy/ping",
                line_number=None,
                cve_id=None,
                status="OPEN"
            ),
        ])

        passed_run = PipelineRun(
            commit_hash="3f9b802",
            branch="main",
            triggered_by="admin@secureshare.io",
            status=PipelineStatus.PASSED,
            started_at=datetime.utcnow() - timedelta(hours=1),
            completed_at=datetime.utcnow() - timedelta(minutes=57),
            total_findings=2,
            critical_count=0,
            high_count=0,
            medium_count=0,
            low_count=2,
            is_blocked=False
        )
        db.add(passed_run)
        db.commit()
        db.refresh(passed_run)

        db.add_all([
            SecurityFinding(
                pipeline_run_id=passed_run.id,
                tool_name="Semgrep",
                severity=FindingSeverity.LOW,
                title="Maintainability: Undocumented Public Function",
                description="Function check_status lacks a descriptive docstring.",
                file_path="app/core/helpers.py",
                line_number=12,
                cve_id="CWE-1164",
                status="OPEN"
            ),
            SecurityFinding(
                pipeline_run_id=passed_run.id,
                tool_name="OWASP ZAP",
                severity=FindingSeverity.INFO,
                title="Security Headers Fully Compliant",
                description="All response headers passed validation: HSTS, CSP, nosniff, and frame-ancestors verified.",
                file_path="/api/v1/auth/login",
                line_number=None,
                cve_id=None,
                status="OPEN"
            ),
        ])
        db.commit()

        print("Seed completed successfully!")
        print(f"Admin: admin@secureshare.io / Admin@SecureShare2026!")
        print(f"Auditor: auditor@secureshare.io / Auditor@SecureShare2026!")
        print(f"Sushmitha: sushmitha@example.com / User@SecureShare2026!")
        print(f"Rahul: rahul@example.com / User@SecureShare2026!")
        print(f"Demo Share Token: {demo_token} (Password: SharePass123!)")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
