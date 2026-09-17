# SECURESHARE
### Secure File Sharing Platform with Automated Security Validation
**Software Engineering + Cybersecurity Capstone Project**

---

## 🛡️ Project Overview

**SECURESHARE** is an enterprise-grade, zero-trust secure file sharing web platform that enforces automated multi-stage security validation on every uploaded file before permitting storage, download, or external distribution. It bridges software engineering best practices with core cyber defense principles:

- **Zero-Trust Security Enforcement**: Files are strictly isolated and never downloadable or shareable before achieving an explicit, validated `CLEAN` verdict.
- **Fail-Closed Malware Scanning**: Integrated ClamAV daemon inspection with an automated EICAR antivirus test harness. If scanner daemons are unreachable, files fail closed (`BLOCKED`/`FAILED`) and are never marked clean.
- **MIME & Magic-Byte Discrepancy Detection**: Deep binary inspection validates actual file headers against declared MIME types and extensions, catching MIME spoofing and disguised executables.
- **Dangerous Content Elimination**: Automated heuristics intercept Windows PE (`MZ`), Linux ELF, macOS Mach-O binaries, shell scripts, Windows batch files, PowerShell payloads, and macro-enabled documents (`.docm`, `.xlsm`, embedded VBA projects).
- **AES-256-GCM Storage Encryption**: All payloads are authenticated and encrypted at rest with unique 96-bit nonces before entering segregated `clean/` or `quarantine/` partitions.
- **Tamper-Evident Hash Chain Audit Trail**: Every authentication, upload, scan, quarantine, and download action is recorded into a cryptographically chained ledger where `entry_hash = SHA-256(previous_hash + payload)` with built-in mathematical tamper detection.
- **SOC Security Dashboard & DevSecOps Gate**: Real-time telemetry, threat charts, user role governance, quarantine management, and CI/CD security gate enforcement (blocking deployments on Critical SAST/SCA/DAST findings).

---

## 📋 Requirements Traceability Matrix

| Requirement | Description | Implementation Status | Core Module |
|---|---|---|---|
| **FR-01** | Authentication & MFA | ✅ Fully Implemented | `app/security/password.py`, `jwt.py`, `totp.py` |
| **FR-02** | Role-Based Access Control (RBAC) | ✅ Fully Implemented | `app/security/rbac.py`, `app/api/deps.py` |
| **FR-03** | File Upload (Max 50MB, SHA-256) | ✅ Fully Implemented | `app/scanners/pipeline.py`, `validator.py` |
| **FR-04** | MIME & Signature Validation | ✅ Fully Implemented | `app/scanners/validator.py` |
| **FR-05** | Automated Malware Scanning | ✅ Fully Implemented | `app/scanners/clamav.py` |
| **FR-06** | Dangerous Script & Binary Detection | ✅ Fully Implemented | `app/scanners/dangerous_file.py` |
| **FR-07** | Quarantine & Admin Release/Purge | ✅ Fully Implemented | `app/storage/`, `app/api/v1/admin.py` |
| **FR-08** | Expiring Password-Protected Shares | ✅ Fully Implemented | `app/services/share_service.py`, `shares.py` |
| **FR-09** | AES-256-GCM Encryption at Rest | ✅ Fully Implemented | `app/security/encryption.py` |
| **FR-10** | Tamper-Evident Audit Logging | ✅ Fully Implemented | `app/audit/logger.py`, `verifier.py` |
| **FR-11** | CI/CD DevSecOps & Security Gate | ✅ Fully Implemented | `.github/workflows/`, `scripts/run_security_pipeline.py` |
| **FR-12** | SOC Security Dashboard & Telemetry | ✅ Fully Implemented | `app/api/v1/admin.py`, `frontend/src/pages/admin/` |

---

## 🎯 Use Case Walkthroughs (SRS UC-1 to UC-7)

- **UC-1: Register & Login with MFA**
  Users register with strong password policy requirements (8+ chars, uppercase, lowercase, digit, symbol). Optional TOTP MFA setup presents a QR code and verifies 6-digit authenticator codes.
- **UC-2: Upload File through 6-Stage Security Pipeline**
  Users drop files up to 50 MB into the drag-and-drop zone. The real-time pipeline executes: Uploading -> Validating Size & Hash -> Checking Magic Bytes -> Dangerous Content Filter -> Antivirus/ClamAV -> AES-256-GCM Encryption.
- **UC-3: Share File Securely**
  Users configure expiration periods (1h to 7 days), optional access passwords (Argon2/bcrypt hashed), and download limits (e.g. burn-after-single-download). The server stores only a SHA-256 hash of the random share token.
- **UC-4: Download Shared File**
  Recipients open `/share/<token>`, view public metadata without exposing file contents, enter password if challenged, and stream decrypted file. Counter increments and download limit is strictly enforced.
- **UC-5: Review Quarantined Files**
  Administrators inspect isolated threats in the Quarantine Center, review scanner findings, and execute audited release or permanent purge.
- **UC-6: Trigger DevSecOps Security Scan**
  Administrators trigger CI/CD pipeline scans. If Critical findings occur (SAST/SCA/DAST), the automated Security Gate blocks deployment.
- **UC-7: View SOC Security Dashboard**
  Administrators monitor real-time threat telemetry, upload vs malware trends, severity breakdowns, user privileges, and audit hash chain integrity.

---

## 🏗️ Architecture & Security Data Flow

```
   Uploaded File
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Size & SHA-256 Hash Check (< 50 MB)                      │
└────────────────┬────────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. MIME & Magic-Byte Signature Inspection                   │
│    (Detects spoofed extensions & mismatched headers)        │
└────────────────┬────────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Dangerous File & Script Filter                           │
│    (PE/MZ, ELF, Mach-O, .bat, .ps1, .sh, VBA macros)        │
└────────────────┬────────────────────────────────────────────┘
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Antivirus & Malware Engine (ClamAV + EICAR Test Harness) │
│    (Fail-Closed: ClamAV offline keeps file blocked)         │
└────────────────┬────────────────────────────────────────────┘
                 ▼
          Security Decision
         ┌───────┴───────┐
         ▼               ▼
      [CLEAN]      [MALICIOUS / HIGH-RISK]
         │               │
         ▼               ▼
  AES-256 Encrypt  AES-256 Encrypt
         │               │
         ▼               ▼
  storage/clean/   storage/quarantine/
  (Available)      (Download Blocked)
         │               │
         └───────┬───────┘
                 ▼
   Tamper-Evident SHA-256 Audit Log
   entry_hash = HASH(prev_hash + event)
```

---

## 🔑 Pre-Seeded Demo Accounts

The database comes pre-seeded with realistic demonstration accounts:

| Role | Email | Password | Access Privileges |
|---|---|---|---|
| **Admin (SOC)** | `admin@secureshare.io` | `Admin@SecureShare2026!` | Full SOC Dashboard, Quarantine, Audit Verification, User RBAC |
| **Standard User** | `alice@example.com` | `User@SecureShare2026!` | File upload, downloads, personal shares, personal activity |
| **Standard User** | `bob@example.com` | `User@SecureShare2026!` | Uploads, personal shares |

*Tip: The UI features 1-click quick login buttons on the sign-in screen for instant grading and evaluation.*

---

## 🚀 Running Locally

### Option A: Standalone Local Development (No Docker Required)

#### 1. Backend Setup
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Run database seeder (initializes tables, demo users, verified audit chain)
python -m app.seed

# Start FastAPI backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation and Swagger UI will be live at: `http://127.0.0.1:8000/docs`

#### 2. Frontend Setup
In a second terminal:
```powershell
cd frontend
npm install
npm run dev
```
Open web application at: `http://localhost:5173`

---

### Option B: Docker Compose Deployment

To launch the complete multi-container stack (PostgreSQL, MinIO S3, ClamAV daemon, Backend, and Frontend):

```bash
docker compose up --build
```
- Frontend UI: `http://localhost:80`
- FastAPI REST API: `http://localhost:8000`
- MinIO Web Console: `http://localhost:9001` (User: `secureshare_minio_user`, Pass: `secureshare_minio_secret_password`)
- ClamAV Daemon: Port 3310

---

## 🧪 Automated Testing

Run the full pytest suite covering authentication, RBAC, file validation, quarantine, secure sharing, encryption at rest, and audit hash chain tamper detection:

```powershell
cd backend
.\venv\Scripts\pytest -v
```

All 18 tests execute in an isolated test database with zero external dependencies.

---

## 🛡️ DevSecOps Local Pipeline Execution

Execute the standalone DevSecOps security scanner script:

```powershell
python scripts/run_security_pipeline.py
```
This performs SAST rule checks, scans dependencies, tests security headers, and records a verified run directly into the Admin SOC dashboard.
