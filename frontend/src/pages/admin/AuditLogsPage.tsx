import React, { useState, useEffect } from 'react';
import {
  FileCheck2,
  ShieldCheck,
  ShieldAlert,
  Search,
  Filter,
  RefreshCw,
  AlertTriangle,
  Lock,
  Binary,
  CheckCircle2,
} from 'lucide-react';
import { api } from '../../api/client';
import { AuditLogItem, AuditVerificationResult } from '../../types';

export const AuditLogsPage: React.FC = () => {
  const [logs, setLogs] = useState<AuditLogItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [verifying, setVerifying] = useState(false);
  const [verificationResult, setVerificationResult] = useState<AuditVerificationResult | null>(null);
  const [actionFilter, setActionFilter] = useState('');
  const [resultFilter, setResultFilter] = useState('');
  const [search, setSearch] = useState('');
  const [error, setError] = useState<string | null>(null);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const data = await api.listAuditLogs(actionFilter || undefined, resultFilter || undefined);
      setLogs(data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch audit log trail.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [actionFilter, resultFilter]);

  const handleVerifyChain = async () => {
    setVerifying(true);
    setError(null);
    try {
      const res = await api.verifyAuditLogs();
      setVerificationResult(res);
    } catch (err: any) {
      setError(err.message || 'Audit chain verification execution error.');
    } finally {
      setVerifying(false);
    }
  };

  const filteredLogs = logs.filter(
    (l) =>
      l.action.toLowerCase().includes(search.toLowerCase()) ||
      (l.actor_email || '').toLowerCase().includes(search.toLowerCase()) ||
      l.resource_type.toLowerCase().includes(search.toLowerCase()) ||
      (l.entry_hash || '').toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-[10px] font-mono font-bold tracking-widest text-cyan-400 uppercase">
            Blockchain-Style SHA-256 Hash Chaining
          </span>
          <h1 className="text-2xl font-bold text-white font-mono mt-1">Tamper-Evident Audit Logs</h1>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Every security event is cryptographically linked: entry_hash = HASH(previous_hash + event_data).
          </p>
        </div>

        {/* Cryptographic Verification Trigger */}
        <button
          onClick={handleVerifyChain}
          disabled={verifying}
          className="px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-black text-xs font-mono font-bold shadow-lg shadow-emerald-500/20 transition flex items-center gap-2 w-fit"
        >
          {verifying ? (
            <RefreshCw className="w-4 h-4 animate-spin" />
          ) : (
            <ShieldCheck className="w-4 h-4" />
          )}
          {verifying ? 'Verifying Hashes...' : 'Verify Cryptographic Chain'}
        </button>
      </div>

      {/* Verification Status Banner */}
      {verificationResult && (
        <div
          className={`p-4 rounded-xl border flex items-center justify-between backdrop-blur ${
            verificationResult.is_valid
              ? 'bg-emerald-950/30 border-emerald-500/40 text-emerald-300'
              : 'bg-rose-950/30 border-rose-500/40 text-rose-300'
          }`}
        >
          <div className="flex items-center gap-3">
            {verificationResult.is_valid ? (
              <CheckCircle2 className="w-6 h-6 text-emerald-400" />
            ) : (
              <ShieldAlert className="w-6 h-6 text-rose-400" />
            )}
            <div>
              <h4 className="text-sm font-bold font-mono">
                {verificationResult.is_valid
                  ? 'Cryptographic Hash Chain Verified Valid'
                  : 'INTEGRITY VIOLATION DETECTED'}
              </h4>
              <p className="text-xs font-mono opacity-90 mt-0.5">
                {verificationResult.message}
              </p>
            </div>
          </div>
          <div className="text-right font-mono text-xs hidden sm:block">
            <span className="text-slate-400 block text-[10px] uppercase">Chain Length</span>
            <span className="font-bold text-white">{verificationResult.total_records} Records</span>
          </div>
        </div>
      )}

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-500/15 border border-rose-500/30 flex items-center gap-2.5 text-rose-300 text-xs font-mono">
          <AlertTriangle className="w-4 h-4 shrink-0 text-rose-400" />
          <span>{error}</span>
        </div>
      )}

      {/* Filters & Search */}
      <div className="bg-[#111827]/80 border border-slate-800 rounded-xl p-3 flex flex-wrap items-center gap-3">
        <div className="flex-1 min-w-[200px] flex items-center gap-2">
          <Search className="w-4 h-4 text-slate-500" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search action, actor, resource, or hash..."
            className="w-full bg-transparent border-none text-white text-xs font-mono placeholder-slate-500 focus:outline-none"
          />
        </div>

        <select
          value={actionFilter}
          onChange={(e) => setActionFilter(e.target.value)}
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-slate-300 text-xs font-mono focus:outline-none"
        >
          <option value="">All Actions</option>
          <option value="FILE_UPLOAD_SCAN">FILE_UPLOAD_SCAN</option>
          <option value="MALWARE_DETECTED_QUARANTINE">MALWARE_DETECTED_QUARANTINE</option>
          <option value="DANGEROUS_FILE_BLOCKED">DANGEROUS_FILE_BLOCKED</option>
          <option value="SHARE_CREATE">SHARE_CREATE</option>
          <option value="SHARE_ACCESS_FAILED">SHARE_ACCESS_FAILED</option>
          <option value="USER_LOGIN_SUCCESS">USER_LOGIN_SUCCESS</option>
          <option value="CI_CD_SCAN_EXECUTION">CI_CD_SCAN_EXECUTION</option>
        </select>

        <select
          value={resultFilter}
          onChange={(e) => setResultFilter(e.target.value)}
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-slate-300 text-xs font-mono focus:outline-none"
        >
          <option value="">All Outcomes</option>
          <option value="SUCCESS">SUCCESS</option>
          <option value="QUARANTINE">QUARANTINE</option>
          <option value="BLOCKED">BLOCKED</option>
          <option value="FAILURE">FAILURE</option>
        </select>
      </div>

      {/* Audit Log Table */}
      <div className="bg-[#111827]/80 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        {loading ? (
          <div className="py-16 text-center text-slate-500 font-mono text-xs flex items-center justify-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin text-cyan-400" />
            Loading cryptographic audit trail...
          </div>
        ) : filteredLogs.length === 0 ? (
          <div className="py-16 text-center text-slate-500 font-mono text-xs">
            No audit records match the current filter.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-xs">
              <thead className="bg-[#0c1222] border-b border-slate-800 text-slate-400 text-[11px] uppercase tracking-wider">
                <tr>
                  <th className="py-3.5 px-4 font-semibold">Seq #</th>
                  <th className="py-3.5 px-4 font-semibold">Action</th>
                  <th className="py-3.5 px-4 font-semibold">Actor</th>
                  <th className="py-3.5 px-4 font-semibold">Resource</th>
                  <th className="py-3.5 px-4 font-semibold">Outcome</th>
                  <th className="py-3.5 px-4 font-semibold">Entry SHA-256 Hash</th>
                  <th className="py-3.5 px-4 font-semibold">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {filteredLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-800/30 transition">
                    <td className="py-3 px-4 font-bold text-cyan-400">#{log.sequence_num}</td>
                    <td className="py-3 px-4 font-semibold text-white max-w-[180px] truncate">
                      {log.action}
                    </td>
                    <td className="py-3 px-4 text-slate-300 max-w-[180px] truncate">
                      {log.actor_email || 'System'}
                    </td>
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
                    <td className="py-3 px-4 text-slate-400 font-mono text-[11px]">
                      <span title={`Previous Hash: ${log.previous_hash}\nEntry Hash: ${log.entry_hash}`}>
                        {log.entry_hash.substring(0, 12)}...
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-500 text-[11px] whitespace-nowrap">
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
