import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ShieldCheck,
  Lock,
  Download,
  FileText,
  AlertCircle,
  Clock,
  KeyRound,
  CheckCircle2,
} from 'lucide-react';
import { api, ApiError } from '../../api/client';

export const SharedAccessPage: React.FC = () => {
  const { token } = useParams<{ token: string }>();

  const [shareInfo, setShareInfo] = useState<any>(null);
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [downloadSuccess, setDownloadSuccess] = useState(false);

  useEffect(() => {
    if (!token) return;
    const fetchInfo = async () => {
      setLoading(true);
      try {
        const info = await api.getPublicShareInfo(token);
        setShareInfo(info);
      } catch (err: any) {
        setError(err.message || 'Share link is invalid, expired, or deactivated.');
      } finally {
        setLoading(false);
      }
    };
    fetchInfo();
  }, [token]);

  const handleDownload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) return;

    setError(null);
    setDownloading(true);
    try {
      await api.downloadSharedFile(token, password || undefined, shareInfo?.original_filename);
      setDownloadSuccess(true);
      // Refresh share info to reflect download count
      const updated = await api.getPublicShareInfo(token);
      setShareInfo(updated);
    } catch (err: any) {
      setError(err.message || 'Failed to download shared file. Check password or limits.');
    } finally {
      setDownloading(false);
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
      <div className="max-w-md mx-auto my-12 text-center text-slate-400 font-mono text-sm">
        <div className="w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        Resolving secure share token...
      </div>
    );
  }

  if (error && !shareInfo) {
    return (
      <div className="max-w-md mx-auto my-12 bg-[#111827] border border-slate-800 rounded-2xl p-8 text-center space-y-4">
        <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center mx-auto text-rose-400">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h3 className="text-lg font-bold text-white font-mono">Link Inaccessible</h3>
        <p className="text-xs text-slate-400 font-mono">{error}</p>
        <Link to="/" className="inline-block mt-4 text-xs text-cyan-400 hover:underline font-mono">
          Return to SecureShare Home
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-lg mx-auto my-8">
      <div className="bg-[#111827]/95 border border-slate-800 rounded-2xl p-8 backdrop-blur shadow-2xl space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center mx-auto text-cyan-400">
            <ShieldCheck className="w-6 h-6 text-emerald-400" />
          </div>
          <h2 className="text-xl font-bold text-white font-mono">Secure Shared File</h2>
          <p className="text-xs text-slate-400 font-mono">
            This file has been verified CLEAN and encrypted with AES-256-GCM.
          </p>
        </div>

        {error && (
          <div className="p-3.5 rounded-lg bg-rose-500/15 border border-rose-500/30 flex items-center gap-2.5 text-rose-300 text-xs font-mono">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
            <span>{error}</span>
          </div>
        )}

        {downloadSuccess && (
          <div className="p-3.5 rounded-lg bg-emerald-500/15 border border-emerald-500/30 flex items-center gap-2.5 text-emerald-300 text-xs font-mono">
            <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-400" />
            <span>Decryption successful! File download started.</span>
          </div>
        )}

        {/* File Metadata Card */}
        <div className="bg-black/40 border border-slate-800 rounded-xl p-4 flex items-center gap-4">
          <div className="w-12 h-12 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 shrink-0">
            <FileText className="w-6 h-6" />
          </div>
          <div className="min-w-0 flex-1">
            <h4 className="text-sm font-bold text-white font-mono truncate">
              {shareInfo?.original_filename}
            </h4>
            <div className="flex flex-wrap items-center gap-2 mt-1 text-[11px] text-slate-400 font-mono">
              <span>{formatBytes(shareInfo?.file_size || 0)}</span>
              <span>•</span>
              <span className="truncate max-w-[140px]">{shareInfo?.detected_mime}</span>
              {shareInfo?.remaining_downloads !== null && (
                <>
                  <span>•</span>
                  <span className="text-cyan-400 font-bold">{shareInfo.remaining_downloads} downloads left</span>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Expiry Badge */}
        {shareInfo?.expires_at && (
          <div className="flex items-center gap-2 text-xs text-slate-400 font-mono bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
            <Clock className="w-4 h-4 text-amber-400" />
            <span>Expires: {new Date(shareInfo.expires_at).toLocaleString()}</span>
          </div>
        )}

        {/* Access Restrictions Check */}
        {shareInfo?.is_expired ? (
          <div className="p-3 bg-rose-500/10 border border-rose-500/30 rounded-lg text-center text-xs text-rose-300 font-mono">
            This share link has expired and is no longer accessible.
          </div>
        ) : shareInfo?.is_limit_reached ? (
          <div className="p-3 bg-rose-500/10 border border-rose-500/30 rounded-lg text-center text-xs text-rose-300 font-mono">
            The download limit for this link has been reached.
          </div>
        ) : (
          <form onSubmit={handleDownload} className="space-y-4 font-mono text-xs">
            {shareInfo?.is_password_protected && (
              <div>
                <label className="block text-slate-300 font-semibold mb-1">
                  Password Required
                </label>
                <div className="relative">
                  <KeyRound className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter file access password"
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-3 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
                  />
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={downloading}
              className="w-full py-3 rounded-lg bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-black font-bold text-xs transition shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2"
            >
              {downloading ? (
                <>
                  <div className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin" />
                  Decrypting & Streaming...
                </>
              ) : (
                <>
                  <Download className="w-4 h-4" />
                  Decrypt & Download File
                </>
              )}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};
