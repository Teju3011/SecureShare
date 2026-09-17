import React from 'react';

interface StatCardProps {
  title: string;
  value: number | string;
  icon: React.ReactNode;
  subtitle?: string;
  color?: 'cyan' | 'emerald' | 'amber' | 'rose' | 'purple' | 'blue';
  trend?: string;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  icon,
  subtitle,
  color = 'cyan',
  trend,
}) => {
  const colorMap = {
    cyan: 'border-cyan-500/30 text-cyan-400 bg-cyan-500/10 shadow-cyan-900/10',
    emerald: 'border-emerald-500/30 text-emerald-400 bg-emerald-500/10 shadow-emerald-900/10',
    amber: 'border-amber-500/30 text-amber-400 bg-amber-500/10 shadow-amber-900/10',
    rose: 'border-rose-500/30 text-rose-400 bg-rose-500/10 shadow-rose-900/10',
    purple: 'border-purple-500/30 text-purple-400 bg-purple-500/10 shadow-purple-900/10',
    blue: 'border-blue-500/30 text-blue-400 bg-blue-500/10 shadow-blue-900/10',
  };

  return (
    <div className="bg-[#111827]/80 backdrop-blur border border-slate-800/80 rounded-xl p-5 hover:border-slate-700 transition duration-200 shadow-lg">
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold tracking-wider text-slate-400 uppercase font-mono">{title}</span>
        <div className={`p-2.5 rounded-lg border ${colorMap[color]}`}>
          {icon}
        </div>
      </div>
      <div className="mt-3 flex items-baseline gap-2">
        <span className="text-3xl font-bold font-mono text-white tracking-tight">{value}</span>
        {trend && (
          <span className="text-xs font-medium text-emerald-400">{trend}</span>
        )}
      </div>
      {subtitle && (
        <p className="mt-1 text-xs text-slate-500">{subtitle}</p>
      )}
    </div>
  );
};
