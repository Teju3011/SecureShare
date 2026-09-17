import React, { useState, useEffect } from 'react';
import {
  AlertTriangle,
  ShieldAlert,
  Trash2,
  CheckCircle2,
  RefreshCw,
  FileText,
  ShieldCheck,
  Binary,
  X,
  Eye,
} from 'lucide-react';
import { api } from '../../api/client';
import { FileDetail } from '../../types';
import { SecurityBadge } from '../../components/common/SecurityBadge';

export const QuarantinePage: React.FC = () => {
  const [quarantinedFiles, setQuarantinedFiles] = useState<FileDetail[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<FileDetail | null>(null);

  const fetchQuarantine = async () => {
    try {
      setLoading(true);
      const data = await api.listQuarantined();
      setQuarantinedFiles(data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch quarantine list.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuarantine();
  }, []);

  const handleRelease = async (fileId: number) => {
    if (!window.confirm('Are you sure you want to release this file from quarantine into the clean storage zone? This action will be audited.')) return;
    setError(null);
    setSuccess(null);
    try {
      const res = await api.releaseQuarantined(fileId);
      setSuccess(res.message);
      setQuarantinedFiles(quarantinedFiles.filter((f) => f.id !== fileId));
      if (selectedFile?.id === fileId) setSelectedFile(null);
    } catch (err: any) {
      setError(err.message || 'Failed to release file from quarantine.');
    }
  };

  const handlePurge = async (fileId: number) => {
    if (!window.confirm('Permanently purge this threat from quarantine storage? This cannot be undone.')) return;
    setError(null);
    setSuccess(null);
    try {
      const res = await api.purgeQuarantined(fileId);
      setSuccess(res.message);
      setQuarantinedFiles(quarantinedFiles.filter((f) => f.id !== fileId));
      if (selectedFile?.id === fileId) setSelectedFile(null);
    } catch (err: any) {
      setError(err.message || 'Failed to purge file.');
    }
  };

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-[10px] font-mono font-bold tracking-widest text-rose-400 uppercase">
            Isolated Storage Vault
          </span>
          <h1 className="text-2xl font-bold text-white font-mono mt-1">Quarantine Management</h1>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Zero-Trust quarantine partition: Inspect detected malware, spoofed MIME, or scripts, and execute release/purge actions.
          </p>
        </div>

        <button
          onClick={fetchQuarantine}
          className="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono text-xs flex items-center gap-2 transition w-fit"
        >
          <RefreshCw className="w-3.5 h-3.5 text-cyan-400" />
          Refresh Vault
        </button>
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-500/15 border border-rose-500/30 flex items-center gap-2.5 text-rose-300 text-xs font-mono">
          <AlertTriangle className="w-4 h-4 shrink-0 text-rose-400" />
          <span>{error}</span>
        </div>
      )}

      {success && (
        <div className="p-3.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 flex items-center gap-2.5 text-emerald-300 text-xs font-mono">
          <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-400" />
          <span>{success}</span>
        </div>
      )}

      <div className="bg-[#111827]/80 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        {loading ? (
          <div className="py-16 text-center text-slate-500 font-mono text-xs flex items-center justify-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin text-rose-400" />
            Loading quarantined files...
          </div>
        ) : quarantinedFiles.length === 0 ? (
          <div className="py-16 text-center text-slate-500 font-mono text-xs">
            No active threats in quarantine. System storage is clean.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-xs">
              <thead className="bg-[#0c1222] border-b border-slate-800 text-slate-400 text-[11px] uppercase tracking-wider">
                <tr>
                  <th className="py-3.5 px-4 font-semibold">File Name</th>
                  <th className="py-3.5 px-4 font-semibold">Size</th>
                  <th className="py-3.5 px-4 font-semibold">Quarantine Reason</th>
                  <th className="py-3.5 px-4 font-semibold">Status</th>
                  <th className="py-3.5 px-4 font-semibold">Detected At</th>
                  <th className="py-3.5 px-4 font-semibold text-right">Admin Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {quarantinedFiles.map((file) => (
                  <tr key={file.id} className="hover:bg-slate-800/30 transition">
                    <td className="py-3.5 px-4 font-bold text-white max-w-[200px] truncate">
                      {file.original_filename}
                    </td>
                    <td className="py-3.5 px-4 text-slate-400">{formatBytes(file.file_size)}</td>
                    <td className="py-3.5 px-4 text-rose-300 max-w-xs truncate text-[11px]">
                      {file.quarantine_reason || 'Security scan failed'}
                    </td>
                    <td className="py-3.5 px-4">
                      <SecurityBadge status={file.status} />
                    </td>
                    <td className="py-3.5 px-4 text-slate-500 text-[11px]">
                      {new Date(file.created_at).toLocaleString()}
                    </td>
                    <td className="py-3.5 px-4 text-right space-x-2 whitespace-nowrap">
                      <button
                        onClick={() => setSelectedFile(file)}
                        className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition text-[11px]"
                      >
                        Inspect
                      </button>
                      <button
                        onClick={() => handleRelease(file.id)}
                        className="px-2.5 py-1 rounded bg-emerald-500/15 hover:bg-emerald-500/25 text-emerald-300 border border-emerald-500/30 transition text-[11px]"
                      >
                        Release
                      </button>
                      <button
                        onClick={() => handlePurge(file.id)}
                        className="px-2.5 py-1 rounded bg-rose-500/15 hover:bg-rose-500/25 text-rose-300 border border-rose-500/30 transition text-[11px]"
                      >
                        Purge
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Inspect Modal */}
      {selectedFile && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#111827] border border-slate-800 rounded-2xl max-w-2xl w-full p-6 space-y-5 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <ShieldAlert className="w-5 h-5 text-rose-400" />
                <h3 className="text-sm font-bold text-white font-mono">Quarantine Inspection: {selectedFile.original_filename}</h3>
              </div>
              <button onClick={() => setSelectedFile(null)} className="text-slate-500 hover:text-white">
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-3 bg-black/40 p-4 rounded-xl border border-slate-800 text-xs font-mono">
              <div>
                <span className="text-slate-500 block text-[10px]">SHA-256 Hash:</span>
                <span className="text-cyan-300 break-all text-[11px]">{selectedFile.sha256_hash}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">Storage Partition:</span>
                <span className="text-rose-400 font-bold">{selectedFile.storage_path}</span>
              </div>
              <div className="col-span-2 mt-2">
                <span className="text-slate-500 block text-[10px]">Quarantine Cause:</span>
                <span className="text-rose-300 font-semibold">{selectedFile.quarantine_reason}</span>
              </div>
            </div>

            {/* Scan results */}
            <div className="space-y-2">
              <span className="text-xs font-bold text-white font-mono uppercase">Scanner Breakdown:</span>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {selectedFile.scan_results?.map((sr) => (
                  <div key={sr.id} className="p-3 bg-slate-900 border border-slate-800 rounded-lg flex items-center justify-between text-xs font-mono">
                    <div>
                      <span className="font-bold text-slate-200">{sr.scanner_name}</span>
                      <p className="text-[11px] text-slate-400 mt-0.5">{sr.details}</p>
                    </div>
                    <SecurityBadge status={sr.scan_status} />
                  </div>
                ))}
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800 font-mono text-xs">
              <button
                onClick={() => handleRelease(selectedFile.id)}
                className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-black font-bold rounded-lg transition"
              >
                Release to Clean Storage
              </button>
              <button
                onClick={() => handlePurge(selectedFile.id)}
                className="px-4 py-2 bg-rose-500 hover:bg-rose-400 text-white font-bold rounded-lg transition"
              >
                Permanently Purge
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
