import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, Key, CheckCircle2, AlertCircle, ArrowRight } from 'lucide-react';
import { api } from '../../api/client';
import { useAuth } from '../../context/AuthContext';

export const MfaSetupPage: React.FC = () => {
  const { user, refreshUser } = useAuth();
  const navigate = useNavigate();

  const [setupData, setSetupData] = useState<{ secret: string; qr_code_data_url: string } | null>(null);
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const initMfa = async () => {
      try {
        const data = await api.setupMfa();
        setSetupData(data);
      } catch (err: any) {
        setError(err.message || 'Failed to initialize MFA setup.');
      }
    };
    initMfa();
  }, []);

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await api.verifyMfa(code);
      setSuccess(true);
      await refreshUser();
      setTimeout(() => navigate('/dashboard'), 2000);
    } catch (err: any) {
      setError(err.message || 'Invalid MFA code. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto my-6">
      <div className="bg-[#111827]/90 border border-slate-800 rounded-2xl p-8 backdrop-blur shadow-2xl space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center mx-auto text-emerald-400">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold text-white font-mono">Setup Two-Factor MFA</h2>
          <p className="text-xs text-slate-400 font-mono">
            Enhance account security with Time-Based One-Time Passwords (TOTP)
          </p>
        </div>

        {error && (
          <div className="p-3.5 rounded-lg bg-rose-500/15 border border-rose-500/30 flex items-center gap-2.5 text-rose-300 text-xs font-mono">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
            <span>{error}</span>
          </div>
        )}

        {success ? (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-center space-y-2">
            <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
            <h4 className="text-sm font-bold text-emerald-300 font-mono">MFA Successfully Activated!</h4>
            <p className="text-xs text-slate-400 font-mono">Redirecting to your dashboard...</p>
          </div>
        ) : (
          setupData && (
            <div className="space-y-6">
              <div className="bg-white p-4 rounded-xl flex justify-center w-fit mx-auto shadow-lg">
                <img
                  src={setupData.qr_code_data_url}
                  alt="MFA QR Code"
                  className="w-48 h-48 object-contain"
                />
              </div>

              <div className="bg-black/40 border border-slate-800 rounded-lg p-3 text-center">
                <span className="text-[10px] text-slate-500 font-mono uppercase block">Manual Secret Key</span>
                <code className="text-xs font-mono font-bold text-cyan-400 tracking-wider">
                  {setupData.secret}
                </code>
              </div>

              <form onSubmit={handleVerify} className="space-y-4 font-mono text-xs">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">
                    Enter 6-Digit Code from Authenticator
                  </label>
                  <input
                    type="text"
                    required
                    maxLength={6}
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    placeholder="123456"
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2.5 text-center text-xl tracking-widest text-cyan-400 font-bold focus:outline-none focus:border-cyan-500"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading || code.length !== 6}
                  className="w-full py-2.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-black font-bold text-xs transition shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2"
                >
                  {loading ? 'Verifying...' : 'Confirm & Enable MFA'}
                  <ArrowRight className="w-4 h-4" />
                </button>
              </form>
            </div>
          )
        )}
      </div>
    </div>
  );
};
