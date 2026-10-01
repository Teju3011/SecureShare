# Logging, Audit Trails & SOC Monitoring Architecture

## 1. Overview
SecureShare implements a tamper-evident audit logging architecture designed to satisfy ISO/IEC 27001 Control 8.15 and NIST SP 800-53 AU-9. Every security-relevant event produces an immutable cryptographic record chained to preceding events using SHA-256 hashing.

---

## 2. Event Types Captured

| Event Category | Action String | Captured Metadata |
| :--- | :--- | :--- |
| **Authentication** | `USER_LOGIN_SUCCESS`, `USER_LOGIN_FAILURE`, `USER_LOGOUT`, `MFA_SETUP`, `MFA_VERIFIED` | Actor IP, User-Agent, Email, Timestamp |
| **File Lifecycle** | `FILE_UPLOAD_CLEAN`, `FILE_QUARANTINED`, `FILE_DOWNLOADED`, `FILE_DELETED` | File ID, SHA-256 Checksum, MIME Type, Threat Name |
| **Access Control** | `PERMISSION_GRANTED`, `PERMISSION_REVOKED`, `ROLE_UPDATED`, `ACCOUNT_STATUS_CHANGED` | Target User, Preset Granted, Acting Admin |
| **Public Sharing** | `SHARE_LINK_CREATED`, `SHARE_LINK_ACCESSED`, `SHARE_LINK_REVOKED` | Token Prefix, Expiry, Max Downloads |
| **Admin Operations**| `QUARANTINE_RELEASE`, `QUARANTINE_PURGE`, `AUDIT_VERIFIED`, `PIPELINE_TRIGGERED` | Target Resource ID, Discrepancy Flag |

---

## 3. Cryptographic Blockchain Hash Chaining
Each audit log row contains:
- `prev_hash`: The `log_hash` of the immediately preceding record in chronological sequence.
- `log_hash`: Computed as:
  ```python
  payload = f"{prev_hash}:{actor_id}:{action}:{resource_type}:{resource_id}:{ip_address}:{status}:{timestamp}"
  log_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
  ```

### Continuous Verification
The verification engine (`backend/app/audit/verifier.py`) performs sequential recalculation of the expected hash chain:
1. Detects any row deletion (broken sequence ID or mismatched `prev_hash`).
2. Detects any row alteration (mismatched `log_hash`).
3. Detects any row insertion out of sequence.

---

## 4. SOC Admin Live Telemetry
The SOC Admin Dashboard provides:
- Live aggregate event stream.
- One-click cryptographic verification of the complete ledger.
- Real-time alerts for failed logins and quarantined malware uploads.
- Forensic investigation views filtering by action type, user, or IP address.
