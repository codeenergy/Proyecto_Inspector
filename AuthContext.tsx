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
            // Set localStorage FIRST
            localStorage.setItem(AUTH_KEY, 'true');

            // Use flushSync to ensure state update happens synchronously
            flushSync(() => {
                setIsAuthenticated(true);
            });

            // Force a page reload to ensure clean state (fixes React 19 routing issues)
            setTimeout(() => {
                window.location.href = window.location.origin;
            }, 100);

            return true;
        }
        return false;
    };

    const logout = () => {
        localStorage.removeItem(AUTH_KEY);
        setIsAuthenticated(false);
        // Force reload to ensure clean logout
        window.location.href = window.location.origin;
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
