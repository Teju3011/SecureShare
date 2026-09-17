export type UserRole = 'STANDARD_USER' | 'ADMIN';

export type FileStatus =
  | 'UPLOADING'
  | 'VALIDATING'
  | 'SCANNING'
  | 'CLEAN'
  | 'HIGH_RISK'
  | 'MALICIOUS'
  | 'QUARANTINED'
  | 'FAILED';

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  mfa_enabled: boolean;
  created_at: string;
}

export interface ScanResultItem {
  id: number;
  scanner_name: string;
  scan_status: 'PASSED' | 'MALICIOUS' | 'HIGH_RISK' | 'FAILED' | 'ERROR';
  threat_level: 'CLEAN' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  threat_name?: string;
  details?: string;
  scanned_at: string;
}

export interface FileItem {
  id: number;
  user_id: number;
  original_filename: string;
  file_size: number;
  declared_mime: string;
  detected_mime: string;
  magic_bytes_preview?: string;
  sha256_hash: string;
  status: FileStatus;
  storage_path?: string;
  is_quarantined: boolean;
  quarantine_reason?: string;
  created_at: string;
  updated_at: string;
}

export interface FileDetail extends FileItem {
  scan_results: ScanResultItem[];
}

export interface ShareLinkItem {
  id: number;
  file_id: number;
  original_filename: string;
  expires_at?: string;
  max_downloads?: number;
  download_count: number;
  is_active: boolean;
  is_password_protected: boolean;
  created_at: string;
}

export interface AuditLogItem {
  id: number;
  sequence_num: number;
  actor_id?: number;
  actor_email?: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  ip_address?: string;
  user_agent?: string;
  result: 'SUCCESS' | 'FAILURE' | 'BLOCKED' | 'QUARANTINE' | 'WARNING';
  metadata_json?: string;
  timestamp: string;
  previous_hash: string;
  entry_hash: string;
}

export interface AuditVerificationResult {
  is_valid: boolean;
  total_records: number;
  tampered_sequence_num?: number;
  expected_hash?: string;
  actual_hash?: string;
  message: string;
}

export interface PipelineRunItem {
  id: number;
  commit_hash: string;
  branch: string;
  triggered_by: string;
  status: 'RUNNING' | 'PASSED' | 'FAILED' | 'BLOCKED';
  started_at: string;
  completed_at?: string;
  total_findings: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  is_blocked: boolean;
}

export interface SecurityFindingItem {
  id: number;
  pipeline_run_id: number;
  tool_name: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low' | 'Informational';
  title: string;
  description: string;
  file_path?: string;
  line_number?: number;
  cve_id?: string;
  status: string;
  created_at: string;
}

export interface AdminDashboardStats {
  total_users: number;
  total_files: number;
  files_scanned: number;
  threats_detected: number;
  quarantined_files: number;
  active_shares: number;
  total_security_findings: number;
  pipeline_failures: number;
  status_counts: Record<string, number>;
  severity_breakdown: Record<string, number>;
  upload_trend: Array<{ day: string; uploads: number }>;
  malware_trend: Array<{ day: string; threats: number }>;
  recent_alerts: Array<{ id: number; action: string; actor: string; result: string; timestamp: string; resource: string }>;
  recent_quarantine: Array<{ id: number; filename: string; size: number; reason: string; timestamp: string }>;
  recent_pipeline_runs: Array<{ id: number; commit: string; branch: string; status: string; critical: number; high: number; timestamp: string }>;
}

export interface UserDashboardStats {
  total_files: number;
  safe_files: number;
  scanning_files: number;
  quarantined_files: number;
  active_shares: number;
  recent_files: Array<{ id: number; filename: string; size: number; mime: string; status: string; is_quarantined: boolean; created_at: string }>;
  recent_activity: Array<{ id: number; action: string; resource: string; result: string; timestamp: string }>;
}
