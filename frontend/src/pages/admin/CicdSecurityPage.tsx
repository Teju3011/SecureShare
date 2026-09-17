import React, { useState, useEffect } from 'react';
import {
  Terminal,
  ShieldCheck,
  ShieldAlert,
  Play,
  RefreshCw,
  AlertTriangle,
  GitBranch,
  GitCommit,
  Clock,
  CheckCircle2,
  XCircle,
  Bug,
} from 'lucide-react';
import { api } from '../../api/client';
import { PipelineRunItem } from '../../types';

export const CicdSecurityPage: React.FC = () => {
  const [pipelineRuns, setPipelineRuns] = useState<PipelineRunItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [triggering, setTriggering] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const fetchRuns = async () => {
    try {
      setLoading(true);
      const data = await api.listPipelineRuns();
      setPipelineRuns(data);
    } catch (err: any) {
      setError(err.message || 'Failed to retrieve CI/CD pipeline history.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRuns();
  }, []);

  const handleTrigger = async (simulateFail = false) => {
    setTriggering(true);
    setError(null);
    setSuccessMsg(null);
    try {
      const res = await api.triggerPipelineScan('main', simulateFail);
      setPipelineRuns([res, ...pipelineRuns]);
      if (res.is_blocked) {
        setSuccessMsg(`Scan completed: Security Gate activated! Deployment BLOCKED due to ${res.critical_count} Critical finding(s).`);
      } else {
        setSuccessMsg('Scan completed: Security Gate verified. Clean deployment ALLOWED.');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to trigger scan.');
    } finally {
      setTriggering(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-[10px] font-mono font-bold tracking-widest text-emerald-400 uppercase">
            DevSecOps Automated Pipeline
          </span>
          <h1 className="text-2xl font-bold text-white font-mono mt-1">CI/CD Security Pipeline</h1>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Automated SAST (Semgrep), Dependency Scanning, DAST (OWASP ZAP), and Zero-Tolerance Security Gate.
          </p>
        </div>

        {/* Action Triggers */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => handleTrigger(false)}
            disabled={triggering}
            className="px-3.5 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-black text-xs font-mono font-bold transition flex items-center gap-1.5 shadow-lg shadow-emerald-500/20"
          >
            <Play className="w-3.5 h-3.5" />
            Trigger Clean Scan
          </button>
          <button
            onClick={() => handleTrigger(true)}
            disabled={triggering}
            className="px-3.5 py-2 rounded-lg bg-rose-500/15 hover:bg-rose-500/25 text-rose-300 border border-rose-500/30 text-xs font-mono font-bold transition flex items-center gap-1.5"
          >
            <ShieldAlert className="w-3.5 h-3.5" />
            Simulate Gate Block
          </button>
        </div>
      </div>

      {/* Security Gate Policy Overview Card */}
      <div className="bg-[#111827]/80 border border-slate-800 rounded-2xl p-6 backdrop-blur space-y-4">
        <h3 className="text-xs font-bold text-white font-mono uppercase tracking-wider flex items-center gap-2">
          <Terminal className="w-4 h-4 text-cyan-400" />
          Continuous Delivery Security Gate Rule
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs font-mono">
          <div className="p-3 bg-black/40 border border-slate-800 rounded-xl">
            <span className="text-slate-400 text-[11px] block">Stage 1: SAST</span>
            <span className="font-bold text-cyan-400">Semgrep Ruleset</span>
            <p className="text-[10px] text-slate-500 mt-1">Detects SQLi, XSS, Path Traversal</p>
          </div>
          <div className="p-3 bg-black/40 border border-slate-800 rounded-xl">
            <span className="text-slate-400 text-[11px] block">Stage 2: SCA</span>
            <span className="font-bold text-cyan-400">pip-audit / npm audit</span>
            <p className="text-[10px] text-slate-500 mt-1">Identifies vulnerable dependencies</p>
          </div>
          <div className="p-3 bg-black/40 border border-slate-800 rounded-xl">
            <span className="text-slate-400 text-[11px] block">Stage 3: DAST</span>
            <span className="font-bold text-cyan-400">OWASP ZAP Baseline</span>
            <p className="text-[10px] text-slate-500 mt-1">Dynamic API security scan</p>
          </div>
          <div className="p-3 bg-rose-950/20 border border-rose-500/30 rounded-xl">
            <span className="text-rose-400 text-[11px] block">Stage 4: Quality Gate</span>
            <span className="font-bold text-rose-300">Critical Finding: BLOCK</span>
            <p className="text-[10px] text-slate-400 mt-1">Deployment automatically halted</p>
          </div>
        </div>
      </div>

      {successMsg && (
        <div className="p-3.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 flex items-center gap-2.5 text-emerald-300 text-xs font-mono">
          <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-400" />
          <span>{successMsg}</span>
        </div>
      )}

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-500/15 border border-rose-500/30 flex items-center gap-2.5 text-rose-300 text-xs font-mono">
          <AlertTriangle className="w-4 h-4 shrink-0 text-rose-400" />
          <span>{error}</span>
        </div>
      )}

      {/* Pipeline Runs Table */}
      <div className="bg-[#111827]/80 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        {loading ? (
          <div className="py-16 text-center text-slate-500 font-mono text-xs flex items-center justify-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin text-emerald-400" />
            Loading CI/CD runs...
          </div>
        ) : pipelineRuns.length === 0 ? (
          <div className="py-16 text-center text-slate-500 font-mono text-xs">
            No pipeline runs recorded yet. Click "Trigger Clean Scan" to start.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-xs">
              <thead className="bg-[#0c1222] border-b border-slate-800 text-slate-400 text-[11px] uppercase tracking-wider">
                <tr>
                  <th className="py-3.5 px-4 font-semibold">Commit & Branch</th>
                  <th className="py-3.5 px-4 font-semibold">Triggered By</th>
                  <th className="py-3.5 px-4 font-semibold">Findings Breakdown</th>
                  <th className="py-3.5 px-4 font-semibold">Security Gate Action</th>
                  <th className="py-3.5 px-4 font-semibold">Status</th>
                  <th className="py-3.5 px-4 font-semibold">Execution Time</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {pipelineRuns.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-800/30 transition">
                    <td className="py-3.5 px-4 font-bold text-white flex items-center gap-2">
                      <GitCommit className="w-4 h-4 text-cyan-400" />
                      <span>{p.commit_hash}</span>
                      <span className="text-slate-500 font-normal">({p.branch})</span>
                    </td>
                    <td className="py-3.5 px-4 text-slate-300">{p.triggered_by}</td>
                    <td className="py-3.5 px-4">
                      <div className="flex items-center gap-1.5 text-[11px]">
                        {p.critical_count > 0 && (
                          <span className="px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold border border-rose-500/30">
                            {p.critical_count} Critical
                          </span>
                        )}
                        {p.high_count > 0 && (
                          <span className="px-1.5 py-0.5 rounded bg-orange-500/20 text-orange-300 font-bold border border-orange-500/30">
                            {p.high_count} High
                          </span>
                        )}
                        {p.medium_count > 0 && (
                          <span className="px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
                            {p.medium_count} Med
                          </span>
                        )}
                        {p.low_count > 0 && (
                          <span className="px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                            {p.low_count} Low
                          </span>
                        )}
                        {p.total_findings === 0 && (
                          <span className="text-slate-500">0 findings</span>
                        )}
                      </div>
                    </td>
                    <td className="py-3.5 px-4">
                      <span
                        className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-bold ${
                          p.is_blocked
                            ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                            : 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30'
                        }`}
                      >
                        {p.is_blocked ? (
                          <>
                            <XCircle className="w-3 h-3 text-rose-400" /> DEPLOYMENT BLOCKED
                          </>
                        ) : (
                          <>
                            <CheckCircle2 className="w-3 h-3 text-emerald-400" /> DEPLOYMENT ALLOWED
                          </>
                        )}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-bold">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] ${
                          p.status === 'PASSED'
                            ? 'bg-emerald-500/10 text-emerald-400'
                            : p.status === 'BLOCKED'
                            ? 'bg-rose-500/15 text-rose-300'
                            : 'bg-cyan-500/10 text-cyan-400 animate-pulse'
                        }`}
                      >
                        {p.status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-slate-500 text-[11px]">
                      {new Date(p.started_at).toLocaleString()}
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
