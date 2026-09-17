import React from 'react';
import {
  CheckCircle2,
  AlertOctagon,
  Shield,
  FileCheck,
  Binary,
  Lock,
  Loader2,
} from 'lucide-react';
import { FileItem, ScanResultItem } from '../../types';

interface PipelineVisualizerProps {
  file?: FileItem | null;
  scans?: ScanResultItem[];
  isUploading?: boolean;
}

export const SecurityPipelineVisualizer: React.FC<PipelineVisualizerProps> = ({
  file,
  scans = [],
  isUploading = false,
}) => {
  const mimeScan = scans.find((s) => s.scanner_name === 'mime_signature_validator');
  const dangerScan = scans.find((s) => s.scanner_name === 'dangerous_file_detector');
  const clamavScan = scans.find((s) => s.scanner_name === 'clamav_scanner');

  const steps = [
    {
      id: 'size_hash',
      title: '1. Size & SHA-256 Hash',
      description: file ? `SHA-256: ${file.sha256_hash.substring(0, 16)}...` : 'Validating < 50MB and calculating hash',
      icon: <Binary className="w-4 h-4" />,
      status: file ? 'passed' : isUploading ? 'active' : 'pending',
    },
    {
      id: 'mime_sig',
      title: '2. MIME & Magic Bytes',
      description: mimeScan?.details || (file ? `Header: ${file.magic_bytes_preview || 'Verified'}` : 'Checking declared MIME vs file magic signature'),
      icon: <FileCheck className="w-4 h-4" />,
      status: mimeScan?.scan_status === 'PASSED' ? 'passed' : mimeScan?.scan_status === 'FAILED' ? 'failed' : isUploading ? 'active' : 'pending',
    },
    {
      id: 'dangerous',
      title: '3. Dangerous Content',
      description: dangerScan?.details || 'Deep inspection for PE/ELF binaries, shell scripts, and macros',
      icon: <AlertOctagon className="w-4 h-4" />,
      status: dangerScan?.scan_status === 'PASSED' ? 'passed' : dangerScan?.scan_status === 'HIGH_RISK' ? 'failed' : isUploading ? 'active' : 'pending',
    },
    {
      id: 'clamav',
      title: '4. Antivirus & Malware',
      description: clamavScan?.details || (file?.is_quarantined ? file.quarantine_reason : 'ClamAV daemon scan & EICAR test signature validation'),
      icon: <Shield className="w-4 h-4" />,
      status: clamavScan?.scan_status === 'PASSED' ? 'passed' : clamavScan?.scan_status === 'MALICIOUS' ? 'failed' : isUploading ? 'active' : 'pending',
    },
    {
      id: 'decision',
      title: '5. Security Verdict',
      description: file ? (file.is_quarantined ? `QUARANTINED: ${file.quarantine_reason || 'Threat isolated'}` : 'VERIFIED CLEAN: Approved for storage & sharing') : 'Evaluating scanner findings',
      icon: <Shield className="w-4 h-4" />,
      status: file ? (file.is_quarantined ? 'failed' : 'passed') : isUploading ? 'active' : 'pending',
    },
    {
      id: 'encryption',
      title: '6. AES-256-GCM Encryption',
      description: file ? 'Encrypted with 256-bit key at rest before writing to storage' : 'Authenticated envelope encryption',
      icon: <Lock className="w-4 h-4" />,
      status: file ? 'passed' : 'pending',
    },
  ];

  return (
    <div className="bg-[#0f172a]/90 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="flex items-center justify-between mb-5 border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-sm font-bold font-mono tracking-wider text-cyan-400 uppercase flex items-center gap-2">
            <Shield className="w-4 h-4 text-cyan-400" />
            Automated Zero-Trust Security Pipeline
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Every uploaded file undergoes multi-stage cryptographic and signature inspection
          </p>
        </div>
        {file && (
          <div className="text-right">
            <span className="text-xs font-mono text-slate-400 block">Overall Status</span>
            <span
              className={`text-xs font-bold px-2.5 py-1 rounded font-mono ${
                file.is_quarantined
                  ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                  : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
              }`}
            >
              {file.status}
            </span>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {steps.map((step) => {
          let badgeColor = 'border-slate-800 bg-slate-900/50 text-slate-500';
          let statusIcon = null;

          if (step.status === 'passed') {
            badgeColor = 'border-emerald-500/30 bg-emerald-950/20 text-emerald-300';
            statusIcon = <CheckCircle2 className="w-4 h-4 text-emerald-400" />;
          } else if (step.status === 'failed') {
            badgeColor = 'border-rose-500/40 bg-rose-950/25 text-rose-300';
            statusIcon = <AlertOctagon className="w-4 h-4 text-rose-400" />;
          } else if (step.status === 'active') {
            badgeColor = 'border-cyan-500/40 bg-cyan-950/30 text-cyan-300 animate-pulse';
            statusIcon = <Loader2 className="w-4 h-4 text-cyan-400 animate-spin" />;
          }

          return (
            <div
              key={step.id}
              className={`p-3.5 rounded-lg border transition duration-150 flex flex-col justify-between ${badgeColor}`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <div className="p-1.5 rounded bg-black/40 text-slate-300">{step.icon}</div>
                  <span className="text-xs font-semibold font-mono tracking-wide">{step.title}</span>
                </div>
                {statusIcon}
              </div>
              <p className="text-[11px] text-slate-400 mt-2 font-mono break-words leading-relaxed">
                {step.description}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
