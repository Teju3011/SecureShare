# OWASP ZAP Dynamic Application Security Testing (DAST)

## 1. Overview
OWASP Zed Attack Proxy (ZAP) is an open-source web application security scanner used in SecureShare to perform runtime automated vulnerability assessments against the live application stack.

---

## 2. Configuration & Exclusions
The baseline scan rules are defined in `security/zap/zap-config.yaml`. The scan tests for:
- SQL Injection in query strings and JSON payloads
- Cross-Site Scripting (Reflected & Stored XSS)
- Missing Anti-Clickjacking headers (`X-Frame-Options`)
- Missing Content Security Policy (`CSP`)
- Insecure Cookie attributes (`HttpOnly`, `SameSite`, `Secure`)
- Path Traversal and Information Leakage via HTTP headers

---

## 3. Running the Automated ZAP Scan

### 3.1 Via Local Bash Script
```bash
# Start the SecureShare application
docker compose up -d

# Execute the automated baseline scan
./security/zap/zap-baseline.sh http://localhost:8000
```

### 3.2 Via Docker Directly
```bash
docker run --rm -v $(pwd)/security/reports:/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
  -t http://host.docker.internal:8000 \
  -g zap-config.yaml \
  -r zap_report.html \
  -J zap_report.json
```

---

## 4. Scan Artifacts & Reports
Reports are written directly to `security/reports/`:
- `zap_report.html`: Interactive executive and technical summary.
- `zap_report.json`: Machine-readable findings parsed by the SOC Admin dashboard.
- **Current Baseline Status**: 0 High Alerts, 0 Medium Alerts.
