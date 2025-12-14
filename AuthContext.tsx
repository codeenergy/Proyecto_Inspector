import React, { createContext, useContext, useState, ReactNode } from 'react';
import { flushSync } from 'react-dom';

interface AuthContextType {
    isAuthenticated: boolean;
    login: (username: string, password: string) => boolean;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const VALID_USERNAME = 'codeenergy';
const VALID_PASSWORD = 'Codeenergy77##';
const AUTH_KEY = 'trafficbot_auth';

export function AuthProvider({ children }: { children: ReactNode }) {
    // Check localStorage immediately on initialization to prevent flash
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() => {
        const authStatus = localStorage.getItem(AUTH_KEY);
        return authStatus === 'true';
    });

    const login = (username: string, password: string): boolean => {
        if (username === VALID_USERNAME && password === VALID_PASSWORD) {
            // Set localStorage FIRST to ensure it's ready before state update
            localStorage.setItem(AUTH_KEY, 'true');

            // Use flushSync to ensure state update happens synchronously
            // This prevents React 19's batching from delaying the authentication state update
            flushSync(() => {
                setIsAuthenticated(true);
            });

            // Force a microtask to ensure localStorage is flushed
            Promise.resolve().then(() => {
                // Verify auth state is set correctly
                const authStatus = localStorage.getItem(AUTH_KEY);
                if (authStatus !== 'true') {
                    console.error('Auth state mismatch after login');
                }
            });

            return true;
        }
        return false;
    };

    const logout = () => {
        setIsAuthenticated(false);
        localStorage.removeItem(AUTH_KEY);
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
