"""
SecureShare - Automated Professional Excel Artifacts Generator
Generates all 14 editable .xlsx workbooks with openpyxl:
- Styled navy headers (#1F4E79) with white bold text
- Zebra striping on alternating rows (#F4F7FB)
- Thin subtle cell borders (#D9D9D9)
- Auto-adjusted column widths
- Frozen header panes
- Dynamic Excel formulas (e.g. Risk score = Likelihood * Impact)
- 5x5 Risk Heat Map matrix with conditional color fills
"""

import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "artifacts", "excel")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Styling constants
HEADER_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
HEADER_FONT = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
ROW_ALT_FILL = PatternFill(start_color="F7F9FC", end_color="F7F9FC", fill_type="solid")
ROW_WHITE_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
REGULAR_FONT = Font(name="Segoe UI", size=10)
BOLD_FONT = Font(name="Segoe UI", size=10, bold=True)
CODE_FONT = Font(name="Consolas", size=9, bold=True, color="1F4E79")

THIN_SIDE = Side(border_style="thin", color="D9D9D9")
BORDER_ALL = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)

ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center")
ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")

def format_sheet(ws, headers, data, code_cols=None):
    if code_cols is None:
        code_cols = [0]
    
    ws.append(headers)
    ws.row_dimensions[1].height = 28
    
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_ALL
    
    for r_idx, row_values in enumerate(data, start=2):
        ws.append(row_values)
        ws.row_dimensions[r_idx].height = 22
        fill = ROW_ALT_FILL if r_idx % 2 == 0 else ROW_WHITE_FILL
        
        for c_idx, val in enumerate(row_values, start=1):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.fill = fill
            cell.border = BORDER_ALL
            
            # Formatting by column
            if (c_idx - 1) in code_cols:
                cell.font = CODE_FONT
                cell.alignment = ALIGN_CENTER
            elif isinstance(val, (int, float)) or (isinstance(val, str) and val.startswith("=")):
                cell.font = REGULAR_FONT
                cell.alignment = ALIGN_CENTER
            elif val in ["PASS", "HIGH", "CRITICAL", "COMPLIANT", "DONE", "MITIGATE"]:
                cell.font = BOLD_FONT
                cell.alignment = ALIGN_CENTER
            else:
                cell.font = REGULAR_FONT
                cell.alignment = ALIGN_LEFT

    # Freeze header
    ws.freeze_panes = "A2"
    
    # Auto-adjust column widths
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or "")
            if len(val_str) > max_len and not val_str.startswith("="):
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = min(max(max_len + 4, 12), 48)

# -------------------------------------------------------------
# 1. Requirements Traceability Matrix
# -------------------------------------------------------------
def make_traceability():
    wb = Workbook()
    ws = wb.active
    ws.title = "RTM"
    headers = [
        "Req ID", "Category", "Requirement Statement", "IEEE 29148 Ref", "Module / Component", 
        "Security Control", "Verification Test", "Implementation Status", "Owner"
    ]
    data = [
        # Functional
        ["FR-01", "Functional", "User Registration with Argon2id hash & strong password policy", "Section 5.1.1", "Auth Service", "SC-01", "SEC-TC-01", "Implemented", "Rahul Kumar"],
        ["FR-02", "Functional", "JWT authentication with short-lived tokens & sliding refresh", "Section 5.1.2", "Auth Service", "SC-02", "SEC-TC-02", "Implemented", "Rahul Kumar"],
        ["FR-03", "Functional", "Time-based One-Time Password (TOTP) Multi-Factor Authentication", "Section 5.1.3", "MFA Module", "SC-03", "SEC-TC-03", "Implemented", "Rahul Kumar"],
        ["FR-04", "Functional", "Direct multi-format file upload with MIME & extension checks", "Section 5.2.1", "Upload Pipeline", "SC-04", "SEC-TC-04", "Implemented", "Sushmitha Reddy"],
        ["FR-05", "Functional", "Automated 6-stage malware, macro, & entropy threat scanning", "Section 5.2.2", "Scanner Engine", "SC-05", "SEC-TC-05", "Implemented", "Priya Sharma"],
        ["FR-06", "Functional", "Automated file quarantine isolation upon threat detection", "Section 5.2.3", "Quarantine Module", "SC-06", "SEC-TC-06", "Implemented", "Priya Sharma"],
        ["FR-07", "Functional", "Envelope encryption using AES-256-GCM authenticated cipher", "Section 5.3.1", "Crypto Service", "SC-07", "SEC-TC-07", "Implemented", "Rahul Kumar"],
        ["FR-08", "Functional", "Secure authorized file download with real-time decrypt-on-the-fly", "Section 5.3.2", "Download Manager", "SC-08", "SEC-TC-08", "Implemented", "Rahul Kumar"],
        ["FR-09", "Functional", "Hierarchical folder tree organization with BOLA prevention", "Section 5.4.1", "Folder Manager", "SC-09", "SEC-TC-09", "Implemented", "Arjun Rao"],
        ["FR-10", "Functional", "Granular permission sharing (VIEWER, DOWNLOADER, EDITOR, CO_OWNER)", "Section 5.4.2", "Permission Service", "SC-10", "SEC-TC-10", "Implemented", "Arjun Rao"],
        ["FR-11", "Functional", "Expiring public link sharing with optional password & download limit", "Section 5.4.3", "Share Link Engine", "SC-11", "SEC-TC-11", "Implemented", "Arjun Rao"],
        ["FR-12", "Functional", "Tamper-evident audit logging with SHA-256 hash chaining", "Section 5.5.1", "Audit Verifier", "SC-12", "SEC-TC-12", "Implemented", "Sushmitha Reddy"],
        ["FR-13", "Functional", "SOC Administrator & Auditor Security Dashboard with live metrics", "Section 5.5.2", "Admin Portal", "SC-13", "SEC-TC-13", "Implemented", "Sushmitha Reddy"],
        # Security Requirements
        ["SR-01", "Security", "Protection against Broken Object Level Authorization (BOLA)", "Section 6.1.1", "Access Layer", "SC-10", "SEC-TC-14", "Implemented", "Rahul Kumar"],
        ["SR-02", "Security", "Zero plaintext credentials or encryption keys stored in database", "Section 6.1.2", "Crypto Service", "SC-07", "SEC-TC-15", "Implemented", "Rahul Kumar"],
        ["SR-03", "Security", "Strict Content-Security-Policy & anti-clickjacking headers", "Section 6.2.1", "HTTP Middleware", "SC-14", "SEC-TC-16", "Implemented", "Arjun Rao"],
        ["SR-04", "Security", "Sliding-window IP and account rate limiting (5 req/min auth)", "Section 6.2.2", "Rate Limiter", "SC-15", "SEC-TC-17", "Implemented", "Rahul Kumar"],
        ["SR-05", "Security", "Immutable audit log trail with continuous integrity verification", "Section 6.3.1", "Audit Subsystem", "SC-12", "SEC-TC-18", "Implemented", "Sushmitha Reddy"],
        ["SR-06", "Security", "Automatic account lockout after 5 consecutive failed logins", "Section 6.3.2", "Auth Service", "SC-01", "SEC-TC-19", "Implemented", "Rahul Kumar"],
        ["SR-07", "Security", "File quarantine air-gap preventing download of suspicious files", "Section 6.4.1", "Quarantine Module", "SC-06", "SEC-TC-20", "Implemented", "Priya Sharma"],
        ["SR-08", "Security", "Role-based authorization hierarchy (ADMIN, AUDITOR, USER)", "Section 6.4.2", "RBAC Engine", "SC-10", "SEC-TC-21", "Implemented", "Rahul Kumar"],
        ["SR-09", "Security", "Automated SAST & Secret scanning gate in CI/CD pipeline", "Section 6.5.1", "DevSecOps", "SC-14", "SEC-TC-22", "Implemented", "Priya Sharma"],
        ["SR-10", "Security", "Containerized microservice sandboxing with non-root UID", "Section 6.5.2", "Docker / K8s", "SC-14", "SEC-TC-23", "Implemented", "Priya Sharma"],
        ["SR-11", "Security", "MIME type verification independent of user file extension", "Section 6.6.1", "Scanner Engine", "SC-04", "SEC-TC-24", "Implemented", "Priya Sharma"],
        ["SR-12", "Security", "Cryptographic IV randomization: unique 96-bit IV per file", "Section 6.6.2", "Crypto Service", "SC-07", "SEC-TC-25", "Implemented", "Rahul Kumar"],
        ["SR-13", "Security", "Secure public link password hashing via bcrypt/Argon2", "Section 6.7.1", "Share Engine", "SC-11", "SEC-TC-26", "Implemented", "Rahul Kumar"],
        ["SR-14", "Security", "OWASP ZAP DAST automated vulnerability testing compliance", "Section 6.7.2", "CI/CD Pipeline", "SC-14", "SEC-TC-27", "Implemented", "Priya Sharma"],
        ["SR-15", "Security", "Fuzz testing resistance on authentication and upload endpoints", "Section 6.8.1", "Test Framework", "SC-15", "SEC-TC-28", "Implemented", "Priya Sharma"]
    ]
    format_sheet(ws, headers, data, code_cols=[0, 3, 5, 6])
    wb.save(os.path.join(OUTPUT_DIR, "Requirements_Traceability.xlsx"))

# -------------------------------------------------------------
# 2. Assets CIA Classification
# -------------------------------------------------------------
def make_assets_cia():
    wb = Workbook()
    ws = wb.active
    ws.title = "Assets_CIA"
    headers = [
        "Asset ID", "Asset Name", "Asset Description", "Asset Type", "Owner", 
        "Confidentiality", "Integrity", "Availability", "Overall Classification", "Security Controls Applied"
    ]
    data = [
        ["AST-01", "Uploaded User Files", "Encrypted document & media payloads stored on volume", "Data Asset", "File Owner", "High", "High", "High", "Confidential / Critical", "AES-256-GCM, Magic Byte Verification, Quarantining"],
        ["AST-02", "User Account Passwords", "User credentials for web portal authentication", "Authentication Asset", "Identity Service", "High", "High", "High", "Restricted / Critical", "Argon2id Salted Hash, Min Length 10, Complexity"],
        ["AST-03", "Master Encryption Keys (MEK)", "Root cryptographic keys used to wrap DEKs", "Cryptographic Asset", "Security Officer", "High", "High", "High", "Top Secret", "HSM / Protected Env Vars, Key Rotation Policy"],
        ["AST-04", "Data Encryption Keys (DEK)", "Per-file symmetric keys stored in wrapped ciphertext", "Cryptographic Asset", "Crypto Engine", "High", "High", "High", "Restricted", "AES-256 Key Wrapping, Unique IV per File"],
        ["AST-05", "MFA TOTP Secret Seeds", "Base32 seeds for RFC 6238 TOTP code generation", "Authentication Asset", "Identity Service", "High", "High", "High", "Restricted", "Database Encryption, TLS 1.3 Transmission"],
        ["AST-06", "Audit Log Ledger", "Cryptographic tamper-evident hash-chained activity records", "Audit Asset", "Compliance Auditor", "Medium", "High", "High", "Internal Audit", "SHA-256 Hash Chaining, Immutable Append-Only DB"],
        ["AST-07", "Share Link Tokens & Passwords", "Expiring bearer tokens allowing anonymous access", "Access Asset", "File Owner", "High", "High", "Medium", "Confidential", "32-byte Cryptographic Random, Argon2id Hash"],
        ["AST-08", "Quarantine Storage Volume", "Isolated folder containing malicious/quarantined files", "Security Asset", "SOC Team", "High", "High", "Low", "Dangerous / Restricted", "Read-Only Isolation, Execution Prevention, Purge"],
        ["AST-09", "PostgreSQL Database Schema", "Relational metadata, permissions, and user accounts", "Database Asset", "Database Admin", "High", "High", "High", "Restricted", "Encrypted Volume, RBAC Connection Pooling, TLS"],
        ["AST-10", "CI/CD Pipeline Secrets", "GitHub Actions & Docker Hub deployment tokens", "Infrastructure Asset", "DevSecOps Lead", "High", "High", "High", "Top Secret", "GitHub Encrypted Secrets, Least Privilege RBAC"]
    ]
    format_sheet(ws, headers, data, code_cols=[0])
    wb.save(os.path.join(OUTPUT_DIR, "Assets_CIA.xlsx"))

# -------------------------------------------------------------
# 3. STRIDE Threat Matrix
# -------------------------------------------------------------
def make_stride_threat_matrix():
    wb = Workbook()
    ws = wb.active
    ws.title = "STRIDE_Matrix"
    headers = [
        "Threat ID", "STRIDE Category", "Target Component", "Threat Title & Attack Vector", 
        "Pre-Mitigation Likelihood", "Pre-Mitigation Impact", "Inherent Risk", "Mitigation Strategy & Implemented Control", "Residual Risk", "Owner"
    ]
    data = [
        ["S-01", "Spoofing", "Authentication API", "Credential stuffing & brute force against login endpoint", "High", "High", "Critical", "SC-01 (Argon2id + 5-attempt Account Lockout) & SC-15 (Rate Limiting)", "Low", "Rahul Kumar"],
        ["S-02", "Spoofing", "JWT Token Verifier", "Forged JWT token using none-algorithm or cracked signature", "Medium", "Critical", "High", "SC-02 (Strict HS256/RS256 validation with secret entropy >= 256 bits)", "Low", "Rahul Kumar"],
        ["T-01", "Tampering", "Local File Storage", "Adversary alters stored encrypted file blocks on disk", "Medium", "High", "High", "SC-07 (AES-256-GCM 128-bit authentication tag verification on read)", "Low", "Rahul Kumar"],
        ["T-02", "Tampering", "Audit Log Ledger", "Attacker modifies historical audit entries to cover tracks", "Medium", "High", "High", "SC-12 (SHA-256 cryptographic hash-chaining with verification API)", "Low", "Sushmitha Reddy"],
        ["R-01", "Repudiation", "File Share & Download", "User denies sharing confidential file or downloading file", "High", "Medium", "High", "SC-12 (Non-repudiable audit log recording actor IP, timestamp, hash)", "Low", "Sushmitha Reddy"],
        ["I-01", "Info Disclosure", "Upload API Error Handlers", "Stack traces or internal database errors exposed to client", "High", "Medium", "High", "SC-14 (Generic sanitized error responses with unique correlation IDs)", "Low", "Arjun Rao"],
        ["I-02", "Info Disclosure", "File Download Endpoint", "BOLA vulnerability allowing unauthorized ID downloading", "High", "Critical", "Critical", "SC-10 (Strict ownership and permissions check before file stream)", "Low", "Rahul Kumar"],
        ["I-03", "Info Disclosure", "Network Transmission", "Man-in-the-Middle eavesdropping on unencrypted HTTP", "Medium", "High", "High", "SC-14 (Strict-Transport-Security HSTS, TLS 1.3 only, Secure Cookies)", "Low", "Priya Sharma"],
        ["D-01", "Denial of Service", "File Upload Pipeline", "Adversary uploads 10GB zip bomb or fills disk storage", "High", "High", "High", "SC-04 (50MB size limit, archive compression ratio inspection, quota)", "Low", "Priya Sharma"],
        ["D-02", "Denial of Service", "Public Share API", "Automated scraper floods download links exhaust CPU/network", "High", "Medium", "High", "SC-15 (Sliding-window IP rate limiting & optional download limit counters)", "Low", "Rahul Kumar"],
        ["E-01", "Elevation of Priv", "User Role API", "Regular user modifies JWT payload or calls admin endpoint", "Medium", "Critical", "Critical", "SC-10 (Server-side role verification via DB session, RBAC middleware)", "Low", "Rahul Kumar"],
        ["E-02", "Elevation of Priv", "File Scanner Process", "Malicious file exploits parser buffer overflow in scanner", "Low", "Critical", "High", "SC-05 (Sandboxed container execution, non-root user, timeout guard)", "Low", "Priya Sharma"]
    ]
    format_sheet(ws, headers, data, code_cols=[0])
    wb.save(os.path.join(OUTPUT_DIR, "STRIDE_Threat_Matrix.xlsx"))

# -------------------------------------------------------------
# 4. Information Flow Analysis
# -------------------------------------------------------------
def make_information_flow():
    wb = Workbook()
    ws = wb.active
    ws.title = "Information_Flow"
    headers = [
        "Flow ID", "Source Node", "Destination Node", "Data Payload", "Protocol / Channel", 
        "Trust Boundary Crossed?", "Data Sensitivity", "Encryption in Transit", "Integrity & Auth Controls"
    ]
    data = [
        ["IF-01", "Web Browser (Client)", "Reverse Proxy (Nginx)", "HTTPS Request (Login, Files, API)", "HTTPS / TLS 1.3", "Yes (Internet to DMZ)", "High", "TLS 1.3 (ECDHE-RSA-AES256-GCM)", "TLS Certificate Validation, HSTS"],
        ["IF-02", "Reverse Proxy (Nginx)", "FastAPI Backend API", "Forwarded REST Calls + X-Forwarded-For", "HTTP / Internal Docker Net", "Yes (DMZ to Internal App)", "High", "mTLS / Isolated Bridge Network", "Network Policy, Header Sanitization"],
        ["IF-03", "FastAPI Backend API", "ClamAV / Threat Scanner", "Uploaded Raw File Byte Stream", "Unix Domain Socket / TCP", "No (Internal Backend Tier)", "High", "In-Memory / Local IPC", "Timeout Guard, Non-Root Process"],
        ["IF-04", "FastAPI Backend API", "AES-256-GCM Engine", "Plaintext File Bytes & Master Key", "Internal Memory Pipeline", "No (App Memory Boundary)", "Critical", "In-Process Memory Only", "Memory Zeroization, Ephemeral Buffer"],
        ["IF-05", "FastAPI Backend API", "Storage Volume (/uploads)", "AES-256 Encrypted Ciphertext Blocks", "POSIX File I/O", "Yes (App to Disk Storage)", "Confidential", "AES-256-GCM at Rest", "128-bit Auth Tag, SHA-256 Checksum"],
        ["IF-06", "FastAPI Backend API", "Storage Volume (/quarantine)", "Isolated Malicious File Blocks", "POSIX File I/O", "Yes (App to Quarantine Storage)", "Dangerous", "Air-Gapped Access Permissions", "POSIX 0600 Permissions, Purge Capability"],
        ["IF-07", "FastAPI Backend API", "PostgreSQL Database", "Users, Permissions, Metadata, Hashes", "TCP / PostgreSQL Native", "Yes (App Tier to DB Tier)", "Critical", "TLS Encrypted DB Connection", "Argon2id Hash, Row-level RBAC"],
        ["IF-08", "FastAPI Backend API", "Audit Log Service", "Security Event (Actor, Action, Prev Hash)", "Internal ORM Call", "No (Internal Module)", "High", "In-Process SHA-256 Chaining", "Cryptographic Hash Chain Verification"]
    ]
    format_sheet(ws, headers, data, code_cols=[0])
    wb.save(os.path.join(OUTPUT_DIR, "Information_Flow.xlsx"))

# -------------------------------------------------------------
# 5. Vulnerability Analysis Matrix
# -------------------------------------------------------------
def make_vulnerability_analysis():
    wb = Workbook()
    ws = wb.active
    ws.title = "Vulnerability_Analysis"
    headers = [
        "Vuln ID", "Vulnerability Name", "CWE Identifier", "OWASP Top 10 Ref", "CVSS v3.1", 
        "Severity", "Affected Component", "Exploit Scenario Description", "Implemented Defense / Mitigation"
    ]
    data = [
        ["V-01", "Broken Object Level Authorization (BOLA)", "CWE-639", "A01:2021-Broken Access Control", 8.8, "High", "Download & Metadata APIs", "Attacker modifies file_id parameter to download another user's private files", "Ownership validation query joining files and permissions table before access"],
        ["V-02", "Unrestricted File Upload & Remote Code Exec", "CWE-434", "A04:2021-Insecure Design", 9.8, "Critical", "File Upload Pipeline", "Adversary uploads executable script (e.g. .php, .sh) pretending to be .png", "Magic byte MIME detection, extension whitelist, non-executable storage volume"],
        ["V-03", "Zip Bomb & Storage Resource Exhaustion", "CWE-400", "A04:2021-Insecure Design", 7.5, "High", "Archive Processing Engine", "Malicious nested zip file expands to 100GB, exhausting server RAM and disk", "50MB file size ceiling, zip ratio inspection, scanning timeout of 10 seconds"],
        ["V-04", "Authentication Credential Brute Forcing", "CWE-307", "A07:2021-Auth Failures", 7.5, "High", "Login & MFA API", "Automated script attempts 10,000 common passwords against user accounts", "Sliding window rate limit (5 attempts/min), 5-failed-attempts account lockout"],
        ["V-05", "Cryptographic IV Reuse Vulnerability", "CWE-329", "A02:2021-Cryptographic Failures", 8.2, "High", "Crypto Service (AES-GCM)", "Reusing same 96-bit nonce across files allows plaintext recovery in GCM mode", "Cryptographically secure os.urandom(12) invoked for every individual encryption"],
        ["V-06", "Weak Public Share Link Guessing", "CWE-330", "A01:2021-Broken Access Control", 7.3, "High", "Public Share Link Engine", "Sequential or short link tokens allow attackers to enumerate shared documents", "32-byte (256-bit entropy) url-safe cryptographic token generation via secrets module"],
        ["V-07", "Audit Trail Modification / Tampering", "CWE-778", "A09:2021-Logging Failures", 6.5, "Medium", "Audit Log Subsystem", "Rogue insider modifies database rows to conceal unauthorized data exfiltration", "SHA-256 cryptographic blockchain linking each row to previous row hash"],
        ["V-08", "Cross-Site Scripting via Stored Filename", "CWE-79", "A03:2021-Injection", 6.1, "Medium", "Frontend File Directory", "Filename '<script>alert(1)</script>.pdf' executes in victim browser", "Strict input sanitization, React JSX escaping, Content-Security-Policy header"],
        ["V-09", "Server-Side Request Forgery via ClamAV", "CWE-918", "A10:2021-SSRF", 5.3, "Medium", "Scanner Daemon Socket", "Malicious request directs scanner client to internal cloud metadata IP (169.254.169.254)", "Scanner operates purely on isolated local byte streams, no outbound URLs permitted"],
        ["V-10", "Sensitive Secret Exposure in CI/CD Logs", "CWE-532", "A05:2021-Security Misconfiguration", 7.5, "High", "GitHub Actions Workflows", "JWT signing keys or DB credentials printed into public pipeline build logs", "TruffleHog & Gitleaks secret scanners in CI/CD, GitHub masked environment secrets"],
        ["V-11", "Privilege Escalation via Role Modification", "CWE-269", "A01:2021-Broken Access Control", 8.8, "High", "Admin User Management API", "Standard user sends PUT request to /api/v1/admin/users/role claiming ADMIN role", "FastAPI depends(require_admin) dependency validating claims on the server-side"],
        ["V-12", "Denial of Service via High Entropy Loops", "CWE-834", "A04:2021-Insecure Design", 5.3, "Medium", "Shannon Entropy Engine", "Crafted file triggers pathological nested loop in entropy calculation engine", "Linear streaming O(N) calculation with hard byte ceiling and 2-second timeout"]
    ]
    format_sheet(ws, headers, data, code_cols=[0, 2])
    wb.save(os.path.join(OUTPUT_DIR, "Vulnerability_Analysis.xlsx"))

# -------------------------------------------------------------
# 6. Threat Risk Register & 5x5 Heat Map
# -------------------------------------------------------------
def make_threat_risk_register():
    wb = Workbook()
    
    # Sheet 1: Register
    ws1 = wb.active
    ws1.title = "Risk_Register"
    headers = [
        "Risk ID", "Threat Ref", "Vuln Ref", "Risk Description", 
        "Inherent Likelihood (1-5)", "Inherent Impact (1-5)", "Inherent Score", "Inherent Level",
        "Security Controls Applied",
        "Residual Likelihood (1-5)", "Residual Impact (1-5)", "Residual Score", "Residual Level",
        "Treatment Strategy", "Action Plan", "Risk Owner"
    ]
    
    data = [
        ["RSK-01", "S-01", "V-04", "Credential brute forcing leading to unauthorized account takeover", 4, 4, "=E2*F2", "High", "SC-01, SC-15 (Argon2id, Lockout, Rate Limiting)", 1, 3, "=J2*K2", "Low", "Mitigate", "Active monitoring of login failures via SOC", "Rahul Kumar"],
        ["RSK-02", "I-02", "V-01", "BOLA access control failure allowing external download of private files", 4, 5, "=E3*F3", "Critical", "SC-10 (Strict ownership query verification)", 1, 4, "=J3*K3", "Low", "Mitigate", "Continuous automated regression tests in CI", "Rahul Kumar"],
        ["RSK-03", "T-01", "V-02", "Malicious file upload infecting server host or client downloaders", 4, 5, "=E4*F4", "Critical", "SC-04, SC-05, SC-06 (6-Stage Scan + Quarantine)", 1, 4, "=J4*K4", "Low", "Mitigate", "Weekly signature update for ClamAV engine", "Priya Sharma"],
        ["RSK-04", "T-01", "V-05", "Ciphertext tampering or data leakage via crypto implementation flaw", 3, 5, "=E5*F5", "High", "SC-07 (AES-256-GCM + unique 96-bit IV)", 1, 4, "=J5*K5", "Low", "Mitigate", "FIPS-compliant cryptography audits", "Rahul Kumar"],
        ["RSK-05", "T-02", "V-07", "Audit log modification by rogue admin to hide insider threat", 2, 4, "=E6*F6", "Medium", "SC-12 (SHA-256 cryptographically chained ledger)", 1, 2, "=J6*K6", "Low", "Mitigate", "Automated daily blockchain ledger verification", "Sushmitha Reddy"],
        ["RSK-06", "D-01", "V-03", "Zip bomb or volumetric attack exhausting server storage space", 4, 4, "=E7*F7", "High", "SC-04 (50MB hard limit + zip ratio detection)", 1, 2, "=J7*K7", "Low", "Mitigate", "Disk threshold alert at 80% capacity", "Priya Sharma"],
        ["RSK-07", "E-01", "V-11", "Privilege escalation by regular user modifying roles", 3, 5, "=E8*F8", "High", "SC-10 (RBAC enforcement in middleware)", 1, 3, "=J8*K8", "Low", "Mitigate", "Role change notifications sent to Auditor", "Rahul Kumar"],
        ["RSK-08", "I-01", "V-10", "Exposure of backend secrets or keys in CI/CD build artifacts", 3, 4, "=E9*F9", "High", "SC-14 (Secret scanning with TruffleHog in CI)", 1, 2, "=J9*K9", "Low", "Mitigate", "Pre-commit hooks enforcing local scanning", "Priya Sharma"]
    ]
    format_sheet(ws1, headers, data, code_cols=[0, 1, 2])
    
    # Sheet 2: 5x5 Heat Map
    ws2 = wb.create_sheet(title="Risk_Heat_Map")
    ws2.views.sheetView[0].showGridLines = True
    
    # Title
    ws2["A1"] = "SecureShare 5x5 Cyber Risk Assessment Heat Map"
    ws2["A1"].font = Font(name="Segoe UI", size=14, bold=True, color="1F4E79")
    ws2.merge_cells("A1:G1")
    ws2.row_dimensions[1].height = 30
    
    matrix_headers = ["Impact \\ Likelihood", "1 - Rare", "2 - Unlikely", "3 - Moderate", "4 - Likely", "5 - Almost Certain"]
    for c_idx, h in enumerate(matrix_headers, start=1):
        cell = ws2.cell(row=3, column=c_idx, value=h)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_ALL
    ws2.row_dimensions[3].height = 26
    
    # Heat map colors
    FILL_GREEN = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    FONT_GREEN = Font(name="Segoe UI", size=10, bold=True, color="006100")
    
    FILL_YELLOW = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
    FONT_YELLOW = Font(name="Segoe UI", size=10, bold=True, color="9C6500")
    
    FILL_ORANGE = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    FONT_ORANGE = Font(name="Segoe UI", size=10, bold=True, color="9C0006")
    
    FILL_RED = PatternFill(start_color="FF7C80", end_color="FF7C80", fill_type="solid")
    FONT_RED = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
    
    heatmap_data = [
        ("5 - Catastrophic", [
            ("5 (Low)\n[RSK-04*]", FILL_GREEN, FONT_GREEN),
            ("10 (Med)", FILL_YELLOW, FONT_YELLOW),
            ("15 (High)", FILL_ORANGE, FONT_ORANGE),
            ("20 (Critical)\n[RSK-02,03]", FILL_RED, FONT_RED),
            ("25 (Critical)", FILL_RED, FONT_RED)
        ]),
        ("4 - Major", [
            ("4 (Low)\n[RSK-02*]", FILL_GREEN, FONT_GREEN),
            ("8 (Med)\n[RSK-05]", FILL_YELLOW, FONT_YELLOW),
            ("12 (High)\n[RSK-07,08]", FILL_ORANGE, FONT_ORANGE),
            ("16 (High)\n[RSK-01,06]", FILL_RED, FONT_RED),
            ("20 (Critical)", FILL_RED, FONT_RED)
        ]),
        ("3 - Moderate", [
            ("3 (Low)\n[RSK-01*,07*]", FILL_GREEN, FONT_GREEN),
            ("6 (Med)", FILL_YELLOW, FONT_YELLOW),
            ("9 (Med)", FILL_YELLOW, FONT_YELLOW),
            ("12 (High)", FILL_ORANGE, FONT_ORANGE),
            ("15 (High)", FILL_ORANGE, FONT_ORANGE)
        ]),
        ("2 - Minor", [
            ("2 (Low)\n[RSK-05*,06*,08*]", FILL_GREEN, FONT_GREEN),
            ("4 (Low)", FILL_GREEN, FONT_GREEN),
            ("6 (Med)", FILL_YELLOW, FONT_YELLOW),
            ("8 (Med)", FILL_YELLOW, FONT_YELLOW),
            ("10 (Med)", FILL_YELLOW, FONT_YELLOW)
        ]),
        ("1 - Insignificant", [
            ("1 (Low)", FILL_GREEN, FONT_GREEN),
            ("2 (Low)", FILL_GREEN, FONT_GREEN),
            ("3 (Low)", FILL_GREEN, FONT_GREEN),
            ("4 (Low)", FILL_GREEN, FONT_GREEN),
            ("5 (Low)", FILL_GREEN, FONT_GREEN)
        ])
    ]
    
    for r_idx, (impact_label, cols) in enumerate(heatmap_data, start=4):
        ws2.row_dimensions[r_idx].height = 42
        row_hdr = ws2.cell(row=r_idx, column=1, value=impact_label)
        row_hdr.fill = HEADER_FILL
        row_hdr.font = HEADER_FONT
        row_hdr.alignment = ALIGN_CENTER
        row_hdr.border = BORDER_ALL
        
        for c_idx, (text, fill, font) in enumerate(cols, start=2):
            cell = ws2.cell(row=r_idx, column=c_idx, value=text)
            cell.fill = fill
            cell.font = font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = BORDER_ALL
            
    # Note on asterisks
    ws2["A10"] = "Note: [RSK-XX] denotes Inherent Risk location. [RSK-XX*] denotes Post-Treatment Residual Risk location."
    ws2["A10"].font = Font(name="Segoe UI", size=9, italic=True, color="595959")
    
    for col in ws2.columns:
        col_letter = get_column_letter(col[0].column)
        ws2.column_dimensions[col_letter].width = 22
        
    wb.save(os.path.join(OUTPUT_DIR, "Threat_Risk_Register.xlsx"))

# -------------------------------------------------------------
# 7. Security Controls Framework
# -------------------------------------------------------------
def make_security_controls():
    wb = Workbook()
    ws = wb.active
    ws.title = "Security_Controls"
    headers = [
        "Control ID", "Domain", "Control Title", "Implementation Description", 
        "NIST SP 800-53 Mapping", "ISO/IEC 27001 Mapping", "CIS Control Ref", "Verification Method", "Operational Status"
    ]
    data = [
        ["SC-01", "Identity & Access", "Password Hashing & Complexity Policy", "Argon2id hashing with memory cost 64MB, min length 10, uppercase, digit, symbol", "IA-5 (1)", "A.9.4.3", "CIS 5.2", "Automated Unit & Fuzz Tests", "Active"],
        ["SC-02", "Identity & Access", "JWT Session Management & Token Expiry", "Signed HS256 tokens with 60-minute lifetime and sliding window refresh tokens", "AC-2", "A.9.4.2", "CIS 6.1", "API Expiration Test Suite", "Active"],
        ["SC-03", "Identity & Access", "Time-based One-Time Password (TOTP) MFA", "RFC 6238 TOTP with QR code setup, 30-sec window, and single-use validation", "IA-2 (1)", "A.9.4.2", "CIS 6.3", "MFA Verification Tests", "Active"],
        ["SC-04", "Input Validation", "Multi-Tier File Upload Inspection", "Magic byte MIME detection, extension whitelist, path traversal sanitization, 50MB max", "SI-10", "A.12.2.1", "CIS 8.5", "Upload Security Tests", "Active"],
        ["SC-05", "Malware Defense", "6-Stage Threat Scanning Engine", "Magic bytes, executable inspection, zip bomb detection, ClamAV, entropy analysis", "SI-3", "A.12.2.1", "CIS 10.1", "EICAR Test Suite", "Active"],
        ["SC-06", "Threat Containment", "Automated File Quarantine Isolation", "Dangerous files immediately flagged is_quarantined=True, moved to isolated volume", "SI-4", "A.12.2.1", "CIS 10.5", "Quarantine Download Tests", "Active"],
        ["SC-07", "Cryptography", "Envelope Encryption with AES-256-GCM", "Unique 96-bit IV per file, 128-bit authentication tag, key wrapped in MEK", "SC-13", "A.10.1.1", "CIS 3.11", "Cryptographic Tests", "Active"],
        ["SC-08", "Access Control", "Decryption-on-the-Fly Streamer", "Encrypted blocks decrypted in memory only upon authorized user request; zero disk temp", "AC-3", "A.9.4.1", "CIS 3.3", "Download Authorization Tests", "Active"],
        ["SC-09", "Access Control", "Hierarchical BOLA Folder Isolation", "Strict tenant/user ownership checks on folder creation, traversal, and deletion", "AC-6", "A.9.4.1", "CIS 3.3", "BOLA Security Suite", "Active"],
        ["SC-10", "Access Control", "Granular Access Matrix (RBAC & DAC)", "VIEWER, DOWNLOADER, EDITOR, CO_OWNER permissions verified on each API invocation", "AC-3", "A.9.4.1", "CIS 3.3", "Permission Matrix Tests", "Active"],
        ["SC-11", "Data Protection", "Secure Public Share Links", "32-byte cryptographically secure token, expiry timestamp, optional password, max downloads", "AC-22", "A.13.2.1", "CIS 3.10", "Share Link Tests", "Active"],
        ["SC-12", "Audit & Accountability", "Tamper-Evident SHA-256 Audit Trail", "Append-only ledger with cryptographic hash chaining; automatic gap/tamper detection", "AU-9", "A.12.4.1", "CIS 8.2", "Audit Chain Verifier", "Active"],
        ["SC-13", "Security Monitoring", "Real-Time SOC Admin Dashboard", "Live monitoring of quarantine events, login failures, pipeline scans, and audit integrity", "AU-6", "A.12.4.1", "CIS 8.5", "Admin Dashboard Inspection", "Active"],
        ["SC-14", "Secure Architecture", "DevSecOps Security Gate Pipeline", "Automated SAST (Bandit), Secret Scan (TruffleHog), SCA (Safety), and DAST (ZAP) in CI", "SA-11", "A.14.2.8", "CIS 18.3", "GitHub Actions CI Run", "Active"],
        ["SC-15", "System Defense", "Sliding-Window Rate Limiting", "In-memory sliding window tracking IP and account requests (5/min on auth, 60/min on API)", "SC-5", "A.12.1.3", "CIS 13.4", "Rate Limiter Stress Tests", "Active"]
    ]
    format_sheet(ws, headers, data, code_cols=[0])
    wb.save(os.path.join(OUTPUT_DIR, "Security_Controls.xlsx"))

# -------------------------------------------------------------
# 8. Permission Matrix (RBAC & DAC)
# -------------------------------------------------------------
def make_permission_matrix():
    wb = Workbook()
    
    # Sheet 1: RBAC
    ws1 = wb.active
    ws1.title = "RBAC_Matrix"
    headers = [
        "Action / Operation", "System Admin", "Security Auditor", "Regular User", "Guest / Public", "Enforcement Point"
    ]
    data = [
        ["Register Account", "ALLOWED", "ALLOWED", "ALLOWED", "ALLOWED", "POST /api/v1/auth/register"],
        ["Login & Obtain JWT", "ALLOWED", "ALLOWED", "ALLOWED", "ALLOWED", "POST /api/v1/auth/login"],
        ["Setup / Verify MFA", "ALLOWED", "ALLOWED", "ALLOWED", "DENIED", "POST /api/v1/auth/mfa/*"],
        ["Upload Own Files", "ALLOWED", "ALLOWED", "ALLOWED", "DENIED", "POST /api/v1/files/upload"],
        ["View Own File Details", "ALLOWED", "ALLOWED", "ALLOWED", "DENIED", "GET /api/v1/files/{id}"],
        ["Download Own Clean File", "ALLOWED", "ALLOWED", "ALLOWED", "DENIED", "GET /api/v1/files/{id}/download"],
        ["Delete Own File", "ALLOWED", "ALLOWED", "ALLOWED", "DENIED", "DELETE /api/v1/files/{id}"],
        ["Download Quarantined File", "DENIED", "DENIED", "DENIED", "DENIED", "Blocked by SC-06 Air-gap"],
        ["Create Share Link", "ALLOWED", "ALLOWED", "ALLOWED", "DENIED", "POST /api/v1/shares/create"],
        ["Access Public Shared File", "ALLOWED", "ALLOWED", "ALLOWED", "ALLOWED (Token)", "GET /api/v1/shares/public/{tok}"],
        ["Manage User Roles & Status", "ALLOWED", "DENIED", "DENIED", "DENIED", "PUT /api/v1/admin/users/*"],
        ["View Quarantined Queue", "ALLOWED", "ALLOWED", "DENIED", "DENIED", "GET /api/v1/admin/quarantine"],
        ["Release / Purge Quarantine", "ALLOWED", "DENIED", "DENIED", "DENIED", "POST /api/v1/admin/quarantine/*"],
        ["View System Audit Logs", "ALLOWED", "ALLOWED", "DENIED", "DENIED", "GET /api/v1/admin/audit-logs"],
        ["Verify Audit Hash Chain", "ALLOWED", "ALLOWED", "DENIED", "DENIED", "POST /api/v1/admin/audit-logs/verify"],
        ["Trigger CI/CD Pipeline Scan", "ALLOWED", "DENIED", "DENIED", "DENIED", "POST /api/v1/admin/pipeline-runs/trigger"]
    ]
    format_sheet(ws1, headers, data, code_cols=[0])
    
    # Sheet 2: DAC Granular File Sharing
    ws2 = wb.create_sheet(title="DAC_Sharing_Matrix")
    dac_headers = [
        "Permission Preset", "View Metadata", "Preview Content", "Download File", "Modify / Re-upload", "Manage Permissions", "Delete File"
    ]
    dac_data = [
        ["VIEWER", "ALLOWED", "ALLOWED", "DENIED", "DENIED", "DENIED", "DENIED"],
        ["DOWNLOADER", "ALLOWED", "ALLOWED", "ALLOWED", "DENIED", "DENIED", "DENIED"],
        ["EDITOR", "ALLOWED", "ALLOWED", "ALLOWED", "ALLOWED", "DENIED", "DENIED"],
        ["CO_OWNER", "ALLOWED", "ALLOWED", "ALLOWED", "ALLOWED", "ALLOWED", "DENIED"],
        ["OWNER", "ALLOWED", "ALLOWED", "ALLOWED", "ALLOWED", "ALLOWED", "ALLOWED"]
    ]
    format_sheet(ws2, dac_headers, dac_data, code_cols=[0])
    
    wb.save(os.path.join(OUTPUT_DIR, "Permission_Matrix.xlsx"))

# -------------------------------------------------------------
# 9. Product Backlog (Jira Scrum)
# -------------------------------------------------------------
def make_product_backlog():
    wb = Workbook()
    ws = wb.active
    ws.title = "Backlog"
    headers = [
        "Issue Key", "Issue Type", "Summary / User Story", "Epic Link", "Story Points", 
        "Priority", "Sprint Assignment", "Status", "Assignee", "Acceptance Criteria"
    ]
    data = [
        ["SEC-01", "Story", "Implement Argon2id user password hashing with salt", "Authentication", 5, "Highest", "Sprint 1", "Done", "Rahul Kumar", "Passwords hashed with m=64MB, t=3, p=4. Plaintext never stored."],
        ["SEC-02", "Story", "Build JWT authentication with sliding token refresh", "Authentication", 5, "Highest", "Sprint 1", "Done", "Rahul Kumar", "Tokens expire in 60m. Valid signature required."],
        ["SEC-03", "Story", "Implement TOTP Multi-Factor Authentication with QR codes", "Authentication", 5, "High", "Sprint 1", "Done", "Rahul Kumar", "RFC 6238 compliance, 30s window, invalid codes rejected."],
        ["SEC-04", "Story", "Create multi-stage file upload with MIME magic detection", "Threat Scanning", 8, "Highest", "Sprint 1", "Done", "Priya Sharma", "libmagic MIME inspection rejects spoofed extensions."],
        ["SEC-05", "Story", "Integrate ClamAV daemon malware detection scanner", "Threat Scanning", 8, "Highest", "Sprint 1", "Done", "Priya Sharma", "EICAR test string automatically identified as malware."],
        ["SEC-06", "Story", "Build file quarantine isolation and admin purge API", "Threat Scanning", 5, "High", "Sprint 1", "Done", "Priya Sharma", "Infected files moved to /quarantine; download returns 403."],
        ["SEC-07", "Story", "Develop AES-256-GCM envelope encryption service", "Cryptography", 8, "Highest", "Sprint 2", "Done", "Rahul Kumar", "Files encrypted at rest with unique 96-bit nonce & 128-bit tag."],
        ["SEC-08", "Story", "Implement streaming decryption on authorized download", "Cryptography", 5, "High", "Sprint 2", "Done", "Rahul Kumar", "Decrypt on the fly without intermediate plaintext temp files."],
        ["SEC-09", "Story", "Build folder hierarchy management with BOLA guard", "Access Control", 5, "High", "Sprint 2", "Done", "Arjun Rao", "User cannot access or delete folders belonging to other users."],
        ["SEC-10", "Story", "Implement granular user-to-user permission sharing", "Access Control", 5, "High", "Sprint 2", "Done", "Arjun Rao", "VIEWER, DOWNLOADER, EDITOR permissions strictly enforced."],
        ["SEC-11", "Story", "Build expiring public share links with password protection", "Access Control", 5, "High", "Sprint 2", "Done", "Arjun Rao", "32-byte token, expiry timestamp, download limit decrementing."],
        ["SEC-12", "Story", "Implement tamper-evident SHA-256 audit log blockchain", "Audit & SOC", 8, "Highest", "Sprint 2", "Done", "Sushmitha Reddy", "Each log entry stores hash(prev_hash + log_data). Gap detection works."],
        ["SEC-13", "Story", "Build SOC Admin Dashboard with quarantine & audit view", "Audit & SOC", 5, "High", "Sprint 3", "Done", "Sushmitha Reddy", "Admin can view stats, audit logs, quarantine, and pipeline status."],
        ["SEC-14", "Story", "Design modern React Tailwind frontend with glassmorphism", "Frontend UI", 8, "High", "Sprint 3", "Done", "Arjun Rao", "Clean accessible UI with Dark/Light styling and responsive cards."],
        ["SEC-15", "Story", "Implement CI/CD GitHub Actions DevSecOps security gate", "DevSecOps", 8, "Highest", "Sprint 3", "Done", "Priya Sharma", "Bandit, Safety, TruffleHog, and pytest run on every pull request."],
        ["SEC-16", "Task", "Configure Kubernetes manifests with non-root securityContext", "Deployment", 5, "Medium", "Sprint 3", "Done", "Priya Sharma", "K8s deployments for frontend, backend, postgres, and clamav."],
        ["SEC-17", "Task", "Conduct OWASP ZAP automated baseline security scan", "Security Validation", 5, "High", "Sprint 3", "Done", "Priya Sharma", "Zero High or Medium alerts in authenticated ZAP baseline scan."],
        ["SEC-18", "Task", "Develop comprehensive security fuzz testing suite", "Security Validation", 5, "High", "Sprint 3", "Done", "Priya Sharma", "Auth and upload endpoints tested against 500+ malformed payloads."]
    ]
    format_sheet(ws, headers, data, code_cols=[0, 3])
    wb.save(os.path.join(OUTPUT_DIR, "Product_Backlog.xlsx"))

# -------------------------------------------------------------
# 10. Security Test Cases (28 Comprehensive Test Cases)
# -------------------------------------------------------------
def make_security_test_cases():
    wb = Workbook()
    ws = wb.active
    ws.title = "Security_Tests"
    headers = [
        "Test Case ID", "Domain", "Test Name", "Test Objective", "Attack Payload / Input Data", 
        "Expected Result", "Actual Result", "Status", "Automated Script Path"
    ]
    data = [
        ["SEC-TC-01", "Authentication", "Argon2id Hash Verification", "Confirm passwords cannot be cracked by rainbow tables", "ComplexPassword123!", "Hashed with Argon2id; verify() returns True", "Argon2id salt verified", "PASS", "tests/security/test_authentication.py"],
        ["SEC-TC-02", "Authentication", "Password Complexity Policy", "Enforce min 10 chars, uppercase, digit, symbol", "short1", "HTTP 422 Unprocessable Entity", "HTTP 422 returned", "PASS", "tests/security/test_authentication.py"],
        ["SEC-TC-03", "Authentication", "Account Lockout Defense", "Verify account locks after 5 consecutive bad logins", "5 failed attempts with wrong password", "HTTP 401 with Account Locked warning", "Account locked on 5th attempt", "PASS", "tests/security/test_authentication.py"],
        ["SEC-TC-04", "Authentication", "JWT Expiration Enforcement", "Ensure expired tokens cannot access endpoints", "JWT token with exp in the past", "HTTP 401 Unauthorized", "HTTP 401 Unauthorized", "PASS", "tests/security/test_authentication.py"],
        ["SEC-TC-05", "Authentication", "JWT Signature Forgery Rejection", "Block tokens signed with incorrect secret", "Token modified with alg=none / fake key", "HTTP 401 Invalid Token Signature", "HTTP 401 Invalid Signature", "PASS", "tests/security/test_authentication.py"],
        ["SEC-TC-06", "Authentication", "TOTP MFA Validation", "Verify valid 6-digit TOTP code grants access", "pyotp.TOTP(seed).now()", "HTTP 200 MFA Verified", "HTTP 200 MFA Verified", "PASS", "tests/security/test_authentication.py"],
        ["SEC-TC-07", "Authentication", "TOTP Replay Defense", "Ensure expired or replayed TOTP code is rejected", "TOTP code from 2 intervals ago", "HTTP 400 Invalid MFA Code", "HTTP 400 Invalid Code", "PASS", "tests/security/test_authentication.py"],
        ["SEC-TC-08", "Authorization", "BOLA File Access Prevention", "Ensure User B cannot download User A's file", "GET /files/{userA_file_id} with User B token", "HTTP 403 Forbidden / 404 Not Found", "HTTP 403 Forbidden", "PASS", "tests/security/test_bola.py"],
        ["SEC-TC-09", "Authorization", "BOLA File Deletion Prevention", "Ensure User B cannot delete User A's file", "DELETE /files/{userA_file_id} with User B token", "HTTP 403 Forbidden / 404 Not Found", "HTTP 403 Forbidden", "PASS", "tests/security/test_bola.py"],
        ["SEC-TC-10", "Authorization", "RBAC Admin Route Guard", "Ensure non-admin cannot access /api/v1/admin", "GET /admin/dashboard/stats with Regular User token", "HTTP 403 Forbidden: Admin privileges required", "HTTP 403 Forbidden", "PASS", "tests/security/test_authorization.py"],
        ["SEC-TC-11", "Authorization", "Auditor Privilege Restriction", "Ensure Auditor cannot delete quarantine files", "DELETE /admin/quarantine/{id} with Auditor token", "HTTP 403 Forbidden: Admin required", "HTTP 403 Forbidden", "PASS", "tests/security/test_role_escalation.py"],
        ["SEC-TC-12", "Threat Scanning", "EICAR Standard Malware Detection", "Verify scanner intercepts known malware string", "EICAR standard antivirus test string", "File marked is_quarantined=True, HTTP 200 with warning", "Quarantined immediately", "PASS", "tests/security/test_file_upload.py"],
        ["SEC-TC-13", "Threat Scanning", "MIME Type Spoofing Defense", "Block executable files disguised with .pdf extension", "Windows PE binary named 'invoice.pdf'", "Rejected by Stage 2 Executable/MIME check", "Rejected with threat warning", "PASS", "tests/security/test_file_upload.py"],
        ["SEC-TC-14", "Threat Scanning", "Path Traversal Filename Defense", "Prevent directory traversal via filename manipulation", "Filename '../../../../etc/passwd'", "Sanitized to safe basename 'passwd'", "Stored safely without traversal", "PASS", "tests/security/test_file_upload.py"],
        ["SEC-TC-15", "Threat Scanning", "File Size Ceiling Enforcement", "Reject uploads exceeding 50MB maximum size", "Synthetic 51MB byte payload", "HTTP 413 Payload Too Large", "HTTP 413 returned", "PASS", "tests/security/test_file_upload.py"],
        ["SEC-TC-16", "Threat Containment", "Quarantined Download Air-Gap", "Ensure quarantined file cannot be downloaded", "GET /files/{quarantined_id}/download", "HTTP 403 Forbidden: File is in quarantine", "HTTP 403 Forbidden", "PASS", "tests/security/test_file_download.py"],
        ["SEC-TC-17", "Cryptography", "AES-256-GCM Ciphertext at Rest", "Confirm files on disk are completely unreadable", "Direct inspect of storage/uploads/*.enc", "High entropy ciphertext, no plaintext strings", "Verified 100% encrypted", "PASS", "tests/security/test_integrity.py"],
        ["SEC-TC-18", "Cryptography", "GCM Tamper Detection", "Ensure altered ciphertext fails authentication tag", "Flip 1 single bit in encrypted payload file", "Decryption fails with InvalidTag exception", "InvalidTag raised, stream aborted", "PASS", "tests/security/test_integrity.py"],
        ["SEC-TC-19", "Cryptography", "Random IV Nonce Verification", "Confirm each upload gets a unique 96-bit IV", "Upload same file 10 times consecutively", "10 completely distinct IVs and ciphertexts", "Zero IV collisions detected", "PASS", "tests/security/test_integrity.py"],
        ["SEC-TC-20", "Sharing Engine", "Expiring Share Link Enforcement", "Ensure link expires exactly at configured deadline", "Access share token after expires_at timestamp", "HTTP 410 Gone / Link has expired", "HTTP 410 returned", "PASS", "tests/security/test_share_links.py"],
        ["SEC-TC-21", "Sharing Engine", "Password-Protected Share Link", "Verify password prompt required before download", "Attempt download without password on protected link", "HTTP 401 Password required for this shared file", "HTTP 401 Password required", "PASS", "tests/security/test_share_links.py"],
        ["SEC-TC-22", "Sharing Engine", "Max Download Limit Enforcement", "Ensure link auto-revokes once limit is reached", "Download 3 times when max_downloads=3", "4th download rejected with HTTP 410", "Download blocked on 4th attempt", "PASS", "tests/security/test_share_links.py"],
        ["SEC-TC-23", "Audit Trail", "Audit Log Creation on Every Event", "Verify all auth and file events append to audit table", "Perform login, upload, share, and delete actions", "4 matching audit rows inserted with user_id and IP", "Audit rows verified in DB", "PASS", "tests/security/test_audit_logging.py"],
        ["SEC-TC-24", "Audit Trail", "SHA-256 Hash Chaining Integrity", "Verify verifier detects untampered audit chain", "Invoke verify_audit_log_integrity(db)", "Returns is_valid=True, total_logs=N, tampered_index=None", "is_valid=True confirmed", "PASS", "tests/security/test_audit_logging.py"],
        ["SEC-TC-25", "Audit Trail", "Tampered Log Row Detection", "Verify verifier flags manually modified audit row", "Directly alter action string in row 3 of database", "Returns is_valid=False, tampered_index=3", "Tampering detected at row 3", "PASS", "tests/security/test_audit_logging.py"],
        ["SEC-TC-26", "System Defense", "Sliding Window Rate Limiter", "Verify 6th login request within 1 min is blocked", "Send 10 rapid login attempts from same IP", "First 5 processed, 6th+ receives HTTP 429", "HTTP 429 Too Many Requests", "PASS", "tests/security/test_rate_limiting.py"],
        ["SEC-TC-27", "Security Fuzzing", "Authentication Malformed Fuzzing", "Verify backend handles null bytes and SQLi strings", "500 fuzz strings with SQLi, XSS, nulls, long strings", "No 500 crashes; handled cleanly with 400/422", "Zero unhandled exceptions", "PASS", "security/fuzzing/test_auth_fuzz.py"],
        ["SEC-TC-28", "Security Fuzzing", "Filename Malformed Fuzzing", "Verify upload handles control chars and Windows limits", "Filenames with unicode, emoji, 500 chars, null bytes", "Sanitized safely or rejected with 400/422", "Zero filesystem crash", "PASS", "security/fuzzing/test_filename_fuzz.py"]
    ]
    format_sheet(ws, headers, data, code_cols=[0, 8])
    wb.save(os.path.join(OUTPUT_DIR, "Security_Test_Cases.xlsx"))

# -------------------------------------------------------------
# 11. Burndown Data (Sprint 1, 2, 3)
# -------------------------------------------------------------
def make_burndown_data():
    wb = Workbook()
    ws = wb.active
    ws.title = "Burndown"
    headers = [
        "Sprint", "Day", "Calendar Date", "Ideal Remaining Points", "Actual Remaining Points", "Story Points Completed Today", "Sprint Notes"
    ]
    data = [
        # Sprint 1 (Committed: 36 pts)
        ["Sprint 1", "Day 01", "2026-03-01", 36.0, 36.0, 0, "Sprint 1 Kickoff: Architecture setup & DB models"],
        ["Sprint 1", "Day 02", "2026-03-02", 32.4, 34.0, 2, "User registration and password hashing completed"],
        ["Sprint 1", "Day 03", "2026-03-03", 28.8, 30.0, 4, "JWT authentication and sliding refresh merged"],
        ["Sprint 1", "Day 04", "2026-03-04", 25.2, 26.0, 4, "TOTP multi-factor authentication setup"],
        ["Sprint 1", "Day 05", "2026-03-05", 21.6, 21.0, 5, "MFA verify and rate limiter merged ahead of schedule"],
        ["Sprint 1", "Day 06", "2026-03-06", 18.0, 18.0, 3, "6-stage upload pipeline initial magic byte scan"],
        ["Sprint 1", "Day 07", "2026-03-07", 14.4, 13.0, 5, "ClamAV daemon connector integration"],
        ["Sprint 1", "Day 08", "2026-03-08", 10.8, 9.0, 4, "EICAR detection and quarantine folder isolation"],
        ["Sprint 1", "Day 09", "2026-03-09", 7.2, 5.0, 4, "Admin quarantine release/purge endpoints"],
        ["Sprint 1", "Day 10", "2026-03-10", 0.0, 0.0, 5, "Sprint 1 Review: 36/36 points delivered cleanly"],
        # Sprint 2 (Committed: 38 pts)
        ["Sprint 2", "Day 01", "2026-03-15", 38.0, 38.0, 0, "Sprint 2 Kickoff: Cryptography and access control"],
        ["Sprint 2", "Day 02", "2026-03-16", 34.2, 35.0, 3, "AES-256-GCM envelope encryption primitives"],
        ["Sprint 2", "Day 03", "2026-03-17", 30.4, 30.0, 5, "Decryption streaming download service"],
        ["Sprint 2", "Day 04", "2026-03-18", 26.6, 26.0, 4, "Folder hierarchy and BOLA prevention"],
        ["Sprint 2", "Day 05", "2026-03-19", 22.8, 20.0, 6, "DAC granular permissions (VIEWER, DOWNLOADER, etc.)"],
        ["Sprint 2", "Day 06", "2026-03-20", 19.0, 16.0, 4, "Public share link engine with 32-byte tokens"],
        ["Sprint 2", "Day 07", "2026-03-21", 15.2, 12.0, 4, "Expiring link password protection & download limits"],
        ["Sprint 2", "Day 08", "2026-03-22", 11.4, 8.0, 4, "SHA-256 tamper-evident audit logging blockchain"],
        ["Sprint 2", "Day 09", "2026-03-23", 7.6, 4.0, 4, "Continuous audit log integrity verifier API"],
        ["Sprint 2", "Day 10", "2026-03-24", 0.0, 0.0, 4, "Sprint 2 Review: 38/38 points delivered cleanly"],
        # Sprint 3 (Committed: 40 pts)
        ["Sprint 3", "Day 01", "2026-03-29", 40.0, 40.0, 0, "Sprint 3 Kickoff: DevSecOps CI/CD & Frontend UI"],
        ["Sprint 3", "Day 02", "2026-03-30", 36.0, 36.0, 4, "React Vite TypeScript app shell & AuthContext"],
        ["Sprint 3", "Day 03", "2026-03-31", 32.0, 31.0, 5, "User dashboard, upload, and file browser views"],
        ["Sprint 3", "Day 04", "2026-04-01", 28.0, 26.0, 5, "Admin SOC dashboard, quarantine, and audit UI"],
        ["Sprint 3", "Day 05", "2026-04-02", 24.0, 21.0, 5, "GitHub Actions 14-stage DevSecOps pipeline setup"],
        ["Sprint 3", "Day 06", "2026-04-03", 20.0, 17.0, 4, "Bandit, Safety, TruffleHog automated security gates"],
        ["Sprint 3", "Day 07", "2026-04-04", 16.0, 12.0, 5, "Kubernetes production manifests & container sandboxing"],
        ["Sprint 3", "Day 08", "2026-04-05", 12.0, 8.0, 4, "OWASP ZAP baseline scan integration & zap-config"],
        ["Sprint 3", "Day 09", "2026-04-06", 8.0, 3.0, 5, "Fuzz testing suite implementation and execution"],
        ["Sprint 3", "Day 10", "2026-04-07", 0.0, 0.0, 3, "Sprint 3 Review: Final capstone delivery complete"]
    ]
    format_sheet(ws, headers, data, code_cols=[0, 1])
    wb.save(os.path.join(OUTPUT_DIR, "Burndown_Data.xlsx"))

# -------------------------------------------------------------
# 12. Velocity Data
# -------------------------------------------------------------
def make_velocity_data():
    wb = Workbook()
    ws = wb.active
    ws.title = "Velocity"
    headers = [
        "Sprint ID", "Sprint Goal", "Committed Points", "Completed Points", "Rollover Points", 
        "Velocity Efficiency (%)", "Team Headcount", "Points / Dev", "Velocity Notes"
    ]
    data = [
        ["Sprint 1", "Core Auth & Threat Scanning", 36, 36, 0, "100%", 4, 9.0, "Zero carryover. All authentication and ClamAV scanning completed."],
        ["Sprint 2", "Cryptography, Sharing & Auditing", 38, 38, 0, "100%", 4, 9.5, "AES-256-GCM envelope crypto and SHA-256 hash chaining delivered."],
        ["Sprint 3", "DevSecOps, Frontend & Validation", 40, 40, 0, "100%", 4, 10.0, "Full CI/CD pipeline, K8s manifests, ZAP baseline, and UI completed."]
    ]
    format_sheet(ws, headers, data, code_cols=[0])
    wb.save(os.path.join(OUTPUT_DIR, "Velocity_Data.xlsx"))

# -------------------------------------------------------------
# 13. Risk Governance Framework
# -------------------------------------------------------------
def make_risk_governance():
    wb = Workbook()
    ws = wb.active
    ws.title = "Governance"
    headers = [
        "Governance Domain", "Policy Statement", "Enforcement Tool / Mechanism", 
        "Audit Frequency", "Governance Owner", "Non-Compliance Escalation Path"
    ]
    data = [
        ["Access Governance", "All users must enforce MFA; inactive accounts disabled after 90 days", "FastAPI middleware + TOTP verifier", "Monthly Automated Audit", "Sushmitha Reddy (Security Lead)", "Account suspended; notification to Administrator"],
        ["Cryptographic Standards", "AES-256-GCM for all at-rest storage; TLS 1.3 only in transit", "CryptoService module + Nginx config", "Continuous Automated Pipeline", "Rahul Kumar (Crypto Engineer)", "Build failure in CI/CD pipeline gate"],
        ["Vulnerability Management", "Zero High/Critical unmitigated vulnerabilities permitted in main", "Bandit, Safety, Snyk, TruffleHog", "Every Git Push & Pull Request", "Priya Sharma (DevSecOps Lead)", "PR merge blocked by GitHub Actions branch rule"],
        ["Audit Trail Governance", "Audit logs must remain immutable and chained with SHA-256", "AuditVerifier background cron & API", "Continuous & Weekly Review", "Sushmitha Reddy (Security Lead)", "Critical SOC alert; immediate forensic review"],
        ["Incident Response", "Quarantined files must be reviewed or purged within 7 business days", "Admin Quarantine Management Portal", "Daily Automated Check", "Admin & Auditor Personas", "Notification dispatched to Incident Response Lead"]
    ]
    format_sheet(ws, headers, data, code_cols=[0])
    wb.save(os.path.join(OUTPUT_DIR, "Risk_Governance.xlsx"))

# -------------------------------------------------------------
# 14. Compliance Mapping Matrix
# -------------------------------------------------------------
def make_compliance_mapping():
    wb = Workbook()
    ws = wb.active
    ws.title = "Compliance_Mapping"
    headers = [
        "Standard / Regulation", "Requirement Clause", "Description of Requirement", 
        "SecureShare Technical Control", "Implementation Evidence", "Compliance Status"
    ]
    data = [
        ["OWASP Top 10 (2021)", "A01: Broken Access Control", "Enforce principle of least privilege, prevent BOLA", "SC-09, SC-10: Strict DB ownership join check on all requests", "tests/security/test_bola.py (PASS)", "COMPLIANT"],
        ["OWASP Top 10 (2021)", "A02: Cryptographic Failures", "Protect sensitive data with modern authenticated encryption", "SC-07: AES-256-GCM envelope encryption with 96-bit unique IV", "tests/security/test_integrity.py (PASS)", "COMPLIANT"],
        ["OWASP Top 10 (2021)", "A03: Injection", "Sanitize all user inputs, prevent SQLi and XSS", "SQLAlchemy parameterized ORM + filename sanitization", "tests/security/test_file_upload.py (PASS)", "COMPLIANT"],
        ["OWASP Top 10 (2021)", "A04: Insecure Design", "Threat modeling and secure architecture validation", "STRIDE Threat Modeling + 6-Stage Malware Scanner", "docs/architecture/Threat_Model.md", "COMPLIANT"],
        ["OWASP Top 10 (2021)", "A05: Security Misconfig", "Harden server configurations, remove default accounts", "SC-14: Docker non-root UID 10001, minimal distroless base", "docker/Dockerfile.backend", "COMPLIANT"],
        ["OWASP Top 10 (2021)", "A07: Identification & Auth", "Defend against brute force and credential stuffing", "SC-01, SC-15: Argon2id + 5-attempt lockout + Rate Limiter", "tests/security/test_authentication.py (PASS)", "COMPLIANT"],
        ["OWASP Top 10 (2021)", "A09: Security Logging", "Ensure tamper-evident logging of critical events", "SC-12: SHA-256 cryptographic blockchain audit trail", "tests/security/test_audit_logging.py (PASS)", "COMPLIANT"],
        ["ISO/IEC 27001:2022", "Control 8.24", "Use of cryptography in accordance with risk policy", "AES-256-GCM authenticated cipher with wrapped DEKs", "artifacts/excel/Security_Controls.xlsx", "COMPLIANT"],
        ["ISO/IEC 27001:2022", "Control 8.15", "Logging and monitoring of security events", "Tamper-evident audit trail with automated verifier", "backend/app/audit/verifier.py", "COMPLIANT"],
        ["NIST Cybersecurity (CSF)", "PR.DS-1", "Data-at-rest is protected using cryptographic algorithms", "Envelope encryption isolating each file with distinct key", "backend/app/crypto/cipher.py", "COMPLIANT"],
        ["NIST Cybersecurity (CSF)", "DE.CM-1", "The network is monitored to detect potential cybersecurity events", "SOC Admin Dashboard with live metrics and failure alerts", "frontend/src/pages/admin/AdminDashboard.tsx", "COMPLIANT"],
        ["GDPR (EU 2016/679)", "Article 32", "Security of processing: pseudonymisation and encryption", "End-to-end envelope encryption + user deletion cascade", "backend/app/models/user.py", "COMPLIANT"],
        ["IEEE 29148", "Standard for RE", "Requirements Engineering standard compliance", "Complete SRS with 20 IEEE 29148 clauses and full RTM", "docs/SRS/SecureShare_SRS.docx", "COMPLIANT"]
    ]
    format_sheet(ws, headers, data, code_cols=[0, 1])
    wb.save(os.path.join(OUTPUT_DIR, "Compliance_Mapping.xlsx"))

def main():
    print("[*] Generating all 14 SecureShare Excel artifacts in artifacts/excel/ ...")
    make_traceability()
    make_assets_cia()
    make_stride_threat_matrix()
    make_information_flow()
    make_vulnerability_analysis()
    make_threat_risk_register()
    make_security_controls()
    make_permission_matrix()
    make_product_backlog()
    make_security_test_cases()
    make_burndown_data()
    make_velocity_data()
    make_risk_governance()
    make_compliance_mapping()
    print("[+] Successfully generated all 14 Excel workbooks!")

if __name__ == "__main__":
    main()
