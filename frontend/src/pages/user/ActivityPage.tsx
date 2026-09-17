import React, { useState, useEffect } from 'react';
import { Activity, RefreshCw, AlertTriangle, ShieldCheck, Clock } from 'lucide-react';
import { api } from '../../api/client';
import { AuditLogItem } from '../../types';

export const ActivityPage: React.FC = () => {
  const [logs, setLogs] = useState<AuditLogItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchActivity = async () => {
      try {
        setLoading(true);
        const data = await api.getUserActivity();
        setLogs(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load user activity log.');
      } finally {
        setLoading(false);
      }
    };
    fetchActivity();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <span className="text-[10px] font-mono font-bold tracking-widest text-cyan-400 uppercase">
          Tamper-Evident Trail
        </span>
        <h1 className="text-2xl font-bold text-white font-mono mt-1">Personal Activity & Audit</h1>
        <p className="text-xs text-slate-400 font-mono mt-1">
          Complete cryptographic history of all actions performed by your user account.
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
            Loading cryptographic audit history...
          </div>
        ) : logs.length === 0 ? (
          <div className="py-16 text-center text-slate-500 font-mono text-xs">
            No activity records found for this account.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-xs">
              <thead className="bg-[#0c1222] border-b border-slate-800 text-slate-400 text-[11px] uppercase tracking-wider">
                <tr>
                  <th className="py-3.5 px-4 font-semibold">Seq #</th>
                  <th className="py-3.5 px-4 font-semibold">Action</th>
                  <th className="py-3.5 px-4 font-semibold">Resource</th>
                  <th className="py-3.5 px-4 font-semibold">Outcome</th>
                  <th className="py-3.5 px-4 font-semibold">IP Address</th>
                  <th className="py-3.5 px-4 font-semibold">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {logs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-800/30 transition">
                    <td className="py-3 px-4 font-bold text-cyan-400">#{log.sequence_num}</td>
                    <td className="py-3 px-4 font-semibold text-white">{log.action}</td>
                    <td className="py-3 px-4 text-slate-400">
                      {log.resource_type}:{log.resource_id || ''}
                    </td>
                    <td className="py-3 px-4">
                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold ${
                          log.result === 'SUCCESS'
                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                            : log.result === 'QUARANTINE'
                            ? 'bg-rose-500/15 text-rose-300 border border-rose-500/40'
                            : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
                        }`}
                      >
                        {log.result}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-400 text-[11px]">{log.ip_address || '127.0.0.1'}</td>
                    <td className="py-3 px-4 text-slate-500 text-[11px]">
                      {new Date(log.timestamp).toLocaleString()}
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
