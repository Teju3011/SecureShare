import React from 'react';
import { Link } from 'react-router-dom';
import {
  Shield,
  Lock,
  FileCheck,
  AlertTriangle,
  Terminal,
  FileKey,
  Database,
  ArrowRight,
  CheckCircle2,
  Cpu,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const LandingPage: React.FC = () => {
  const { loginAsDemo, isAuthenticated } = useAuth();

  return (
    <div className="space-y-16 py-6">
      {/* Hero Section */}
      <div className="text-center max-w-3xl mx-auto space-y-6">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border border-cyan-500/30 bg-cyan-500/10 text-cyan-300 text-xs font-mono font-medium shadow-lg shadow-cyan-900/20">
          <Shield className="w-4 h-4 text-cyan-400" />
          Software Engineering + Cybersecurity Capstone Platform
        </div>
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-tight font-mono">
          SECURE<span className="text-cyan-400">SHARE</span>
        </h1>
        <p className="text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
          Zero-Trust secure file sharing with automated multi-stage malware scanning,
          dangerous script detection, AES-256-GCM encryption at rest, and tamper-evident audit chains.
        </p>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          {isAuthenticated ? (
            <Link
              to="/dashboard"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black font-semibold font-mono text-sm shadow-xl shadow-cyan-500/20 transition"
            >
              Open Dashboard
              <ArrowRight className="w-4 h-4" />
            </Link>
          ) : (
            <>
              <Link
                to="/register"
                className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black font-semibold font-mono text-sm shadow-xl shadow-cyan-500/20 transition"
              >
                Get Started
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                to="/login"
                className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-mono text-sm border border-slate-700 transition"
              >
                Sign In
              </Link>
            </>
          )}

          {/* Quick Demo Access */}
          <div className="flex items-center gap-2 bg-[#111827] border border-cyan-500/30 rounded-xl p-1.5">
            <span className="text-xs text-slate-400 font-mono px-2">Instant Demo:</span>
            <button
              onClick={() => loginAsDemo('admin')}
              className="px-3 py-1.5 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 text-xs font-mono font-bold transition border border-rose-500/30"
            >
              Admin SOC
            </button>
            <button
              onClick={() => loginAsDemo('alice')}
              className="px-3 py-1.5 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 text-xs font-mono font-bold transition border border-cyan-500/30"
            >
              Standard User
            </button>
          </div>
        </div>
      </div>

      {/* Security Architecture Flow */}
      <div className="bg-[#111827]/60 border border-slate-800 rounded-2xl p-8 backdrop-blur shadow-2xl">
        <div className="text-center max-w-xl mx-auto mb-8">
          <h2 className="text-sm font-bold font-mono tracking-widest text-cyan-400 uppercase">
            Core Application Security Flow
          </h2>
          <p className="text-xl font-bold text-white mt-1">Multi-Stage Inspection Pipeline</p>
          <p className="text-xs text-slate-400 mt-1">Files are NEVER downloadable until validated CLEAN</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-6 gap-3 text-center">
          {[
            { step: '01', title: 'File Upload', desc: 'Size < 50MB & SHA-256' },
            { step: '02', title: 'MIME Check', desc: 'MIME vs Declared' },
            { step: '03', title: 'Magic Bytes', desc: 'Binary Signature' },
            { step: '04', title: 'Script Filter', desc: 'PE, ELF, Macros' },
            { step: '05', title: 'ClamAV Scan', desc: 'Malware & EICAR' },
            { step: '06', title: 'AES-256 Crypt', desc: 'GCM Authenticated' },
          ].map((item, idx) => (
            <div key={idx} className="bg-black/40 border border-slate-800 p-4 rounded-xl flex flex-col justify-between">
              <span className="text-[10px] font-mono text-cyan-400 font-bold">{item.step}</span>
              <h4 className="text-xs font-bold text-white font-mono mt-1">{item.title}</h4>
              <p className="text-[11px] text-slate-400 font-mono mt-1">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Feature Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-[#111827]/70 border border-slate-800 p-6 rounded-xl space-y-3">
          <div className="w-10 h-10 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Shield className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white font-mono">Automated Malware & EICAR</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Integration with ClamAV daemon and internal heuristic signature scanners. Includes safe EICAR test file detection and fail-closed security policy.
          </p>
        </div>

        <div className="bg-[#111827]/70 border border-slate-800 p-6 rounded-xl space-y-3">
          <div className="w-10 h-10 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Lock className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white font-mono">AES-256-GCM Encryption</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            All stored files are encrypted using unique 96-bit nonces before storage in segregated clean and quarantine partitions.
          </p>
        </div>

        <div className="bg-[#111827]/70 border border-slate-800 p-6 rounded-xl space-y-3">
          <div className="w-10 h-10 rounded-lg bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400">
            <FileKey className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white font-mono">Tamper-Evident Audit Chain</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Every authentication, upload, quarantine, and download event is cryptographically hashed in a SHA-256 blockchain-style sequence.
          </p>
        </div>
      </div>
    </div>
  );
};
