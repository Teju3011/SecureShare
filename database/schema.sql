-- ==============================================================================
-- SECURESHARE - Complete PostgreSQL / Relational Schema
-- Standard: Conforms to IEEE 29148 Data Architecture & Zero-Trust Access Control
-- ==============================================================================

-- 1. USER TABLE
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(32) NOT NULL DEFAULT 'USER', -- 'USER', 'ADMIN', 'SECURITY_AUDITOR'
    account_status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE', -- 'ACTIVE', 'SUSPENDED', 'DISABLED'
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    mfa_secret VARCHAR(64),
    mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- 2. FOLDER TABLE (Organization & Hierarchy)
CREATE TABLE IF NOT EXISTS folders (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    parent_folder_id INTEGER REFERENCES folders(id) ON DELETE CASCADE,
    folder_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_folders_owner ON folders(owner_id);
CREATE INDEX IF NOT EXISTS idx_folders_parent ON folders(parent_folder_id);

-- 3. FILE TABLE (Storage, Status, Encryption at Rest)
CREATE TABLE IF NOT EXISTS files (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    folder_id INTEGER REFERENCES folders(id) ON DELETE SET NULL,
    original_filename VARCHAR(255) NOT NULL,
    stored_filename VARCHAR(255) NOT NULL UNIQUE,
    file_size BIGINT NOT NULL,
    declared_mime VARCHAR(128) NOT NULL,
    detected_mime VARCHAR(128) NOT NULL,
    magic_bytes_preview VARCHAR(64),
    sha256_hash VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'UPLOADING', -- 'UPLOADING','VALIDATING','SCANNING','CLEAN','HIGH_RISK','MALICIOUS','QUARANTINED','FAILED'
    storage_path VARCHAR(512) NOT NULL,
    is_quarantined BOOLEAN NOT NULL DEFAULT FALSE,
    quarantine_reason TEXT,
    encryption_status VARCHAR(64) NOT NULL DEFAULT 'AES-256-GCM',
    encryption_iv VARCHAR(64) NOT NULL, -- 12-byte hex nonce
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_files_user ON files(user_id);
CREATE INDEX IF NOT EXISTS idx_files_folder ON files(folder_id);
CREATE INDEX IF NOT EXISTS idx_files_sha256 ON files(sha256_hash);
CREATE INDEX IF NOT EXISTS idx_files_status ON files(status);
CREATE INDEX IF NOT EXISTS idx_files_quarantined ON files(is_quarantined);

-- 4. FILE_VERSION TABLE (Historical Integrity & Revisions)
CREATE TABLE IF NOT EXISTS file_versions (
    id SERIAL PRIMARY KEY,
    file_id INTEGER NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    version_num INTEGER NOT NULL DEFAULT 1,
    file_size BIGINT NOT NULL,
    sha256_hash VARCHAR(64) NOT NULL,
    storage_path VARCHAR(512) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_file_versions_file ON file_versions(file_id);

-- 5. PERMISSION TABLE (Object-Level Authorization & Presets)
CREATE TABLE IF NOT EXISTS permissions (
    id SERIAL PRIMARY KEY,
    file_id INTEGER NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    can_view BOOLEAN NOT NULL DEFAULT TRUE,
    can_download BOOLEAN NOT NULL DEFAULT FALSE,
    can_edit BOOLEAN NOT NULL DEFAULT FALSE,
    can_share BOOLEAN NOT NULL DEFAULT FALSE,
    role_preset VARCHAR(32) NOT NULL DEFAULT 'VIEWER', -- 'VIEWER', 'DOWNLOADER', 'EDITOR', 'COLLABORATOR', 'OWNER'
    granted_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_permissions_file_user ON permissions(file_id, user_id);

-- 6. SHARE_LINK TABLE (Expiring, One-Time, & Password-Protected Shares)
CREATE TABLE IF NOT EXISTS share_links (
    id SERIAL PRIMARY KEY,
    file_id INTEGER NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(64) NOT NULL UNIQUE, -- SHA-256 of opaque token
    password_hash VARCHAR(255),
    expires_at TIMESTAMP WITH TIME ZONE,
    max_downloads INTEGER,
    download_count INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_shares_token ON share_links(token_hash);
CREATE INDEX IF NOT EXISTS idx_shares_file ON share_links(file_id);

-- 7. SECURITY_SCAN TABLE (Multi-Engine Inspection Telemetry)
CREATE TABLE IF NOT EXISTS scan_results (
    id SERIAL PRIMARY KEY,
    file_id INTEGER NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    scanner_name VARCHAR(100) NOT NULL,
    scan_status VARCHAR(32) NOT NULL, -- 'PASSED', 'MALICIOUS', 'HIGH_RISK', 'FAILED', 'ERROR'
    threat_level VARCHAR(32) NOT NULL DEFAULT 'CLEAN', -- 'CLEAN', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    threat_name VARCHAR(255),
    details TEXT,
    scanned_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_scans_file ON scan_results(file_id);

-- 8. AUDIT_LOG TABLE (Tamper-Evident SHA-256 Chained Ledger)
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    sequence_num INTEGER NOT NULL UNIQUE,
    actor_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    actor_email VARCHAR(255),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(100),
    ip_address VARCHAR(64),
    user_agent VARCHAR(255),
    result VARCHAR(32) NOT NULL, -- 'SUCCESS', 'FAILURE', 'BLOCKED', 'WARNING'
    metadata_json TEXT,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    previous_hash VARCHAR(64) NOT NULL,
    entry_hash VARCHAR(64) NOT NULL UNIQUE
);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_entry_hash ON audit_logs(entry_hash);

-- 9. LOGIN_ATTEMPT TABLE (Brute-Force & Anomaly Detection)
CREATE TABLE IF NOT EXISTS login_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    email VARCHAR(255) NOT NULL,
    ip_address VARCHAR(64),
    user_agent VARCHAR(255),
    success BOOLEAN NOT NULL DEFAULT FALSE,
    failure_reason VARCHAR(255),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_login_email ON login_attempts(email);
CREATE INDEX IF NOT EXISTS idx_login_timestamp ON login_attempts(timestamp);
