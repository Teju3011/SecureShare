import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  FolderLock,
  Search,
  Download,
  Share2,
  Trash2,
  Eye,
  AlertTriangle,
  RefreshCw,
  Copy,
  Check,
  Lock,
  Calendar,
  X,
} from 'lucide-react';
import { api } from '../../api/client';
import { FileItem } from '../../types';
import { SecurityBadge } from '../../components/common/SecurityBadge';

export const MyFilesPage: React.FC = () => {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [actionError, setActionError] = useState<string | null>(null);

  // Share Modal state
  const [shareFile, setShareFile] = useState<FileItem | null>(null);
  const [expiresHours, setExpiresHours] = useState('24');
  const [password, setPassword] = useState('');
  const [maxDownloads, setMaxDownloads] = useState('');
  const [shareResult, setShareResult] = useState<any>(null);
  const [copied, setCopied] = useState(false);
  const [sharing, setSharing] = useState(false);

  const fetchFiles = async () => {
    try {
      setLoading(true);
      const data = await api.listFiles();
      setFiles(data);
    } catch (err: any) {
      setActionError(err.message || 'Failed to retrieve file repository.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  const handleDownload = async (file: FileItem) => {
    setActionError(null);
    try {
      await api.downloadFile(file.id, file.original_filename);
    } catch (err: any) {
      setActionError(err.message || 'Download blocked by security policy.');
    }
  };

  const handleDelete = async (fileId: number) => {
    if (!window.confirm('Permanently delete this file and its encrypted records?')) return;
    try {
      await api.deleteFile(fileId);
      setFiles(files.filter((f) => f.id !== fileId));
    } catch (err: any) {
      setActionError(err.message || 'Failed to delete file.');
    }
  };

  const handleCreateShare = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!shareFile) return;
    setActionError(null);
    setSharing(true);
    try {
      const res = await api.createShare({
        file_id: shareFile.id,
        expires_in_hours: parseInt(expiresHours) || 24,
        password: password || undefined,
        max_downloads: maxDownloads ? parseInt(maxDownloads) : undefined,
      });
      // Replace origin with current browser origin
      const currentUrl = `${window.location.origin}/share/${res.share_token}`;
      setShareResult({ ...res, full_url: currentUrl });
    } catch (err: any) {
      setActionError(err.message || 'Failed to generate secure share link.');
    } finally {
      setSharing(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const filteredFiles = files.filter(
    (f) =>
      f.original_filename.toLowerCase().includes(search.toLowerCase()) ||
      f.detected_mime.toLowerCase().includes(search.toLowerCase()) ||
      f.sha256_hash.toLowerCase().includes(search.toLowerCase())
  );

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
          <span className="text-[10px] font-mono font-bold tracking-widest text-cyan-400 uppercase">
            Encrypted Storage
          </span>
          <h1 className="text-2xl font-bold text-white font-mono mt-1">My Secure Files</h1>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Zero-Trust verified repository with AES-256-GCM authenticated encryption at rest.
          </p>
        </div>

        <Link
          to="/upload"
          className="px-4 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black text-xs font-mono font-bold shadow-lg shadow-cyan-500/20 transition w-fit"
        >
          + Upload New File
        </Link>
      </div>

      {actionError && (
        <div className="p-3.5 rounded-xl bg-rose-500/15 border border-rose-500/30 flex items-center gap-2.5 text-rose-300 text-xs font-mono">
          <AlertTriangle className="w-4 h-4 shrink-0 text-rose-400" />
          <span>{actionError}</span>
        </div>
      )}

      {/* Search Bar */}
      <div className="bg-[#111827]/80 border border-slate-800 rounded-xl p-3 flex items-center gap-3">
        <Search className="w-4 h-4 text-slate-500" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by file name, MIME type, or SHA-256 hash..."
          className="w-full bg-transparent border-none text-white text-xs font-mono placeholder-slate-500 focus:outline-none"
        />
      </div>

      {/* Files Table */}
      <div className="bg-[#111827]/80 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        {loading ? (
          <div className="py-16 text-center text-slate-500 font-mono text-xs flex items-center justify-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin text-cyan-400" />
            Loading encrypted file registry...
          </div>
        ) : filteredFiles.length === 0 ? (
          <div className="py-16 text-center text-slate-500 font-mono text-xs">
            No matching files found in your secure repository.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-xs">
              <thead className="bg-[#0c1222] border-b border-slate-800 text-slate-400 text-[11px] uppercase tracking-wider">
                <tr>
                  <th className="py-3.5 px-4 font-semibold">File Name</th>
                  <th className="py-3.5 px-4 font-semibold">Size</th>
                  <th className="py-3.5 px-4 font-semibold">MIME / Signature</th>
                  <th className="py-3.5 px-4 font-semibold">SHA-256 Hash</th>
                  <th className="py-3.5 px-4 font-semibold">Security Status</th>
                  <th className="py-3.5 px-4 font-semibold text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {filteredFiles.map((file) => (
                  <tr key={file.id} className="hover:bg-slate-800/30 transition">
                    <td className="py-3.5 px-4 font-semibold text-white max-w-[220px] truncate">
                      <Link to={`/files/${file.id}`} className="hover:text-cyan-400 transition">
                        {file.original_filename}
                      </Link>
                    </td>
                    <td className="py-3.5 px-4 text-slate-400 whitespace-nowrap">
                      {formatBytes(file.file_size)}
                    </td>
                    <td className="py-3.5 px-4 text-slate-400 max-w-[150px] truncate">
                      {file.detected_mime}
                    </td>
                    <td className="py-3.5 px-4 text-slate-400 font-mono text-[11px]">
                      <span title={file.sha256_hash}>{file.sha256_hash.substring(0, 10)}...</span>
                    </td>
                    <td className="py-3.5 px-4 whitespace-nowrap">
                      <SecurityBadge status={file.status} />
                    </td>
                    <td className="py-3.5 px-4 text-right whitespace-nowrap space-x-2">
                      <Link
                        to={`/files/${file.id}`}
                        className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white inline-block transition"
                        title="View Security Scan Details"
                      >
                        <Eye className="w-3.5 h-3.5" />
                      </Link>

                      {file.status === 'CLEAN' && !file.is_quarantined ? (
                        <>
                          <button
                            onClick={() => handleDownload(file)}
                            className="p-1.5 rounded bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 transition"
                            title="Decrypt & Download"
                          >
                            <Download className="w-3.5 h-3.5" />
                          </button>
                          <button
                            onClick={() => {
                              setShareFile(file);
                              setShareResult(null);
                            }}
                            className="p-1.5 rounded bg-purple-500/10 hover:bg-purple-500/20 text-purple-400 border border-purple-500/30 transition"
                            title="Create Expiring Share Link"
                          >
                            <Share2 className="w-3.5 h-3.5" />
                          </button>
                        </>
                      ) : (
                        <span
                          className="p-1.5 rounded bg-rose-500/10 text-rose-500/40 border border-rose-500/20 cursor-not-allowed inline-block"
                          title="Download & Share strictly blocked by zero-trust quarantine policy"
                        >
                          <Lock className="w-3.5 h-3.5" />
                        </span>
                      )}

                      <button
                        onClick={() => handleDelete(file.id)}
                        className="p-1.5 rounded bg-slate-800 hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 transition"
                        title="Delete File"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Secure Share Modal */}
      {shareFile && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#111827] border border-slate-800 rounded-2xl max-w-md w-full p-6 space-y-5 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <Share2 className="w-4 h-4 text-purple-400" />
                <h3 className="text-sm font-bold text-white font-mono">Create Secure Share Link</h3>
              </div>
              <button
                onClick={() => setShareFile(null)}
                className="text-slate-500 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="bg-black/40 border border-slate-800 rounded-lg p-3 text-xs font-mono text-slate-300">
              <span className="text-slate-500 block text-[10px] uppercase">Selected File:</span>
              <span className="font-bold text-white">{shareFile.original_filename}</span>
            </div>

            {shareResult ? (
              <div className="space-y-4 font-mono text-xs">
                <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-300">
                  Secure share link successfully generated!
                </div>
                <div>
                  <label className="block text-slate-400 mb-1">Share URL (Single Token Access):</label>
                  <div className="flex items-center gap-2">
                    <input
                      type="text"
                      readOnly
                      value={shareResult.full_url}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-cyan-400 text-xs select-all"
                    />
                    <button
                      onClick={() => copyToClipboard(shareResult.full_url)}
                      className="px-3 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black font-bold shrink-0 transition"
                    >
                      {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                    </button>
                  </div>
                </div>
                <p className="text-[11px] text-slate-400">
                  Note: The server stores only a SHA-256 hash of this token. The plaintext token cannot be retrieved again if lost.
                </p>
                <button
                  onClick={() => setShareFile(null)}
                  className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition"
                >
                  Close
                </button>
              </div>
            ) : (
              <form onSubmit={handleCreateShare} className="space-y-4 font-mono text-xs">
                <div>
                  <label className="block text-slate-300 mb-1">Expiration Period</label>
                  <select
                    value={expiresHours}
                    onChange={(e) => setExpiresHours(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-purple-500"
                  >
                    <option value="1">1 Hour</option>
                    <option value="6">6 Hours</option>
                    <option value="24">24 Hours (1 Day)</option>
                    <option value="72">72 Hours (3 Days)</option>
                    <option value="168">7 Days</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-300 mb-1">Optional Access Password</label>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Leave empty for unpassworded link"
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-purple-500"
                  />
                </div>

                <div>
                  <label className="block text-slate-300 mb-1">Max Download Limit (Optional)</label>
                  <input
                    type="number"
                    min="1"
                    max="1000"
                    value={maxDownloads}
                    onChange={(e) => setMaxDownloads(e.target.value)}
                    placeholder="e.g. 1 (Burn after single download)"
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-purple-500"
                  />
                </div>

                <button
                  type="submit"
                  disabled={sharing}
                  className="w-full py-2.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-white font-bold transition shadow-lg shadow-purple-900/30"
                >
                  {sharing ? 'Generating Cryptographic Link...' : 'Create Secure Share'}
                </button>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
