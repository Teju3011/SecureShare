#!/usr/bin/env bash
# OWASP ZAP Automated Baseline Scan for SecureShare
set -e

TARGET_URL="${1:-http://localhost:8000}"
REPORT_DIR="$(pwd)/security/reports"
mkdir -p "$REPORT_DIR"

echo "=========================================================="
echo "Starting OWASP ZAP Baseline Security Scan on $TARGET_URL"
echo "=========================================================="

docker run --rm -v "$REPORT_DIR":/zap/wrk/:rw \
  -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
  -t "$TARGET_URL" \
  -g zap-config.yaml \
  -r zap_report.html \
  -J zap_report.json \
  -m 3 || true

echo "[+] OWASP ZAP Baseline scan complete! Reports generated in $REPORT_DIR"
