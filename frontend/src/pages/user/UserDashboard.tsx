import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  FolderLock,
  ShieldCheck,
  RefreshCw,
  AlertTriangle,
  Share2,
  UploadCloud,
  Activity,
  ArrowRight,
  Shield,
  Download,
  Lock,
} from 'lucide-react';
import { api } from '../../api/client';
import { UserDashboardStats } from '../../types';
import { StatCard } from '../../components/common/StatCard';
import { SecurityBadge } from '../../components/common/SecurityBadge';
import { useAuth } from '../../context/AuthContext';

export const UserDashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<UserDashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await api.getUserDashboard();
        setStats(data);
      } catch (err) {
        console.error('Failed to load user dashboard stats', err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20 text-slate-400 font-mono text-xs">
        <RefreshCw className="w-5 h-5 animate-spin mr-2 text-cyan-400" />
        Loading security dashboard...
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-[#111827]/80 border border-slate-800 rounded-2xl p-6 backdrop-blur">
        <div>
          <span className="text-[10px] font-mono font-bold tracking-widest text-cyan-400 uppercase">
            User Workspace
          </span>
          <h1 className="text-2xl font-bold text-white font-mono mt-1">
            Welcome back, {user?.full_name}
          </h1>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Account Role: <span className="text-slate-200 font-bold">{user?.role}</span> •
            MFA Status: <span className={user?.mfa_enabled ? 'text-emerald-400 font-bold' : 'text-amber-400 font-bold'}>
              {user?.mfa_enabled ? 'Active (TOTP)' : 'Disabled'}
            </span>
          </p>
        </div>

        <div className="flex items-center gap-3">
          {!user?.mfa_enabled && (
            <Link
              to="/mfa-setup"
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/30 text-xs font-mono font-semibold transition"
            >
              <Lock className="w-3.5 h-3.5" />
              Enable MFA
            </Link>
          )}
          <Link
            to="/upload"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black text-xs font-mono font-bold shadow-lg shadow-cyan-500/20 transition"
          >
            <UploadCloud className="w-4 h-4" />
            Upload File
          </Link>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard
          title="Total Files"
          value={stats?.total_files || 0}
          icon={<FolderLock className="w-5 h-5" />}
          color="blue"
        />
        <StatCard
          title="Verified Clean"
          value={stats?.safe_files || 0}
          icon={<ShieldCheck className="w-5 h-5" />}
          color="emerald"
        />
        <StatCard
          title="Scanning / In-Flight"
          value={stats?.scanning_files || 0}
          icon={<RefreshCw className="w-5 h-5" />}
          color="cyan"
        />
        <StatCard
          title="Quarantined Threats"
          value={stats?.quarantined_files || 0}
          icon={<AlertTriangle className="w-5 h-5" />}
          color="rose"
        />
        <StatCard
          title="Active Shares"
          value={stats?.active_shares || 0}
          icon={<Share2 className="w-5 h-5" />}
          color="purple"
        />
      </div>

      {/* Quick Action Highlights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link
          to="/upload"
          className="group bg-[#111827]/60 hover:bg-[#111827] border border-slate-800 hover:border-cyan-500/40 rounded-xl p-5 transition space-y-2"
        >
          <div className="flex items-center justify-between">
            <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <UploadCloud className="w-5 h-5" />
            </div>
            <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-cyan-400 group-hover:translate-x-1 transition" />
          </div>
          <h3 className="text-sm font-bold text-white font-mono">Upload & Validate</h3>
          <p className="text-xs text-slate-400 font-mono">
            Execute 6-stage malware, MIME, and script inspection pipeline.
          </p>
        </Link>

        <Link
          to="/files"
          className="group bg-[#111827]/60 hover:bg-[#111827] border border-slate-800 hover:border-emerald-500/40 rounded-xl p-5 transition space-y-2"
        >
          <div className="flex items-center justify-between">
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <FolderLock className="w-5 h-5" />
            </div>
            <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-emerald-400 group-hover:translate-x-1 transition" />
          </div>
          <h3 className="text-sm font-bold text-white font-mono">My Secure Files</h3>
          <p className="text-xs text-slate-400 font-mono">
            View SHA-256 hashes, scan logs, and decrypt files on demand.
          </p>
        </Link>

        <Link
          to="/shares"
          className="group bg-[#111827]/60 hover:bg-[#111827] border border-slate-800 hover:border-purple-500/40 rounded-xl p-5 transition space-y-2"
        >
          <div className="flex items-center justify-between">
            <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/20">
              <Share2 className="w-5 h-5" />
            </div>
            <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-purple-400 group-hover:translate-x-1 transition" />
          </div>
          <h3 className="text-sm font-bold text-white font-mono">Expiring Secure Shares</h3>
          <p className="text-xs text-slate-400 font-mono">
            Generate password-protected links with download limit enforcement.
          </p>
        </Link>
      </div>

      {/* Recent Files & Activity Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Files */}
        <div className="bg-[#111827]/80 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-white font-mono flex items-center gap-2">
              <FolderLock className="w-4 h-4 text-cyan-400" />
              Recent Files
            </h3>
            <Link to="/files" className="text-xs text-cyan-400 hover:underline font-mono">
              View all
            </Link>
          </div>

          {stats?.recent_files && stats.recent_files.length > 0 ? (
            <div className="divide-y divide-slate-800 font-mono text-xs">
              {stats.recent_files.map((file) => (
                <div key={file.id} className="py-3 flex items-center justify-between gap-3">
                  <div className="min-w-0 flex-1">
                    <p className="font-semibold text-white truncate">{file.filename}</p>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      {formatBytes(file.size)} • {file.mime}
                    </p>
                  </div>
                  <SecurityBadge status={file.status} />
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-slate-500 font-mono py-6 text-center">
              No files uploaded yet. Click "Upload File" to start.
            </p>
          )}
        </div>

        {/* Recent Activity */}
        <div className="bg-[#111827]/80 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-white font-mono flex items-center gap-2">
              <Activity className="w-4 h-4 text-amber-400" />
              Recent Personal Activity
            </h3>
            <Link to="/activity" className="text-xs text-cyan-400 hover:underline font-mono">
              Full audit log
            </Link>
          </div>

          {stats?.recent_activity && stats.recent_activity.length > 0 ? (
            <div className="space-y-3 font-mono text-xs">
              {stats.recent_activity.map((act) => (
                <div
                  key={act.id}
                  className="p-2.5 rounded-lg bg-black/30 border border-slate-800 flex items-center justify-between"
                >
                  <div>
                    <span className="font-semibold text-slate-200">{act.action}</span>
                    <span className="text-[11px] text-slate-500 block">{act.resource}</span>
                  </div>
                  <div className="text-right">
                    <span
                      className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                        act.result === 'SUCCESS'
                          ? 'bg-emerald-500/10 text-emerald-400'
                          : act.result === 'QUARANTINE'
                          ? 'bg-rose-500/10 text-rose-400'
                          : 'bg-amber-500/10 text-amber-400'
                      }`}
                    >
                      {act.result}
                    </span>
                    <span className="text-[10px] text-slate-500 block mt-0.5">
                      {new Date(act.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-slate-500 font-mono py-6 text-center">
              No recent security activity logged.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};
