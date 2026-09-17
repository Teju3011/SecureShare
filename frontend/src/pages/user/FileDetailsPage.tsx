import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  ShieldCheck,
  ShieldAlert,
  ArrowLeft,
  Download,
  Share2,
  Trash2,
  Lock,
  Binary,
  FileText,
  AlertTriangle,
  RefreshCw,
  Clock,
} from 'lucide-react';
import { api } from '../../api/client';
import { FileDetail } from '../../types';
import { SecurityBadge } from '../../components/common/SecurityBadge';
import { SecurityPipelineVisualizer } from '../../components/upload/SecurityPipelineVisualizer';

export const FileDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [file, setFile] = useState<FileDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    const fetchDetails = async () => {
      try {
        setLoading(true);
        const data = await api.getFileDetails(parseInt(id));
        setFile(data);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch file security details.');
      } finally {
        setLoading(false);
      }
    };
    fetchDetails();
  }, [id]);

  const handleDownload = async () => {
    if (!file) return;
    try {
      await api.downloadFile(file.id, file.original_filename);
    } catch (err: any) {
      setError(err.message || 'Download blocked by security policy.');
    }
  };

  const handleDelete = async () => {
    if (!file) return;
    if (!window.confirm('Permanently delete this file and audit records?')) return;
    try {
      await api.deleteFile(file.id);
      navigate('/files');
    } catch (err: any) {
      setError(err.message || 'Failed to delete file.');
    }
  };

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
  };

  if (loading) {
    return (
      <div className="py-20 text-center text-slate-500 font-mono text-xs flex items-center justify-center gap-2">
        <RefreshCw className="w-4 h-4 animate-spin text-cyan-400" />
        Loading security report...
      </div>
    );
  }

  if (error || !file) {
    return (
      <div className="max-w-md mx-auto my-12 bg-[#111827] border border-slate-800 rounded-2xl p-8 text-center space-y-4">
        <AlertTriangle className="w-8 h-8 text-rose-400 mx-auto" />
        <h3 className="text-base font-bold text-white font-mono">Error Loading File</h3>
        <p className="text-xs text-slate-400 font-mono">{error || 'File not found.'}</p>
        <Link to="/files" className="text-xs text-cyan-400 hover:underline font-mono">
          Back to My Files
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Back button & Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Link
            to="/files"
            className="p-2 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 transition"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <span className="text-[10px] font-mono font-bold tracking-widest text-cyan-400 uppercase">
              Security Inspection Report
            </span>
            <h1 className="text-xl font-bold text-white font-mono mt-0.5 truncate max-w-lg">
              {file.original_filename}
            </h1>
          </div>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs">
          {file.status === 'CLEAN' && !file.is_quarantined ? (
            <button
              onClick={handleDownload}
              className="px-3.5 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-black font-bold flex items-center gap-1.5 shadow-lg shadow-emerald-500/20 transition"
            >
              <Download className="w-3.5 h-3.5" />
              Decrypt & Download
            </button>
          ) : (
            <div className="px-3 py-1.5 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-300 flex items-center gap-1.5 text-xs font-mono">
              <Lock className="w-3.5 h-3.5 text-rose-400" />
              Download Blocked (Quarantined)
            </div>
          )}
          <button
            onClick={handleDelete}
            className="p-2 rounded-lg bg-slate-800 hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 transition"
            title="Delete File"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Security Status Banner */}
      <div
        className={`p-5 rounded-xl border flex items-center justify-between ${
          file.is_quarantined
            ? 'bg-rose-950/20 border-rose-500/40 text-rose-300'
            : 'bg-emerald-950/20 border-emerald-500/40 text-emerald-300'
        }`}
      >
        <div className="flex items-center gap-3">
          {file.is_quarantined ? (
            <ShieldAlert className="w-6 h-6 text-rose-400" />
          ) : (
            <ShieldCheck className="w-6 h-6 text-emerald-400" />
          )}
          <div>
            <h3 className="text-sm font-bold font-mono">
              {file.is_quarantined
                ? 'Security Status: QUARANTINED'
                : 'Security Status: VERIFIED CLEAN'}
            </h3>
            <p className="text-xs font-mono text-slate-400 mt-0.5">
              {file.quarantine_reason || 'File passed all signature, MIME, dangerous script, and antivirus scans.'}
            </p>
          </div>
        </div>
        <SecurityBadge status={file.status} />
      </div>

      {/* Visualizer Step Progress */}
      <SecurityPipelineVisualizer file={file} scans={file.scan_results} />

      {/* Technical Metadata & Cryptographic Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-[#111827]/80 border border-slate-800 rounded-xl p-5 space-y-3 font-mono text-xs">
          <h4 className="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-2">
            <FileText className="w-4 h-4" />
            File & Signature Metadata
          </h4>
          <div className="space-y-2 divide-y divide-slate-800/60">
            <div className="flex justify-between py-1.5">
              <span className="text-slate-400">Original Name:</span>
              <span className="text-white font-semibold">{file.original_filename}</span>
            </div>
            <div className="flex justify-between py-1.5">
              <span className="text-slate-400">File Size:</span>
              <span className="text-white">{formatBytes(file.file_size)}</span>
            </div>
            <div className="flex justify-between py-1.5">
              <span className="text-slate-400">Declared MIME:</span>
              <span className="text-white">{file.declared_mime}</span>
            </div>
            <div className="flex justify-between py-1.5">
              <span className="text-slate-400">Detected MIME:</span>
              <span className="text-white">{file.detected_mime}</span>
            </div>
            <div className="flex justify-between py-1.5">
              <span className="text-slate-400">Magic Bytes (Hex):</span>
              <code className="text-cyan-400 font-bold">{file.magic_bytes_preview || 'N/A'}</code>
            </div>
            <div className="flex justify-between py-1.5">
              <span className="text-slate-400">Uploaded At:</span>
              <span className="text-slate-300">{new Date(file.created_at).toLocaleString()}</span>
            </div>
          </div>
        </div>

        <div className="bg-[#111827]/80 border border-slate-800 rounded-xl p-5 space-y-3 font-mono text-xs">
          <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-2">
            <Binary className="w-4 h-4" />
            Cryptographic Integrity & Encryption
          </h4>
          <div className="space-y-2 divide-y divide-slate-800/60">
            <div className="py-1.5">
              <span className="text-slate-400 block mb-1">SHA-256 Digest:</span>
              <code className="bg-black/50 p-2 rounded block text-cyan-300 text-[11px] break-all border border-slate-800">
                {file.sha256_hash}
              </code>
            </div>
            <div className="flex justify-between py-1.5">
              <span className="text-slate-400">Encryption Standard:</span>
              <span className="text-white font-bold">AES-256-GCM (Authenticated)</span>
            </div>
            <div className="flex justify-between py-1.5">
              <span className="text-slate-400">Storage Partition:</span>
              <span className={file.is_quarantined ? 'text-rose-400' : 'text-emerald-400'}>
                {file.is_quarantined ? 'quarantine/' : 'clean/'}
              </span>
            </div>
            <div className="flex justify-between py-1.5">
              <span className="text-slate-400">Zero-Trust Status:</span>
              <span className="text-emerald-400 font-semibold">Strict Download Enforcement</span>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Multi-Stage Scan Results Table */}
      <div className="bg-[#111827]/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <h4 className="text-xs font-bold text-white font-mono uppercase tracking-wider flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-cyan-400" />
          Scanner Verdict Audit Trail
        </h4>
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead className="bg-[#0c1222] border-b border-slate-800 text-slate-400 text-[11px] uppercase">
              <tr>
                <th className="py-3 px-4">Scanner Engine</th>
                <th className="py-3 px-4">Verdict</th>
                <th className="py-3 px-4">Threat Level</th>
                <th className="py-3 px-4">Threat Name</th>
                <th className="py-3 px-4">Details & Findings</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {file.scan_results.map((sr) => (
                <tr key={sr.id} className="hover:bg-slate-800/30">
                  <td className="py-3 px-4 font-semibold text-white">{sr.scanner_name}</td>
                  <td className="py-3 px-4">
                    <SecurityBadge status={sr.scan_status} />
                  </td>
                  <td className="py-3 px-4">
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                        sr.threat_level === 'CRITICAL'
                          ? 'bg-rose-500/20 text-rose-300'
                          : sr.threat_level === 'HIGH'
                          ? 'bg-amber-500/20 text-amber-300'
                          : 'bg-emerald-500/20 text-emerald-300'
                      }`}
                    >
                      {sr.threat_level}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-300">{sr.threat_name || 'None'}</td>
                  <td className="py-3 px-4 text-slate-400 max-w-xs">{sr.details || 'Verified'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
