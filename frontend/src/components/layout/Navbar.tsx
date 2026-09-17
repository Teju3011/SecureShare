import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Shield, Lock, LogOut, User as UserIcon, ShieldAlert } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const Navbar: React.FC = () => {
  const { user, isAdmin, logout, loginAsDemo } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <header className="h-16 bg-[#0c1222]/90 backdrop-blur border-b border-slate-800/80 px-6 flex items-center justify-between sticky top-0 z-40">
      <div className="flex items-center gap-3">
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-cyan-600 to-emerald-500 p-0.5 shadow-lg shadow-cyan-900/30 group-hover:scale-105 transition">
            <div className="w-full h-full bg-[#090e1a] rounded-[7px] flex items-center justify-center">
              <Shield className="w-5 h-5 text-cyan-400" />
            </div>
          </div>
          <div>
            <span className="font-mono font-bold tracking-wider text-base text-white flex items-center gap-1.5">
              SECURE<span className="text-cyan-400">SHARE</span>
            </span>
            <span className="text-[10px] font-mono text-slate-400 block -mt-1 tracking-widest uppercase">
              Automated Validation
            </span>
          </div>
        </Link>

        <div className="hidden lg:flex items-center gap-2 ml-6 pl-6 border-l border-slate-800">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            ZERO-TRUST ENFORCED
          </span>
          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-medium bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
            <Lock className="w-3 h-3 text-cyan-400" />
            AES-256-GCM AT REST
          </span>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {user ? (
          <>
            {/* Quick Demo Switcher */}
            <div className="hidden md:flex items-center gap-1.5 bg-slate-900/80 border border-slate-800 rounded-lg p-1 text-xs font-mono">
              <span className="text-slate-500 px-2">Switch:</span>
              <button
                onClick={() => loginAsDemo('admin')}
                className={`px-2.5 py-1 rounded transition ${
                  isAdmin ? 'bg-cyan-500/20 text-cyan-300 font-bold' : 'text-slate-400 hover:text-white'
                }`}
                title="Login as Administrator"
              >
                Admin (SOC)
              </button>
              <button
                onClick={() => loginAsDemo('alice')}
                className={`px-2.5 py-1 rounded transition ${
                  !isAdmin ? 'bg-cyan-500/20 text-cyan-300 font-bold' : 'text-slate-400 hover:text-white'
                }`}
                title="Login as Alice (Standard User)"
              >
                Alice (User)
              </button>
            </div>

            {/* Profile Info */}
            <div className="flex items-center gap-3 pl-3 border-l border-slate-800">
              <div className="text-right hidden sm:block">
                <span className="text-xs font-semibold text-white block">{user.full_name}</span>
                <span
                  className={`text-[10px] font-mono px-1.5 py-0.2 rounded uppercase ${
                    isAdmin
                      ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                      : 'bg-slate-800 text-slate-300 border border-slate-700'
                  }`}
                >
                  {user.role}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="p-2 rounded-lg bg-slate-800/80 hover:bg-rose-500/20 text-slate-400 hover:text-rose-300 border border-slate-700 hover:border-rose-500/30 transition"
                title="Sign out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </>
        ) : (
          <div className="flex items-center gap-2">
            <Link
              to="/login"
              className="text-xs font-mono px-3 py-1.5 rounded-lg text-slate-300 hover:text-white border border-slate-700 hover:border-slate-600 transition"
            >
              Sign In
            </Link>
            <Link
              to="/register"
              className="text-xs font-mono px-3.5 py-1.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black font-semibold transition shadow-md shadow-cyan-500/20"
            >
              Get Started
            </Link>
          </div>
        )}
      </div>
    </header>
  );
};
