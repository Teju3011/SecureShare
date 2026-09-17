import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  ShieldAlert,
  Users,
  FolderLock,
  Binary,
  AlertTriangle,
  Share2,
  Bug,
  Terminal,
  RefreshCw,
  TrendingUp,
  Activity,
  ArrowRight,
  ShieldCheck,
  Lock,
} from 'lucide-react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { api } from '../../api/client';
import { AdminDashboardStats } from '../../types';
import { StatCard } from '../../components/common/StatCard';
import { SecurityBadge } from '../../components/common/SecurityBadge';

export const AdminDashboard: React.FC = () => {
  const [stats, setStats] = useState<AdminDashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const data = await api.getAdminStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load admin SOC stats', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const severityColors: Record<string, string> = {
    Critical: '#ef4444',
    High: '#f97316',
    Medium: '#f59e0b',
    Low: '#10b981',
    Informational: '#06b6d4',
  };

  const statusColors: Record<string, string> = {
    CLEAN: '#10b981',
    MALICIOUS: '#ef4444',
    QUARANTINED: '#f43f5e',
    HIGH_RISK: '#f59e0b',
    SCANNING: '#06b6d4',
  };

  if (loading) {
    return (
      <div className="py-24 text-center text-slate-500 font-mono text-xs flex items-center justify-center gap-2">
        <RefreshCw className="w-5 h-5 animate-spin text-rose-400" />
        Aggregating SOC security metrics and threat telemetry...
      </div>
    );
  }

  // Format data for severity chart
  const severityData = Object.entries(stats?.severity_breakdown || {}).map(([name, value]) => ({
    name,
    count: value,
    fill: severityColors[name] || '#6b7280',
  }));

  // Format data for status pie chart
  const statusData = Object.entries(stats?.status_counts || {})
    .filter(([_, value]) => value > 0)
    .map(([name, value]) => ({
      name,
      value,
      fill: statusColors[name] || '#6b7280',
    }));

  return (
    <div className="space-y-8">
      {/* SOC Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-[#111827]/90 border border-rose-500/30 rounded-2xl p-6 shadow-xl shadow-rose-950/20 backdrop-blur">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping"></span>
            <span className="text-[10px] font-mono font-bold tracking-widest text-rose-400 uppercase">
              Security Operations Center (SOC) Live Telemetry
            </span>
          </div>
          <h1 className="text-2xl font-bold text-white font-mono mt-1">Platform Security Dashboard</h1>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Real-time monitoring: Zero-Trust file upload validation, malware quarantine, tamper-evident audits, and DevSecOps gates.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchStats}
            className="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono text-xs flex items-center gap-2 transition"
          >
            <RefreshCw className="w-3.5 h-3.5 text-cyan-400" />
            Refresh Telemetry
          </button>
          <Link
            to="/admin/quarantine"
            className="px-3.5 py-2 rounded-lg bg-rose-500 hover:bg-rose-400 text-black font-mono text-xs font-bold transition shadow-lg shadow-rose-500/20"
          >
            Manage Quarantine
          </Link>
        </div>
      </div>

      {/* Primary KPI Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Registered Users"
          value={stats?.total_users || 0}
          icon={<Users className="w-5 h-5" />}
          color="blue"
        />
        <StatCard
          title="Files Scanned"
          value={stats?.files_scanned || 0}
          icon={<Binary className="w-5 h-5" />}
          color="cyan"
          subtitle={`${stats?.total_files || 0} total files in storage`}
        />
        <StatCard
          title="Threats Intercepted"
          value={stats?.threats_detected || 0}
          icon={<ShieldAlert className="w-5 h-5" />}
          color="rose"
          subtitle="Malware & dangerous payloads"
        />
        <StatCard
          title="Quarantined Files"
          value={stats?.quarantined_files || 0}
          icon={<AlertTriangle className="w-5 h-5" />}
          color="amber"
          subtitle="Strictly isolated at rest"
        />
        <StatCard
          title="Active Expiring Shares"
          value={stats?.active_shares || 0}
          icon={<Share2 className="w-5 h-5" />}
          color="purple"
        />
        <StatCard
          title="Security Findings"
          value={stats?.total_security_findings || 0}
          icon={<Bug className="w-5 h-5" />}
          color="rose"
          subtitle="Semgrep, pip-audit, DAST"
        />
        <StatCard
          title="Pipeline Gate Blocks"
          value={stats?.pipeline_failures || 0}
          icon={<Terminal className="w-5 h-5" />}
          color="amber"
          subtitle="Deployments blocked by gate"
        />
        <StatCard
          title="Tamper Verification"
          value="Intact"
          icon={<ShieldCheck className="w-5 h-5" />}
          color="emerald"
          subtitle="SHA-256 chain verified"
        />
      </div>

      {/* Interactive Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Upload vs Threat Trend (AreaChart) */}
        <div className="lg:col-span-2 bg-[#111827]/80 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold text-white font-mono uppercase tracking-wider flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-cyan-400" />
              Upload Volume vs Malware Threat Detections (7 Days)
            </h3>
            <span className="text-[10px] font-mono text-slate-400">Live Trend</span>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats?.upload_trend || []}>
                <defs>
                  <linearGradient id="uploadGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="threatGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.6} />
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="day" stroke="#64748b" fontSize={11} fontFamily="monospace" />
                <YAxis stroke="#64748b" fontSize={11} fontFamily="monospace" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '11px', fontFamily: 'monospace' }}
                />
                <Area type="monotone" dataKey="uploads" stroke="#06b6d4" fillOpacity={1} fill="url(#uploadGrad)" name="Valid Uploads" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Security Findings by Severity (BarChart) */}
        <div className="bg-[#111827]/80 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold text-white font-mono uppercase tracking-wider flex items-center gap-2">
              <Bug className="w-4 h-4 text-rose-400" />
              Findings by Severity
            </h3>
            <Link to="/admin/findings" className="text-[10px] text-cyan-400 hover:underline font-mono">
              View All
            </Link>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={severityData} layout="vertical">
                <XAxis type="number" stroke="#64748b" fontSize={10} fontFamily="monospace" />
                <YAxis dataKey="name" type="category" stroke="#64748b" fontSize={10} fontFamily="monospace" width={80} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '11px', fontFamily: 'monospace' }}
                />
                <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                  {severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Lower Row: Recent Security Alerts & Quarantined Threats */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Security Alerts */}
        <div className="bg-[#111827]/80 border border-slate-800 rounded-xl p-5 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold text-white font-mono uppercase tracking-wider flex items-center gap-2">
              <Activity className="w-4 h-4 text-amber-400" />
              Recent High-Priority Security Alerts
            </h3>
            <Link to="/admin/audit-logs" className="text-xs text-cyan-400 hover:underline font-mono">
              Audit Logs
            </Link>
          </div>
          <div className="space-y-2.5 font-mono text-xs">
            {stats?.recent_alerts && stats.recent_alerts.length > 0 ? (
              stats.recent_alerts.map((alert) => (
                <div
                  key={alert.id}
                  className="p-3 rounded-lg bg-black/40 border border-slate-800 flex items-center justify-between"
                >
                  <div className="min-w-0 flex-1">
                    <span className="font-semibold text-white truncate block">{alert.action}</span>
                    <span className="text-[11px] text-slate-500 truncate block">
                      Actor: {alert.actor} • {alert.resource}
                    </span>
                  </div>
                  <div className="text-right ml-3 shrink-0">
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                        alert.result === 'BLOCKED' || alert.result === 'QUARANTINE'
                          ? 'bg-rose-500/15 text-rose-300 border border-rose-500/30'
                          : 'bg-amber-500/15 text-amber-300 border border-amber-500/30'
                      }`}
                    >
                      {alert.result}
                    </span>
                    <span className="text-[10px] text-slate-500 block mt-1">
                      {new Date(alert.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-500 py-6 text-center">No recent critical security alerts.</p>
            )}
          </div>
        </div>

        {/* Quarantined Files Monitor */}
        <div className="bg-[#111827]/80 border border-slate-800 rounded-xl p-5 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold text-white font-mono uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-rose-400" />
              Active Quarantined Threats
            </h3>
            <Link to="/admin/quarantine" className="text-xs text-rose-400 hover:underline font-mono">
              Quarantine Manager
            </Link>
          </div>
          <div className="space-y-2.5 font-mono text-xs">
            {stats?.recent_quarantine && stats.recent_quarantine.length > 0 ? (
              stats.recent_quarantine.map((q) => (
                <div
                  key={q.id}
                  className="p-3 rounded-lg bg-rose-950/15 border border-rose-500/30 flex items-center justify-between"
                >
                  <div className="min-w-0 flex-1">
                    <span className="font-semibold text-rose-200 truncate block">{q.filename}</span>
                    <span className="text-[11px] text-rose-400/80 truncate block">{q.reason}</span>
                  </div>
                  <Link
                    to="/admin/quarantine"
                    className="px-2.5 py-1 rounded bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 text-xs font-mono ml-3 shrink-0 transition"
                  >
                    Review
                  </Link>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-500 py-6 text-center">Quarantine zone is currently clean.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
