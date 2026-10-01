# Snyk Software Composition Analysis (SCA) & Container Scanning

## 1. Overview
SecureShare integrates Snyk into its continuous security lifecycle to monitor open-source dependencies (Python wheels and npm packages) and Docker container base images for known Common Vulnerabilities and Exposures (CVEs).

---

## 2. Installation & Authentication

```bash
# Install Snyk CLI globally
npm install -g snyk

# Authenticate Snyk with your developer account
snyk auth
```

---

## 3. Running Scans

### 3.1 Python Backend Dependency Scan
```bash
cd backend
snyk test --file=requirements.txt
```

### 3.2 Frontend NPM Dependency Scan
```bash
cd frontend
snyk test
```

### 3.3 Container Image Vulnerability Scan
```bash
# Test the backend Docker container image
snyk container test secureshare-backend:latest --file=docker/Dockerfile.backend
```

---

## 4. Continuous Monitoring in CI/CD
Snyk is monitored automatically in the GitHub Actions workflow using the official action:

```yaml
- name: Run Snyk to check for vulnerabilities
  uses: snyk/actions/python@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    args: --severity-threshold=high
```

---

## 5. Security Posture
- **Zero High/Critical Dependency CVEs**: All production packages are pinned to hardened, patched versions.
- **Minimal Distroless / Alpine Base**: Minimizes attack surface by removing package managers, shells, and unnecessary utilities from final container images.
