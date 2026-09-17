import React from 'react';
import { ShieldCheck, ShieldAlert, AlertTriangle, RefreshCw, XCircle } from 'lucide-react';
import { FileStatus } from '../../types';

interface SecurityBadgeProps {
  status: FileStatus | string;
  className?: string;
  showIcon?: boolean;
}

export const SecurityBadge: React.FC<SecurityBadgeProps> = ({
  status,
  className = '',
  showIcon = true,
}) => {
  const norm = status.toUpperCase();

  if (norm === 'CLEAN' || norm === 'PASSED') {
    return (
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 shadow-sm shadow-emerald-900/20 ${className}`}>
        {showIcon && <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />}
        CLEAN / VERIFIED
      </span>
    );
  }

  if (norm === 'SCANNING' || norm === 'VALIDATING' || norm === 'UPLOADING' || norm === 'RUNNING') {
    return (
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 animate-pulse ${className}`}>
        {showIcon && <RefreshCw className="w-3.5 h-3.5 text-cyan-400 animate-spin" />}
        {norm}
      </span>
    );
  }

  if (norm === 'HIGH_RISK' || norm === 'WARNING') {
    return (
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/30 ${className}`}>
        {showIcon && <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />}
        HIGH RISK
      </span>
    );
  }

  if (norm === 'MALICIOUS') {
    return (
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-500/15 text-rose-400 border border-rose-500/40 shadow-sm shadow-rose-900/30 ${className}`}>
        {showIcon && <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />}
        MALICIOUS
      </span>
    );
  }

  if (norm === 'QUARANTINED' || norm === 'BLOCKED') {
    return (
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-500/15 text-rose-300 border border-rose-500/40 ${className}`}>
        {showIcon && <XCircle className="w-3.5 h-3.5 text-rose-400" />}
        QUARANTINED
      </span>
    );
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-800 text-slate-300 border border-slate-700 ${className}`}>
      {status}
    </span>
  );
};
