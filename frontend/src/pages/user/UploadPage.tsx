import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  UploadCloud,
  FileText,
  AlertTriangle,
  ShieldAlert,
  ShieldCheck,
  CheckCircle2,
  Lock,
  Binary,
  RefreshCw,
  Bug,
} from 'lucide-react';
import { api } from '../../api/client';
import { FileItem } from '../../types';
import { SecurityPipelineVisualizer } from '../../components/upload/SecurityPipelineVisualizer';

export const UploadPage: React.FC = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadedResult, setUploadedResult] = useState<FileItem | null>(null);
  const [scanHistory, setScanHistory] = useState<any[]>([]);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (file: File) => {
    setError(null);
    setUploadedResult(null);
    if (file.size > 50 * 1024 * 1024) {
      setError('File size exceeds maximum allowed limit of 50 MB.');
      return;
    }
    setSelectedFile(file);
  };

  const executeUpload = async (fileToUpload: File) => {
    setError(null);
    setUploading(true);
    setUploadedResult(null);

    const formData = new FormData();
    formData.append('file', fileToUpload);

    try {
      const res = await api.uploadFile(formData);
      setUploadedResult(res.file);
      // Fetch scan history
      const details = await api.getFileDetails(res.file.id);
      setScanHistory(details.scan_results);
    } catch (err: any) {
      setError(err.message || 'File upload failed validation.');
    } finally {
      setUploading(false);
    }
  };

  const handleEicarTest = async () => {
    setError(null);
    setUploading(true);
    setSelectedFile(null);
    setUploadedResult(null);

    try {
      const res = await api.uploadEicarTest();
      setUploadedResult(res.file);
      const details = await api.getFileDetails(res.file.id);
      setScanHistory(details.scan_results);
    } catch (err: any) {
      setError(err.message || 'EICAR test upload failed.');
    } finally {
      setUploading(false);
    }
  };

  const handleUploadCleanSample = () => {
    const sampleBlob = new Blob(
      ['%PDF-1.4\n1 0 obj\n<< /Title (Zero-Trust Security Verification Sample) >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF'],
      { type: 'application/pdf' }
    );
    const sampleFile = new File([sampleBlob], 'ZeroTrust_Security_Sample.pdf', { type: 'application/pdf' });
    setSelectedFile(sampleFile);
    executeUpload(sampleFile);
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-[10px] font-mono font-bold tracking-widest text-cyan-400 uppercase">
            Security Gate
          </span>
          <h1 className="text-2xl font-bold text-white font-mono mt-1">Upload & Automated Validation</h1>
          <p className="text-xs text-slate-400 font-mono mt-1">
            Zero-Trust pipeline: files are checked for spoofed MIME, scripts, macros, and malware before encryption.
          </p>
        </div>

        {/* Quick Demo Test Buttons */}
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleUploadCleanSample}
            disabled={uploading}
            className="px-3 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-mono font-semibold transition flex items-center gap-1.5"
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            Upload Clean Sample
          </button>
          <button
            type="button"
            onClick={handleEicarTest}
            disabled={uploading}
            className="px-3 py-1.5 rounded-lg bg-rose-500/15 hover:bg-rose-500/25 text-rose-300 border border-rose-500/40 text-xs font-mono font-bold transition flex items-center gap-1.5 shadow-sm shadow-rose-900/20"
          >
            <Bug className="w-3.5 h-3.5" />
            Test EICAR Malware
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/15 border border-rose-500/30 flex items-center gap-3 text-rose-300 text-xs font-mono">
          <AlertTriangle className="w-5 h-5 shrink-0 text-rose-400" />
          <span>{error}</span>
        </div>
      )}

      {/* Drag & Drop Area */}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition duration-200 ${
          dragActive
            ? 'border-cyan-400 bg-cyan-950/20 shadow-xl shadow-cyan-900/20'
            : 'border-slate-700/80 bg-[#111827]/60 hover:border-slate-600 hover:bg-[#111827]'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          onChange={(e) => e.target.files && e.target.files[0] && handleFileSelect(e.target.files[0])}
        />
        <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center mx-auto text-cyan-400 mb-4">
          <UploadCloud className="w-8 h-8" />
        </div>
        <h3 className="text-base font-bold text-white font-mono">
          {selectedFile ? selectedFile.name : 'Choose a file or drag & drop here'}
        </h3>
        <p className="text-xs text-slate-400 font-mono mt-1">
          Max file size: <span className="text-slate-200 font-bold">50 MB</span> • Multi-stage inspection enforced
        </p>

        {selectedFile && !uploading && !uploadedResult && (
          <div className="mt-4 flex items-center justify-center gap-3">
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                executeUpload(selectedFile);
              }}
              className="px-5 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-black font-mono font-bold text-xs shadow-lg shadow-cyan-500/20 transition"
            >
              Start Security Validation Pipeline
            </button>
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                setSelectedFile(null);
              }}
              className="px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono text-xs transition"
            >
              Clear
            </button>
          </div>
        )}
      </div>

      {/* Real-time Pipeline Visualizer */}
      <SecurityPipelineVisualizer
        file={uploadedResult}
        scans={scanHistory}
        isUploading={uploading}
      />

      {/* Outcome Details Card */}
      {uploadedResult && (
        <div
          className={`border rounded-2xl p-6 backdrop-blur ${
            uploadedResult.is_quarantined
              ? 'bg-rose-950/20 border-rose-500/40'
              : 'bg-emerald-950/20 border-emerald-500/40'
          }`}
        >
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div
                className={`p-3 rounded-xl border ${
                  uploadedResult.is_quarantined
                    ? 'bg-rose-500/10 border-rose-500/30 text-rose-400'
                    : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                }`}
              >
                {uploadedResult.is_quarantined ? (
                  <ShieldAlert className="w-6 h-6" />
                ) : (
                  <ShieldCheck className="w-6 h-6" />
                )}
              </div>
              <div>
                <h4 className="text-base font-bold font-mono text-white">
                  {uploadedResult.is_quarantined
                    ? 'Security Threat Intercepted & Quarantined'
                    : 'Validation Passed: File Encrypted & Available'}
                </h4>
                <p className="text-xs font-mono text-slate-400 mt-0.5">
                  {uploadedResult.is_quarantined
                    ? uploadedResult.quarantine_reason
                    : 'AES-256-GCM authenticated encryption complete. File ready for secure storage and sharing.'}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 font-mono text-xs">
              <button
                onClick={() => navigate('/files')}
                className="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-white transition"
              >
                View in Files
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
