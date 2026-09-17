import React, { useState, useEffect } from 'react';
import {
  Share2,
  Lock,
  Clock,
  Trash2,
  AlertTriangle,
  RefreshCw,
  ExternalLink,
  ShieldCheck,
  Check,
  Copy,
} from 'lucide-react';
import { api } from '../../api/client';
import { ShareLinkItem } from '../../types';

export const SharePage: React.FC = () => {
  const [shares, setShares] = useState<ShareLinkItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchShares = async () => {
    try {
      setLoading(true);
      const data = await api.listMyShares();
      setShares(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load active shares.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchShares();
  }, []);

  const handleRevoke = async (id: number) => {
    if (!window.confirm('Immediately revoke this share link? Further downloads will be blocked.')) return;
    try {
      await api.revokeShare(id);
      setShares(shares.filter((s) => s.id !== id));
    } catch (err: any) {
      setError(err.message || 'Failed to revoke share link.');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <span className="text-[10px] font-mono font-bold tracking-widest text-cyan-400 uppercase">
          Access Governance
        </span>
        <h1 className="text-2xl font-bold text-white font-mono mt-1">Active Share Links</h1>
        <p className="text-xs text-slate-400 font-mono mt-1">
          Monitor expiring secure access tokens, download limits, and password-protected files.
        </p>
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-500/15 border border-rose-500/30 flex items-center gap-2.5 text-rose-300 text-xs font-mono">
          <AlertTriangle className="w-4 h-4 shrink-0 text-rose-400" />
          <span>{error}</span>
        </div>
      )}

      <div className="bg-[#111827]/80 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        {loading ? (
          <div className="py-16 text-center text-slate-500 font-mono text-xs flex items-center justify-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin text-cyan-400" />
            Loading active shares...
          </div>
        ) : shares.length === 0 ? (
          <div className="py-16 text-center text-slate-500 font-mono text-xs">
            No active share links. Select a verified clean file from "My Files" to generate a secure link.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-xs">
              <thead className="bg-[#0c1222] border-b border-slate-800 text-slate-400 text-[11px] uppercase tracking-wider">
                <tr>
                  <th className="py-3.5 px-4 font-semibold">Shared File</th>
                  <th className="py-3.5 px-4 font-semibold">Security Controls</th>
                  <th className="py-3.5 px-4 font-semibold">Downloads</th>
                  <th className="py-3.5 px-4 font-semibold">Expiration</th>
                  <th className="py-3.5 px-4 font-semibold">Status</th>
                  <th className="py-3.5 px-4 font-semibold text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {shares.map((s) => (
                  <tr key={s.id} className="hover:bg-slate-800/30 transition">
                    <td className="py-3.5 px-4 font-semibold text-white max-w-[200px] truncate">
                      {s.original_filename}
                    </td>
                    <td className="py-3.5 px-4">
                      <div className="flex items-center gap-2">
                        {s.is_password_protected ? (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/30 text-[10px]">
                            <Lock className="w-3 h-3" /> Password
                          </span>
                        ) : (
                          <span className="text-slate-500 text-[11px]">Public Token</span>
                        )}
                      </div>
                    </td>
                    <td className="py-3.5 px-4 text-slate-300">
                      <span className="font-bold text-white">{s.download_count}</span>
                      {s.max_downloads ? ` / ${s.max_downloads}` : ' (Unlimited)'}
                    </td>
                    <td className="py-3.5 px-4 text-slate-400 text-[11px]">
                      {s.expires_at ? new Date(s.expires_at).toLocaleString() : 'Never'}
                    </td>
                    <td className="py-3.5 px-4">
                      <span
                        className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold ${
                          s.is_active
                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                            : 'bg-slate-800 text-slate-400 border border-slate-700'
                        }`}
                      >
                        {s.is_active ? 'ACTIVE' : 'REVOKED'}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      {s.is_active && (
                        <button
                          onClick={() => handleRevoke(s.id)}
                          className="p-1.5 rounded bg-slate-800 hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 transition"
                          title="Revoke Share Immediately"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
