import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Shield, UserPlus, Trash2, Check, X, ArrowLeft, Lock, FileText, AlertCircle } from 'lucide-react';
import { api } from '../../api/client';

export const PermissionsPage: React.FC = () => {
  const { fileId } = useParams<{ fileId: string }>();
  const navigate = useNavigate();
  const [permissions, setPermissions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [fileDetails, setFileDetails] = useState<any>(null);

  // Form state
  const [email, setEmail] = useState('');
  const [preset, setPreset] = useState('VIEWER');
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  const fetchPermissions = async () => {
    try {
      setLoading(true);
      const [permRes, fileRes] = await Promise.all([
        api.get(`/permissions/${fileId}`),
        api.get(`/files/${fileId}`)
      ]);
      setPermissions(permRes.data);
      setFileDetails(fileRes.data);
    } catch (err: any) {
      console.error(err);
      setMessage({ text: err.response?.data?.detail || 'Failed to load permissions.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (fileId) fetchPermissions();
  }, [fileId]);

  const handleGrant = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    try {
      setSubmitting(true);
      setMessage(null);
      await api.post(`/permissions/${fileId}`, {
        user_email: email,
        role_preset: preset
      });
      setEmail('');
      setMessage({ text: `Permission '${preset}' successfully assigned to ${email}.`, type: 'success' });
      fetchPermissions();
    } catch (err: any) {
      setMessage({ text: err.response?.data?.detail || 'Failed to assign permission.', type: 'error' });
    } finally {
      setSubmitting(false);
    }
  };

  const handleRevoke = async (permId: number) => {
    if (!confirm('Are you sure you want to revoke this user\'s access immediately?')) return;
    try {
      await api.delete(`/permissions/${permId}`);
      setMessage({ text: 'Access revoked immediately. User can no longer view or download this file.', type: 'success' });
      fetchPermissions();
    } catch (err: any) {
      setMessage({ text: err.response?.data?.detail || 'Failed to revoke permission.', type: 'error' });
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <button
        onClick={() => navigate('/files')}
        className="flex items-center space-x-2 text-xs text-slate-500 hover:text-slate-800 transition"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to My Files</span>
      </button>

      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-indigo-50 text-indigo-600 rounded-lg">
              <Shield className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900">Object-Level Permission Control</h1>
              <p className="text-xs text-slate-500 mt-0.5">
                Manage granular role presets and instantaneous access revocation.
              </p>
            </div>
          </div>
          {fileDetails && (
            <div className="text-right">
              <div className="text-xs font-mono font-semibold text-slate-800">{fileDetails.original_filename}</div>
              <div className="text-[11px] text-slate-400 font-mono">SHA-256: {fileDetails.sha256_hash?.slice(0, 16)}...</div>
            </div>
          )}
        </div>
      </div>

      {message && (
        <div className={`p-4 rounded-lg text-xs flex items-center space-x-2 ${
          message.type === 'success' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-700 border border-rose-200'
        }`}>
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{message.text}</span>
        </div>
      )}

      {/* Grant Form */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-slate-900 mb-4 flex items-center space-x-2">
          <UserPlus className="w-4 h-4 text-indigo-600" />
          <span>Grant User Permission</span>
        </h2>
        <form onSubmit={handleGrant} className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700">Collaborator Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g. rahul@example.com"
              required
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700">Permission Preset</label>
            <select
              value={preset}
              onChange={(e) => setPreset(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none bg-white"
            >
              <option value="VIEWER">Viewer (View only, No Download)</option>
              <option value="DOWNLOADER">Downloader (View + Download)</option>
              <option value="EDITOR">Editor (View + Download + Edit)</option>
              <option value="COLLABORATOR">Collaborator (View + Download + Share)</option>
            </select>
          </div>
          <button
            type="submit"
            disabled={submitting}
            className="w-full py-2 px-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-medium transition shadow-sm disabled:opacity-50"
          >
            {submitting ? 'Granting...' : 'Assign Permission'}
          </button>
        </form>
      </div>

      {/* Permissions Table */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
          <h3 className="text-xs font-semibold text-slate-700 uppercase tracking-wider">Active Permissions List</h3>
          <span className="text-xs text-slate-500 font-mono">{permissions.length} Users Permitted</span>
        </div>

        {loading ? (
          <div className="p-8 text-center text-xs text-slate-500">Loading access control lists...</div>
        ) : permissions.length === 0 ? (
          <div className="p-8 text-center text-xs text-slate-500">No external users have been granted permission yet. Only you (the owner) have access.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 text-[11px] text-slate-500 uppercase bg-slate-50/50">
                  <th className="py-3 px-4">User</th>
                  <th className="py-3 px-4">Preset</th>
                  <th className="py-3 px-4 text-center">View</th>
                  <th className="py-3 px-4 text-center">Download</th>
                  <th className="py-3 px-4 text-center">Edit</th>
                  <th className="py-3 px-4 text-center">Share</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs">
                {permissions.map((p) => {
                  const isRevoked = !!p.revoked_at || (!p.can_view && !p.can_download);
                  return (
                    <tr key={p.id} className="hover:bg-slate-50/80 transition">
                      <td className="py-3 px-4">
                        <div className="font-semibold text-slate-900">{p.user_name}</div>
                        <div className="text-[11px] text-slate-500">{p.user_email}</div>
                      </td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-0.5 rounded font-mono text-[10px] font-semibold bg-slate-100 text-slate-800">
                          {p.role_preset}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-center">
                        {p.can_view ? <Check className="w-4 h-4 text-emerald-600 inline" /> : <X className="w-4 h-4 text-rose-500 inline" />}
                      </td>
                      <td className="py-3 px-4 text-center">
                        {p.can_download ? <Check className="w-4 h-4 text-emerald-600 inline" /> : <X className="w-4 h-4 text-rose-500 inline" />}
                      </td>
                      <td className="py-3 px-4 text-center">
                        {p.can_edit ? <Check className="w-4 h-4 text-emerald-600 inline" /> : <X className="w-4 h-4 text-rose-500 inline" />}
                      </td>
                      <td className="py-3 px-4 text-center">
                        {p.can_share ? <Check className="w-4 h-4 text-emerald-600 inline" /> : <X className="w-4 h-4 text-rose-500 inline" />}
                      </td>
                      <td className="py-3 px-4">
                        {isRevoked ? (
                          <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-rose-50 text-rose-700">REVOKED</span>
                        ) : (
                          <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-50 text-emerald-700">ACTIVE</span>
                        )}
                      </td>
                      <td className="py-3 px-4 text-right">
                        {!isRevoked && (
                          <button
                            onClick={() => handleRevoke(p.id)}
                            className="px-2.5 py-1 text-rose-600 hover:bg-rose-50 rounded text-xs font-medium transition inline-flex items-center space-x-1"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                            <span>Revoke</span>
                          </button>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
