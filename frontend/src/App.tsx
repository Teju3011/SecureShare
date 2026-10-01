import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { AppShell } from './components/layout/AppShell';

// Public pages
import { LandingPage } from './pages/public/LandingPage';
import { LoginPage } from './pages/public/LoginPage';
import { RegisterPage } from './pages/public/RegisterPage';
import { MfaSetupPage } from './pages/public/MfaSetupPage';
import { SharedAccessPage } from './pages/public/SharedAccessPage';
import { DemoPage } from './pages/public/DemoPage';

// User pages
import { UserDashboard } from './pages/user/UserDashboard';
import { UploadPage } from './pages/user/UploadPage';
import { MyFilesPage } from './pages/user/MyFilesPage';
import { FileDetailsPage } from './pages/user/FileDetailsPage';
import { SharePage } from './pages/user/SharePage';
import { ActivityPage } from './pages/user/ActivityPage';
import { PermissionsPage } from './pages/user/PermissionsPage';
import { SettingsPage } from './pages/user/SettingsPage';

// Admin pages
import { AdminDashboard } from './pages/admin/AdminDashboard';
import { UserManagementPage } from './pages/admin/UserManagementPage';
import { QuarantinePage } from './pages/admin/QuarantinePage';
import { AuditLogsPage } from './pages/admin/AuditLogsPage';
import { CicdSecurityPage } from './pages/admin/CicdSecurityPage';
import { SecurityFindingsPage } from './pages/admin/SecurityFindingsPage';

// Route Guards
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  if (isLoading) {
    return <div className="p-8 text-center text-slate-500 font-mono text-xs">Authenticating session...</div>;
  }
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
};

const AdminRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isAdmin, isLoading } = useAuth();
  if (isLoading) {
    return <div className="p-8 text-center text-slate-500 font-mono text-xs">Verifying authorization...</div>;
  }
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (!isAdmin) return <Navigate to="/dashboard" replace />;
  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<AppShell />}>
            {/* Public */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/demo" element={<DemoPage />} />
            <Route path="/mfa-setup" element={<ProtectedRoute><MfaSetupPage /></ProtectedRoute>} />
            <Route path="/share/:token" element={<SharedAccessPage />} />

            {/* Standard User */}
            <Route path="/dashboard" element={<ProtectedRoute><UserDashboard /></ProtectedRoute>} />
            <Route path="/upload" element={<ProtectedRoute><UploadPage /></ProtectedRoute>} />
            <Route path="/files" element={<ProtectedRoute><MyFilesPage /></ProtectedRoute>} />
            <Route path="/files/:id" element={<ProtectedRoute><FileDetailsPage /></ProtectedRoute>} />
            <Route path="/permissions/:fileId" element={<ProtectedRoute><PermissionsPage /></ProtectedRoute>} />
            <Route path="/shares" element={<ProtectedRoute><SharePage /></ProtectedRoute>} />
            <Route path="/activity" element={<ProtectedRoute><ActivityPage /></ProtectedRoute>} />
            <Route path="/settings" element={<ProtectedRoute><SettingsPage /></ProtectedRoute>} />

            {/* User Route Aliases */}
            <Route path="/shared" element={<Navigate to="/shares" replace />} />
            <Route path="/security-activity" element={<Navigate to="/activity" replace />} />

            {/* Admin SOC */}
            <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />
            <Route path="/admin/dashboard" element={<AdminRoute><AdminDashboard /></AdminRoute>} />
            <Route path="/admin/users" element={<AdminRoute><UserManagementPage /></AdminRoute>} />
            <Route path="/admin/quarantine" element={<AdminRoute><QuarantinePage /></AdminRoute>} />
            <Route path="/admin/audit-logs" element={<AdminRoute><AuditLogsPage /></AdminRoute>} />
            <Route path="/audit-logs" element={<Navigate to="/admin/audit-logs" replace />} />
            <Route path="/admin/cicd" element={<AdminRoute><CicdSecurityPage /></AdminRoute>} />
            <Route path="/admin/findings" element={<AdminRoute><SecurityFindingsPage /></AdminRoute>} />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};
