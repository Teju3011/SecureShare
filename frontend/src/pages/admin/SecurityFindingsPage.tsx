import React, { useState, useEffect } from 'react';
import {
  Bug,
  Filter,
  RefreshCw,
  AlertTriangle,
  FileCode,
  ShieldAlert,
  CheckCircle2,
} from 'lucide-react';
import { api } from '../../api/client';
import { SecurityFindingItem } from '../../types';

export const SecurityFindingsPage: React.FC = () => {
  const [findings, setFindings] = useState<SecurityFindingItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [severityFilter, setSeverityFilter] = useState('');
  const [error, setError] = useState<string | null>(null);

  const fetchFindings = async () => {
    try {
      setLoading(true);
      const data = await api.listSecurityFindings(severityFilter || undefined);
      setFindings(data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch security findings.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFindings();
  }, [severityFilter]);

  const severityBadgeClass = (sev: string) => {
    switch (sev) {
      case 'Critical':
        return 'bg-rose-500/20 text-rose-300 border border-rose-500/40';
      case 'High':
        return 'bg-orange-500/20 text-orange-300 border border-orange-500/40';
      case 'Medium':
        return 'bg-amber-500/20 text-amber-300 border border-amber-500/40';
      case 'Low':
        return 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40';
      default:
        return 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-[10px] font-mono font-bold tracking-widest text-orange-400 uppercase">
            Vulnerability Management
          </span>
          <h1 className="text-2xl font-bold text-white font-mono mt-1">Security Findings Repository</h1>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Aggregated vulnerabilities discovered across Static Analysis (Semgrep), Dependencies, and Dynamic DAST.
          </p>
        </div>

        {/* Severity Filter Dropdown */}
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-500" />
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-slate-300 text-xs font-mono focus:outline-none"
          >
            <option value="">All Severities</option>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
            <option value="Informational">Informational</option>
          </select>
        </div>
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-500/15 border border-rose-500/30 flex items-center gap-2.5 text-rose-300 text-xs font-mono">
          <AlertTriangle className="w-4 h-4 shrink-0 text-rose-400" />
          <span>{error}</span>
        </div>
      )}

      {/* Findings List */}
      <div className="bg-[#111827]/80 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        {loading ? (
          <div className="py-16 text-center text-slate-500 font-mono text-xs flex items-center justify-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin text-orange-400" />
            Loading security findings...
          </div>
        ) : findings.length === 0 ? (
          <div className="py-16 text-center text-slate-500 font-mono text-xs">
            No security findings match the selected severity filter.
          </div>
        ) : (
          <div className="divide-y divide-slate-800/60 font-mono text-xs">
            {findings.map((f) => (
              <div key={f.id} className="p-5 hover:bg-slate-800/30 transition space-y-2">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2.5">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${severityBadgeClass(f.severity)}`}>
                      {f.severity}
                    </span>
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] border border-slate-700">
                      {f.tool_name}
                    </span>
                    {f.cve_id && (
                      <span className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 text-[10px] border border-purple-500/30">
                        {f.cve_id}
                      </span>
                    )}
                    <h3 className="font-bold text-white text-sm">{f.title}</h3>
                  </div>

                  <span className="text-slate-500 text-[11px]">
                    {new Date(f.created_at).toLocaleDateString()}
                  </span>
                </div>

                <p className="text-slate-400 text-xs leading-relaxed">{f.description}</p>

                {f.file_path && (
                  <div className="flex items-center gap-1.5 text-[11px] text-cyan-400 bg-black/40 px-2.5 py-1 rounded w-fit border border-slate-800/80">
                    <FileCode className="w-3.5 h-3.5 text-cyan-400" />
                    <span>
                      {f.file_path}
                      {f.line_number ? `:${f.line_number}` : ''}
                    </span>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
