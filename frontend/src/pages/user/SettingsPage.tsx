import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { Shield, Key, Bell, Smartphone, Lock, CheckCircle2 } from 'lucide-react';
import { Link } from 'react-router-dom';

export const SettingsPage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-indigo-50 text-indigo-600 rounded-lg">
            <Shield className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-900">Security & Account Settings</h1>
            <p className="text-xs text-slate-500 mt-0.5">
              Review credential derivation, MFA policy, session tokens, and cryptographic parameters.
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Profile Card */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-4">
          <h2 className="text-sm font-semibold text-slate-900 flex items-center space-x-2">
            <Lock className="w-4 h-4 text-indigo-600" />
            <span>Profile & Access Role</span>
          </h2>
          <div className="space-y-3 text-xs">
            <div>
              <span className="text-slate-400 block text-[11px]">Full Name</span>
              <span className="font-semibold text-slate-800">{user?.full_name || 'Demo Persona'}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[11px]">Email Address</span>
              <span className="font-semibold text-slate-800">{user?.email || 'user@example.com'}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[11px]">Server-Enforced Role</span>
              <span className="inline-block mt-0.5 px-2.5 py-0.5 rounded font-mono text-[10px] font-bold bg-indigo-50 text-indigo-700">
                {user?.role || 'USER'}
              </span>
            </div>
          </div>
        </div>

        {/* MFA & Cryptography Card */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-4">
          <h2 className="text-sm font-semibold text-slate-900 flex items-center space-x-2">
            <Smartphone className="w-4 h-4 text-indigo-600" />
            <span>Multi-Factor Authentication (MFA)</span>
          </h2>
          <p className="text-xs text-slate-500">
            Time-based One-Time Password (TOTP, RFC 6238) provides cryptographic second-factor defense against credential stuffing.
          </p>
          <div className="pt-2">
            <Link
              to="/mfa-setup"
              className="inline-flex items-center space-x-2 px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-medium transition shadow-sm"
            >
              <Key className="w-3.5 h-3.5" />
              <span>Configure Authenticator App</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
