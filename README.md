# SECURESHARE — Secure File Sharing with Continuous Security Validation
### College Cybersecurity & Software Engineering Capstone Project
**Engineered in Strict Conformance with IEEE 29148 Standard for Requirements Engineering**

---

## 🛡️ Executive Summary

**SecureShare** is an enterprise-grade cloud-native web platform that allows users to securely upload, organize, download, and share confidential documents while the platform continuously defends against cyber threats. Every uploaded file undergoes a deterministic **6-stage threat inspection pipeline** before entering **AES-256-GCM envelope encryption** at rest. All application actions are cryptographically sealed into an **immutable SHA-256 blockchain audit ledger** with automated tamper detection. The application's own software lifecycle is guarded by an automated **14-stage DevSecOps CI/CD security gate** incorporating SAST, SCA, Secret Scanning, DAST, and fuzz testing.

---

## ⚡ 1-Click Demo Quick Start (Windows)

The repository includes pre-configured automation scripts to launch the complete stack with seeded demo data in under 10 seconds:

```cmd
:: 1. Start backend, frontend, seed database, and open live presentation dashboard:
START_DEMO.bat

:: 2. Stop running backend and frontend services:
STOP_DEMO.bat

:: 3. Reset database and storage partitions to pristine clean state:
RESET_DEMO.bat
```

### Direct Service URLs
- **Live Presentation & Metrics Dashboard**: [http://localhost:5173/demo](http://localhost:5173/demo)
- **Web Application Portal**: [http://localhost:5173](http://localhost:5173)
- **Interactive OpenAPI / Swagger Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Admin SOC Command Center**: [http://localhost:5173/admin](http://localhost:5173/admin)

---

## 👥 Evaluation Personas & Demo Accounts

All pre-seeded accounts use the universal demonstration password: `Pass123!Secure`

| Persona Name | Email Address | System Role | Primary Responsibilities & Review Focus |
| :--- | :--- | :--- | :--- |
| **Sushmitha Reddy** | `sushmitha@example.com` | `USER` | **Product Owner & Security Lead**: Uploads, file organization, share link generation. |
| **Rahul Kumar** | `rahul@example.com` | `USER` | **Cryptography & Backend Engineer**: File encryption, streaming decrypt, access control. |
| **Priya Sharma** | `priya@example.com` | `USER` | **DevSecOps & QA Lead**: 6-stage malware scanner, CI/CD pipeline, security testing. |
| **Arjun Rao** | `arjun@example.com` | `USER` | **UI/UX & Frontend Engineer**: Glassmorphism UI, permissions modal, activity view. |
| **System Admin** | `admin@example.com` | `ADMIN` | **SOC Operations**: Quarantine isolation center, purge malware, live telemetry. |
| **Security Auditor** | `auditor@example.com` | `SECURITY_AUDITOR` | **Compliance Officer**: SHA-256 blockchain audit verification, governance reports. |

---

## 📋 Requirements Traceability Matrix (IEEE 29148)

### Functional Requirements (FR-01 to FR-13)
- **FR-01**: User Registration with Argon2id memory-hard hashing (`m=64MB, t=3, p=4`) & password complexity policy.
- **FR-02**: JWT session authentication with 60-minute lifetime and sliding window refresh tokens.
- **FR-03**: RFC 6238 Time-based One-Time Password (TOTP) Multi-Factor Authentication with QR setup.
- **FR-04**: Direct multi-format file upload with 50MB ceiling and MIME verification.
- **FR-05**: Automated 6-stage malware, macro, and entropy threat scanning engine.
- **FR-06**: File quarantine isolation air-gap preventing download of suspicious/infected files.
- **FR-07**: Envelope encryption using AES-256-GCM authenticated cipher with 96-bit unique IVs.
- **FR-08**: Authorized decryption-on-the-fly streaming download with zero temporary disk files.
- **FR-09**: Hierarchical folder management with strict BOLA (Broken Object Level Authorization) guards.
- **FR-10**: Granular user-to-user permission sharing (`VIEWER`, `DOWNLOADER`, `EDITOR`, `CO_OWNER`).
- **FR-11**: Expiring public share links with optional Argon2id passwords and max download limits.
- **FR-12**: Tamper-evident SHA-256 blockchain audit logging with continuous verifier API.
- **FR-13**: Real-time SOC Administrator and Auditor Security Dashboard with live attack telemetry.

### Security Requirements (SR-01 to SR-15)
- **SR-01**: BOLA / IDOR protection through relational database ownership join queries.
- **SR-02**: Zero plaintext credentials or cryptographic keys stored in persistent database.
- **SR-03**: Strict Content-Security-Policy (`CSP`), anti-clickjacking (`X-Frame-Options: DENY`), and `HSTS`.
- **SR-04**: Sliding-window IP and account rate limiting (5 req/min on auth, 60 req/min on API).
- **SR-05**: Immutable audit log ledger detecting row deletions, insertions, or alterations.
- **SR-06**: Automatic 15-minute account lockout after 5 consecutive failed login attempts.
- **SR-07**: Complete file quarantine air-gap (quarantined files return HTTP 403 Forbidden).
- **SR-08**: Strict Role-Based Access Control (`ADMIN`, `SECURITY_AUDITOR`, `USER`).
- **SR-09**: Automated SAST and secret scanning quality gate in CI/CD pipeline.
- **SR-10**: Containerized microservice sandboxing executing under non-root UID 10001.
- **SR-11**: Deep magic-byte MIME detection independent of user-supplied file extensions.
- **SR-12**: Cryptographic IV randomization (`os.urandom(12)`) guaranteeing zero IV reuse.
- **SR-13**: Secure public share link password hashing with unique salts.
- **SR-14**: OWASP ZAP automated baseline DAST vulnerability scanning compliance.
- **SR-15**: High fuzzing resistance against 500+ malformed input vectors with zero unhandled crashes.

---

## 🔍 The 6-Stage Upload Threat Scanner Engine

```
Uploaded File Byte Stream
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 1: File Size Ceiling Check (< 50 MB hard limit)       │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 2: Deep MIME & Magic Byte Inspection (libmagic)       │
│          Catches disguised executables and extension spoofing│
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 3: Executable Binary & Script Header Filter           │
│          Blocks PE (MZ), ELF, Mach-O, .bat, .ps1, .sh, VBA   │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 4: Archive Ratio & Zip Bomb Detection Engine          │
│          Inspects uncompressed size & nested archive levels │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 5: ClamAV Daemon Antivirus Signature Scanner          │
│          Detects trojans, viruses, worms & EICAR test string│
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 6: Shannon Byte Entropy Analysis Engine               │
│          Calculates byte randomness to detect packed trojans│
└─────────────────────────────┬───────────────────────────────┘
                              ▼
                      Security Decision
                     ┌────────┴────────┐
                     ▼                 ▼
                  [CLEAN]         [INFECTED]
                     │                 │
                     ▼                 ▼
              AES-256-GCM       Quarantine Vault
            Envelope Encrypt    (/storage/quarantine)
                     │                 │
                     ▼                 ▼
              /storage/uploads    Download Air-Gap
             (Ready for access)   (HTTP 403 Forbidden)
```

---

## 🔄 14-Stage DevSecOps CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/secure-pipeline.yml`) executes 14 automated security gates:

1. **Code Linting & Formatting**: Flake8 & Black code quality enforcement.
2. **Backend Unit & Integration Tests**: Pytest core test suites.
3. **Security Mitigation Tests**: 11 dedicated security suites (BOLA, Crypto, Auth, RBAC).
4. **Malformed Input Fuzzing**: 500+ malformed payloads tested against endpoints.
5. **SAST (Bandit)**: Python static security analysis (SARIF output).
6. **SAST (Semgrep)**: OWASP Top 10 and security-audit rule scanning.
7. **Secret Scanning (TruffleHog)**: High-entropy credential and private key detection.
8. **SCA Backend (pip-audit & Safety)**: Python dependencies CVE vulnerability audit.
9. **SCA Frontend (npm audit)**: Node.js dependency vulnerability scan.
10. **Frontend Build & TypeCheck**: React 18 TypeScript compilation check.
11. **Container Security (Trivy)**: Docker image vulnerability scanning.
12. **DAST (OWASP ZAP)**: Baseline dynamic application security scan.
13. **Security Quality Gate**: Enforces zero High/Critical unmitigated findings.
14. **Artifacts Archival**: Uploads SARIF reports and compliance evidence.

---

## 📊 Project Deliverables & Artifacts Index

All project deliverables are located in their respective directories:

### 1. Excel Spreadsheets (`artifacts/excel/`)
- `Requirements_Traceability.xlsx`: IEEE 29148 RTM linking FR-01..13 & SR-01..15 to test cases.
- `Assets_CIA.xlsx`: CIA classification matrix for all 10 system assets.
- `STRIDE_Threat_Matrix.xlsx`: STRIDE threat model with mitigations and residual ratings.
- `Information_Flow.xlsx`: Data flow and trust boundary traversal matrix.
- `Vulnerability_Analysis.xlsx`: CWE, OWASP Top 10, and CVSS v3.1 scoring for V-01..12.
- `Threat_Risk_Register.xlsx`: Risk register with dynamic formulas and **5x5 Risk Heat Map** worksheet.
- `Security_Controls.xlsx`: NIST SP 800-53 and ISO 27001 mappings for SC-01..15.
- `Permission_Matrix.xlsx`: RBAC and DAC granular permission sharing matrices.
- `Product_Backlog.xlsx`: 18 Jira user stories with story points and sprint allocations.
- `Security_Test_Cases.xlsx`: 28 security test case specifications (SEC-TC-01..28).
- `Burndown_Data.xlsx`: Sprints 1, 2, and 3 burndown metrics and tracking.
- `Velocity_Data.xlsx`: Sprint velocity metrics showing 100% commitment delivery.
- `Risk_Governance.xlsx`: Enterprise risk governance and compliance framework.
- `Compliance_Mapping.xlsx`: Cross-regulatory mapping to OWASP, NIST CSF, ISO 27001, and GDPR.

### 2. Architecture Diagrams (`artifacts/diagrams/`)
- `Use_Case_Diagram` (`.drawio`, `.svg`, `.png`)
- `ER_Diagram` (`.drawio`, `.svg`, `.png`)
- `DFD_Level_0` (`.drawio`, `.svg`, `.png`)
- `DFD_Level_1` (`.drawio`, `.svg`, `.png`)
- `Trust_Boundary_Architecture` (`.drawio`, `.svg`, `.png`)
- `Attack_Tree` (`.drawio`, `.svg`, `.png`)
- `Secure_Architecture` (`.drawio`, `.svg`, `.png`)
- `Risk_Heat_Map.png` (Matplotlib rendered 5x5 heatmap)
- `Burndown_Chart.png` (Sprints 1, 2, 3 burndown curves)
- `Velocity_Chart.png` (Team velocity bar chart)
- `Sprint_Board.png` (Jira Scrum board graphic)

### 3. IEEE Documentation (`docs/SRS/` and `docs/`)
- `docs/SRS/SecureShare_SRS.docx` & `.pdf`: Full 20-clause IEEE 29148 Specification.
- `docs/Use_Case_Specifications.docx` & `.pdf`: Detailed specifications for UC-01 through UC-12.
- `docs/SecureShare_Final_Project_Report.docx` & `.pdf`: 46-section Academic Capstone Report.
- `artifacts/ui/UI_Design_Specification.pdf`: Complete UI/UX design tokens and component specs.

### 4. Jira Scrum Artifacts (`artifacts/jira/`)
- `jira_import.csv`: Standard Jira issue import file.
- `product_backlog.csv`: Full backlog with epics and story points.
- `sprint_1.csv`, `sprint_2.csv`, `sprint_3.csv`: Sprint backlogs.
- `bug_report.csv`: Tracked security defects and resolutions.

### 5. Kubernetes Production Manifests (`k8s/`)
- `namespace.yaml`, `configmap.yaml`, `secret.example.yaml`, `network-policy.yaml`, `ingress.yaml`, `hpa.yaml`.
- Deployments & Services for `postgres`, `clamav`, `backend`, and `frontend`.

---

## 🧪 Running Automated Tests

To execute the entire 48-test automated testing suite:

```powershell
# Run backend unit, security, and fuzzing suites:
backend\venv\Scripts\pytest -v tests/security security/fuzzing backend/tests
```

**Results**: 48 passed, 0 failed (100% pass rate).
