import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';
import { api } from '../api/client';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAdmin: boolean;
  isAuthenticated: boolean;
  login: (credentials: any) => Promise<any>;
  register: (data: any) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  loginAsDemo: (type: 'admin' | 'alice') => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(() => {
    const cached = localStorage.getItem('secureshare_user');
    return cached ? JSON.parse(cached) : null;
  });
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('secureshare_token'));
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const refreshUser = async () => {
    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }
    try {
      const me = await api.getMe();
      setUser(me);
      localStorage.setItem('secureshare_user', JSON.stringify(me));
    } catch {
      logout();
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshUser();

    const handleLogoutEvent = () => {
      setUser(null);
      setToken(null);
      localStorage.removeItem('secureshare_token');
      localStorage.removeItem('secureshare_user');
    };
    window.addEventListener('auth-logout', handleLogoutEvent);
    return () => window.removeEventListener('auth-logout', handleLogoutEvent);
  }, [token]);

  const login = async (credentials: any) => {
    const result = await api.login(credentials);
    if (result.mfa_required) {
      return result;
    }
    setToken(result.access_token);
    localStorage.setItem('secureshare_token', result.access_token);
    const me = await api.getMe();
    setUser(me);
    localStorage.setItem('secureshare_user', JSON.stringify(me));
    return result;
  };

  const register = async (data: any) => {
    await api.register(data);
    await login({ email: data.email, password: data.password });
  };

  const logout = async () => {
    try {
      if (token) {
        await api.logout();
      }
    } catch {
      // Ignore network errors on logout
    } finally {
      setToken(null);
      setUser(null);
      localStorage.removeItem('secureshare_token');
      localStorage.removeItem('secureshare_user');
    }
  };

  const loginAsDemo = async (type: 'admin' | 'alice') => {
    if (type === 'admin') {
      await login({ email: 'admin@secureshare.io', password: 'Admin@SecureShare2026!' });
    } else {
      await login({ email: 'alice@example.com', password: 'User@SecureShare2026!' });
    }
  };

  const isAdmin = user?.role === 'ADMIN';
  const isAuthenticated = !!token && !!user;

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        isAdmin,
        isAuthenticated,
        login,
        register,
        logout,
        refreshUser,
        loginAsDemo,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
