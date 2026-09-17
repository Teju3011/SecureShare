import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  UploadCloud,
  FolderLock,
  Share2,
  Activity,
  ShieldCheck,
  Users,
  AlertTriangle,
  FileCheck2,
  Terminal,
  Bug,
  Lock,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const Sidebar: React.FC = () => {
  const { isAdmin } = useAuth();

  const navItemClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium font-mono transition duration-150 ${
      isActive
        ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 shadow-sm shadow-cyan-900/20'
        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
    }`;

  return (
    <aside className="w-64 bg-[#0a0f1d] border-r border-slate-800/80 flex flex-col justify-between p-4 shrink-0 min-h-[calc(100vh-4rem)]">
      <div className="space-y-6">
        {/* User Navigation */}
        <div>
          <span className="text-[10px] font-bold tracking-widest text-slate-500 uppercase px-3 font-mono">
            User Workspace
          </span>
          <nav className="mt-2 space-y-1">
            <NavLink to="/dashboard" className={navItemClass}>
              <LayoutDashboard className="w-4 h-4 text-cyan-400" />
              Overview
            </NavLink>
            <NavLink to="/upload" className={navItemClass}>
              <UploadCloud className="w-4 h-4 text-emerald-400" />
              Upload & Scan
            </NavLink>
            <NavLink to="/files" className={navItemClass}>
              <FolderLock className="w-4 h-4 text-blue-400" />
              My Secure Files
            </NavLink>
            <NavLink to="/shares" className={navItemClass}>
              <Share2 className="w-4 h-4 text-purple-400" />
              Active Shares
            </NavLink>
            <NavLink to="/activity" className={navItemClass}>
              <Activity className="w-4 h-4 text-amber-400" />
              Personal Audit
            </NavLink>
          </nav>
        </div>

        {/* Admin Navigation */}
        {isAdmin && (
          <div>
            <div className="flex items-center justify-between px-3">
              <span className="text-[10px] font-bold tracking-widest text-rose-400 uppercase font-mono flex items-center gap-1">
                <Lock className="w-3 h-3 text-rose-400" />
                Admin SOC Controls
              </span>
            </div>
            <nav className="mt-2 space-y-1">
              <NavLink to="/admin/dashboard" className={navItemClass}>
                <ShieldCheck className="w-4 h-4 text-rose-400" />
                SOC Dashboard
              </NavLink>
              <NavLink to="/admin/quarantine" className={navItemClass}>
                <AlertTriangle className="w-4 h-4 text-amber-400" />
                Quarantine Center
              </NavLink>
              <NavLink to="/admin/audit-logs" className={navItemClass}>
                <FileCheck2 className="w-4 h-4 text-cyan-400" />
                Tamper-Evident Logs
              </NavLink>
              <NavLink to="/admin/users" className={navItemClass}>
                <Users className="w-4 h-4 text-indigo-400" />
                User Management
              </NavLink>
              <NavLink to="/admin/cicd" className={navItemClass}>
                <Terminal className="w-4 h-4 text-emerald-400" />
                CI/CD DevSecOps
              </NavLink>
              <NavLink to="/admin/findings" className={navItemClass}>
                <Bug className="w-4 h-4 text-orange-400" />
                Security Findings
              </NavLink>
            </nav>
          </div>
        )}
      </div>

      {/* System Status footer */}
      <div className="bg-[#0f172a] border border-slate-800 rounded-lg p-3 text-[11px] font-mono">
        <div className="flex items-center justify-between text-slate-400">
          <span>Engine:</span>
          <span className="text-emerald-400 font-semibold">ClamAV + Signatures</span>
        </div>
        <div className="flex items-center justify-between text-slate-400 mt-1">
          <span>Storage:</span>
          <span className="text-cyan-400 font-semibold">AES-GCM (Isolated)</span>
        </div>
      </div>
    </aside>
  );
};
