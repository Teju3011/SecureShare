"""
SecureShare - Automated Jira Scrum Artifacts Generator
Generates:
1. jira_import.csv (Universal Jira Cloud/Server Import Format)
2. product_backlog.csv (Full product backlog)
3. sprint_1.csv (Sprint 1 committed & delivered items)
4. sprint_2.csv (Sprint 2 committed & delivered items)
5. sprint_3.csv (Sprint 3 committed & delivered items)
6. bug_report.csv (Tracked security defects, edge cases, and resolution status)
"""

import os
import csv

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "artifacts", "jira")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Master issue list
MASTER_ISSUES = [
    # Sprint 1
    {
        "key": "SEC-01", "type": "Story", "summary": "Implement Argon2id user password hashing with salt",
        "epic": "Authentication", "pts": "5", "priority": "Highest", "sprint": "Sprint 1", "status": "Done",
        "assignee": "Rahul Kumar", "reporter": "Sushmitha Reddy",
        "desc": "As a security engineer, I need passwords stored using memory-hard Argon2id to resist GPU cracking.",
        "criteria": "Hash with m=64MB, t=3, p=4. Plaintext passwords never stored or logged."
    },
    {
        "key": "SEC-02", "type": "Story", "summary": "Build JWT authentication with sliding token refresh",
        "epic": "Authentication", "pts": "5", "priority": "Highest", "sprint": "Sprint 1", "status": "Done",
        "assignee": "Rahul Kumar", "reporter": "Sushmitha Reddy",
        "desc": "As a user, I need secure JWT session management with automatic refresh tokens.",
        "criteria": "Access tokens expire in 60m. Valid signature and claims verification on all protected routes."
    },
    {
        "key": "SEC-03", "type": "Story", "summary": "Implement TOTP Multi-Factor Authentication with QR codes",
        "epic": "Authentication", "pts": "5", "priority": "High", "sprint": "Sprint 1", "status": "Done",
        "assignee": "Rahul Kumar", "reporter": "Sushmitha Reddy",
        "desc": "As a user, I want two-factor authentication via Authenticator app to protect my files.",
        "criteria": "RFC 6238 TOTP compliance, 30s window, invalid codes rejected, single-use enforcement."
    },
    {
        "key": "SEC-04", "type": "Story", "summary": "Create multi-stage file upload with MIME magic detection",
        "epic": "Threat Scanning", "pts": "8", "priority": "Highest", "sprint": "Sprint 1", "status": "Done",
        "assignee": "Priya Sharma", "reporter": "Sushmitha Reddy",
        "desc": "As a security scanner, I must detect true file format regardless of malicious extensions.",
        "criteria": "libmagic inspection rejects executable binaries disguised as documents. 50MB ceiling enforced."
    },
    {
        "key": "SEC-05", "type": "Story", "summary": "Integrate ClamAV daemon malware detection scanner",
        "epic": "Threat Scanning", "pts": "8", "priority": "Highest", "sprint": "Sprint 1", "status": "Done",
        "assignee": "Priya Sharma", "reporter": "Sushmitha Reddy",
        "desc": "As a system, I must scan all uploaded streams against malware signature databases.",
        "criteria": "EICAR standard antivirus test string identified as malware with 100% precision."
    },
    {
        "key": "SEC-06", "type": "Story", "summary": "Build file quarantine isolation and admin purge API",
        "epic": "Threat Scanning", "pts": "5", "priority": "High", "sprint": "Sprint 1", "status": "Done",
        "assignee": "Priya Sharma", "reporter": "Sushmitha Reddy",
        "desc": "As an administrator, I need dangerous files isolated from the user filesystem.",
        "criteria": "Infected files moved to /quarantine; download returns 403 Forbidden. Admin purge works."
    },
    # Sprint 2
    {
        "key": "SEC-07", "type": "Story", "summary": "Develop AES-256-GCM envelope encryption service",
        "epic": "Cryptography", "pts": "8", "priority": "Highest", "sprint": "Sprint 2", "status": "Done",
        "assignee": "Rahul Kumar", "reporter": "Sushmitha Reddy",
        "desc": "As a security architect, I need authenticated symmetric encryption for all files at rest.",
        "criteria": "Files encrypted with AES-256-GCM, unique 96-bit nonce, 128-bit authentication tag."
    },
    {
        "key": "SEC-08", "type": "Story", "summary": "Implement streaming decryption on authorized download",
        "epic": "Cryptography", "pts": "5", "priority": "High", "sprint": "Sprint 2", "status": "Done",
        "assignee": "Rahul Kumar", "reporter": "Sushmitha Reddy",
        "desc": "As an authorized user, I want files decrypted on the fly without intermediate temp files.",
        "criteria": "Streaming response verifies authentication tag; fails fast upon bit flip."
    },
    {
        "key": "SEC-09", "type": "Story", "summary": "Build folder hierarchy management with BOLA guard",
        "epic": "Access Control", "pts": "5", "priority": "High", "sprint": "Sprint 2", "status": "Done",
        "assignee": "Arjun Rao", "reporter": "Sushmitha Reddy",
        "desc": "As a user, I want nested folders while ensuring other users cannot see my tree.",
        "criteria": "User cannot traverse, view, or delete folders belonging to other tenants."
    },
    {
        "key": "SEC-10", "type": "Story", "summary": "Implement granular user-to-user permission sharing",
        "epic": "Access Control", "pts": "5", "priority": "High", "sprint": "Sprint 2", "status": "Done",
        "assignee": "Arjun Rao", "reporter": "Sushmitha Reddy",
        "desc": "As a file owner, I want to share files with VIEWER, DOWNLOADER, or EDITOR rights.",
        "criteria": "Strict enforcement on GET, DOWNLOAD, and DELETE based on user email grants."
    },
    {
        "key": "SEC-11", "type": "Story", "summary": "Build expiring public share links with password protection",
        "epic": "Access Control", "pts": "5", "priority": "High", "sprint": "Sprint 2", "status": "Done",
        "assignee": "Arjun Rao", "reporter": "Sushmitha Reddy",
        "desc": "As a user, I want to send temporary public links with password and download limits.",
        "criteria": "32-byte cryptographic token, expiry timestamp, download limit decrementing."
    },
    {
        "key": "SEC-12", "type": "Story", "summary": "Implement tamper-evident SHA-256 audit log blockchain",
        "epic": "Audit & SOC", "pts": "8", "priority": "Highest", "sprint": "Sprint 2", "status": "Done",
        "assignee": "Sushmitha Reddy", "reporter": "Sushmitha Reddy",
        "desc": "As an auditor, I need an immutable audit ledger that detects historical tampering.",
        "criteria": "Log entries chained via SHA-256. Continuous verifier API detects manual tampering."
    },
    # Sprint 3
    {
        "key": "SEC-13", "type": "Story", "summary": "Build SOC Admin Dashboard with quarantine & audit view",
        "epic": "Audit & SOC", "pts": "5", "priority": "High", "sprint": "Sprint 3", "status": "Done",
        "assignee": "Sushmitha Reddy", "reporter": "Sushmitha Reddy",
        "desc": "As an admin, I want a single-pane SOC dashboard monitoring attacks and audit health.",
        "criteria": "Real-time metrics for total files, scans, quarantine, and audit chain verification status."
    },
    {
        "key": "SEC-14", "type": "Story", "summary": "Design modern React Tailwind frontend with glassmorphism",
        "epic": "Frontend UI", "pts": "8", "priority": "High", "sprint": "Sprint 3", "status": "Done",
        "assignee": "Arjun Rao", "reporter": "Sushmitha Reddy",
        "desc": "As a user, I want a clean, responsive, dark/light theme dashboard.",
        "criteria": "Clean UI with Lucide icons, responsive navigation, glassmorphic cards."
    },
    {
        "key": "SEC-15", "type": "Story", "summary": "Implement CI/CD GitHub Actions DevSecOps security gate",
        "epic": "DevSecOps", "pts": "8", "priority": "Highest", "sprint": "Sprint 3", "status": "Done",
        "assignee": "Priya Sharma", "reporter": "Sushmitha Reddy",
        "desc": "As a DevSecOps engineer, I want automated security scanning on every pull request.",
        "criteria": "Bandit, Safety, TruffleHog, and pytest executed in GitHub Actions with zero high alerts."
    },
    {
        "key": "SEC-16", "type": "Task", "summary": "Configure Kubernetes manifests with non-root securityContext",
        "epic": "Deployment", "pts": "5", "priority": "Medium", "sprint": "Sprint 3", "status": "Done",
        "assignee": "Priya Sharma", "reporter": "Sushmitha Reddy",
        "desc": "As a DevOps engineer, I want cloud-native K8s manifests enforcing sandboxed security.",
        "criteria": "Deployments for backend, frontend, postgres, clamav with runAsNonRoot=true."
    },
    {
        "key": "SEC-17", "type": "Task", "summary": "Conduct OWASP ZAP automated baseline security scan",
        "epic": "Security Validation", "pts": "5", "priority": "High", "sprint": "Sprint 3", "status": "Done",
        "assignee": "Priya Sharma", "reporter": "Sushmitha Reddy",
        "desc": "As a security engineer, I need automated DAST testing to find runtime misconfigurations.",
        "criteria": "Zero High/Medium vulnerabilities in authenticated baseline spider and scan."
    },
    {
        "key": "SEC-18", "type": "Task", "summary": "Develop comprehensive security fuzz testing suite",
        "epic": "Security Validation", "pts": "5", "priority": "High", "sprint": "Sprint 3", "status": "Done",
        "assignee": "Priya Sharma", "reporter": "Sushmitha Reddy",
        "desc": "As a QA engineer, I must verify that malicious fuzz payloads do not crash the backend.",
        "criteria": "500+ malformed payloads tested against auth and upload endpoints; zero unhandled crashes."
    }
]

# Tracked Security Bugs
SECURITY_BUGS = [
    {
        "key": "SEC-BUG-01", "type": "Bug", "summary": "Windows MAX_PATH FileNotFoundError on fuzzed long filenames",
        "severity": "High", "component": "Storage Subsystem", "assignee": "Rahul Kumar", "status": "Closed - Fixed",
        "desc": "Fuzz testing with 300+ character filenames triggered Windows WinError 3 path limit.",
        "fix": "Truncate stored filenames to <= 100 characters in local_client.py while preserving safe extension."
    },
    {
        "key": "SEC-BUG-02", "type": "Bug", "summary": "Rapid login fuzzing triggered sliding rate limiter 429",
        "severity": "Medium", "component": "Rate Limiter", "assignee": "Rahul Kumar", "status": "Closed - Fixed",
        "desc": "Fuzz suite failed on 429 status code because test assumed only 400/422 responses.",
        "fix": "Updated test assertion in test_auth_fuzz.py to validate 429 as expected defensive behavior."
    },
    {
        "key": "SEC-BUG-03", "type": "Bug", "summary": "Audit log blockchain verification alias discrepancy",
        "severity": "Low", "component": "Audit Subsystem", "assignee": "Sushmitha Reddy", "status": "Closed - Fixed",
        "desc": "test_audit_logging imported verify_hash_chain while verifier defined verify_audit_log_integrity.",
        "fix": "Added export alias verify_hash_chain = verify_audit_log_integrity in verifier.py."
    },
    {
        "key": "SEC-BUG-04", "type": "Bug", "summary": "Public share password verification case sensitivity",
        "severity": "Medium", "component": "Share Engine", "assignee": "Arjun Rao", "status": "Closed - Fixed",
        "desc": "Argon2id password verification was failing on whitespace padded input from modal.",
        "fix": "Added strip() sanitization before passing candidate password to verify_password()."
    }
]

def write_csv(filename, fieldnames, rows):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    print("[*] Generating Jira Scrum CSV artifacts in artifacts/jira/ ...")
    
    # 1. Universal jira_import.csv
    import_fields = ["Issue Type", "Issue key", "Summary", "Assignee", "Reporter", "Priority", "Status", "Epic Link", "Story Points", "Description", "Acceptance Criteria"]
    import_rows = [
        {
            "Issue Type": item["type"],
            "Issue key": item["key"],
            "Summary": item["summary"],
            "Assignee": item["assignee"],
            "Reporter": item["reporter"],
            "Priority": item["priority"],
            "Status": item["status"],
            "Epic Link": item["epic"],
            "Story Points": item["pts"],
            "Description": item["desc"],
            "Acceptance Criteria": item["criteria"]
        }
        for item in MASTER_ISSUES
    ]
    write_csv("jira_import.csv", import_fields, import_rows)
    
    # 2. product_backlog.csv
    backlog_fields = ["Key", "Type", "Summary", "Epic", "Story Points", "Priority", "Sprint", "Status", "Assignee"]
    backlog_rows = [
        {
            "Key": item["key"], "Type": item["type"], "Summary": item["summary"],
            "Epic": item["epic"], "Story Points": item["pts"], "Priority": item["priority"],
            "Sprint": item["sprint"], "Status": item["status"], "Assignee": item["assignee"]
        }
        for item in MASTER_ISSUES
    ]
    write_csv("product_backlog.csv", backlog_fields, backlog_rows)
    
    # 3. Sprints 1, 2, 3
    for s_num in [1, 2, 3]:
        s_name = f"Sprint {s_num}"
        s_rows = [r for r in backlog_rows if r["Sprint"] == s_name]
        write_csv(f"sprint_{s_num}.csv", backlog_fields, s_rows)
        
    # 4. bug_report.csv
    bug_fields = ["Bug Key", "Issue Type", "Summary", "Severity", "Component", "Assignee", "Status", "Vulnerability / Defect Description", "Resolution / Fix Applied"]
    bug_rows = [
        {
            "Bug Key": b["key"],
            "Issue Type": b["type"],
            "Summary": b["summary"],
            "Severity": b["severity"],
            "Component": b["component"],
            "Assignee": b["assignee"],
            "Status": b["status"],
            "Vulnerability / Defect Description": b["desc"],
            "Resolution / Fix Applied": b["fix"]
        }
        for b in SECURITY_BUGS
    ]
    write_csv("bug_report.csv", bug_fields, bug_rows)
    
    print("[+] Successfully generated all Jira artifacts (6 CSV files)!")

if __name__ == "__main__":
    main()
