import {
  User,
  FileItem,
  FileDetail,
  ShareLinkItem,
  AuditLogItem,
  AuditVerificationResult,
  PipelineRunItem,
  SecurityFindingItem,
  AdminDashboardStats,
  UserDashboardStats,
} from '../types';

const API_BASE = '/api/v1';

export class ApiError extends Error {
  constructor(public status: number, message: string, public detail?: any) {
    super(message);
    this.name = 'ApiError';
  }
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('secureshare_token');
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string> || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Default Content-Type to application/json unless body is FormData
  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorDetail = 'An unexpected error occurred.';
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.detail || errorJson.message || JSON.stringify(errorJson);
    } catch {
      errorDetail = response.statusText || String(response.status);
    }

    if (response.status === 401 && !endpoint.includes('/auth/login')) {
      localStorage.removeItem('secureshare_token');
      localStorage.removeItem('secureshare_user');
      window.dispatchEvent(new Event('auth-logout'));
    }

    throw new ApiError(response.status, errorDetail);
  }

  // Handle empty or blob responses
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    return response.json();
  }
  return response.text() as unknown as T;
}

export const api = {
  // Auth
  login: (data: any) => request<any>('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  register: (data: any) => request<User>('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  logout: () => request<any>('/auth/logout', { method: 'POST' }),
  getMe: () => request<User>('/auth/me'),
  setupMfa: () => request<any>('/auth/mfa/setup', { method: 'POST' }),
  verifyMfa: (code: string) => request<any>('/auth/mfa/verify', { method: 'POST', body: JSON.stringify({ code }) }),

  // User Dashboard & Activity
  getUserDashboard: () => request<UserDashboardStats>('/users/dashboard'),
  getUserActivity: () => request<AuditLogItem[]>('/users/activity'),

  // Files
  listFiles: () => request<FileItem[]>('/files/'),
  getFileDetails: (id: number) => request<FileDetail>(`/files/${id}`),
  uploadFile: (formData: FormData) => request<any>('/files/upload', { method: 'POST', body: formData }),
  uploadEicarTest: () => request<any>('/files/upload-eicar', { method: 'POST' }),
  deleteFile: (id: number) => request<any>(`/files/${id}`, { method: 'DELETE' }),

  downloadFileUrl: (id: number) => `${API_BASE}/files/${id}/download`,
  async downloadFile(id: number, filename: string): Promise<void> {
    const token = localStorage.getItem('secureshare_token');
    const res = await fetch(`${API_BASE}/files/${id}/download`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to download file' }));
      throw new ApiError(res.status, err.detail || 'Download forbidden');
    }
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },

  // Shares
  createShare: (data: any) => request<any>('/shares/create', { method: 'POST', body: JSON.stringify(data) }),
  listMyShares: () => request<ShareLinkItem[]>('/shares/my-shares'),
  revokeShare: (id: number) => request<any>(`/shares/${id}`, { method: 'DELETE' }),
  getPublicShareInfo: (token: string) => request<any>(`/shares/public/${token}/info`),
  async downloadSharedFile(token: string, password?: string, filename?: string): Promise<void> {
    const res = await fetch(`${API_BASE}/shares/public/${token}/download`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Download failed' }));
      throw new ApiError(res.status, err.detail || 'Download forbidden');
    }
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'secureshare_download';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },

  // Admin
  getAdminStats: () => request<AdminDashboardStats>('/admin/dashboard/stats'),
  listUsers: () => request<User[]>('/admin/users'),
  updateUserRole: (id: number, role: string) => request<User>(`/admin/users/${id}/role`, { method: 'PUT', body: JSON.stringify({ role }) }),
  updateUserStatus: (id: number, is_active: boolean) => request<User>(`/admin/users/${id}/status`, { method: 'PUT', body: JSON.stringify({ is_active }) }),
  listQuarantined: () => request<FileDetail[]>('/admin/quarantine'),
  releaseQuarantined: (id: number) => request<any>(`/admin/quarantine/${id}/release`, { method: 'POST' }),
  purgeQuarantined: (id: number) => request<any>(`/admin/quarantine/${id}`, { method: 'DELETE' }),
  listAuditLogs: (action?: string, result?: string) => {
    const params = new URLSearchParams();
    if (action) params.append('action', action);
    if (result) params.append('result', result);
    return request<AuditLogItem[]>(`/admin/audit-logs?${params.toString()}`);
  },
  verifyAuditLogs: () => request<AuditVerificationResult>('/admin/audit-logs/verify'),
  listPipelineRuns: () => request<PipelineRunItem[]>('/admin/pipeline-runs'),
  triggerPipelineScan: (branch = 'main', simulate_fail = false) =>
    request<PipelineRunItem>('/admin/pipeline-runs/trigger', {
      method: 'POST',
      body: JSON.stringify({ branch, simulate_fail })
    }),
  listSecurityFindings: (severity?: string) => {
    const params = new URLSearchParams();
    if (severity) params.append('severity', severity);
    return request<SecurityFindingItem[]>(`/admin/security-findings?${params.toString()}`);
  },
};
