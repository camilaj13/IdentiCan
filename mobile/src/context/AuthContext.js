import React, { createContext, useState, useEffect, useContext } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import client from '../api/client';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const storedToken = await AsyncStorage.getItem('token');
      if (storedToken) {
        setToken(storedToken);
        const response = await client.get('/api/auth/me', {
          headers: { Authorization: `Bearer ${storedToken}` },
        });
        setUser(response.data);
      }
    } catch {
      await AsyncStorage.removeItem('token');
      setToken(null);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      setError(null);
      const response = await client.post('/api/auth/login', { email, password });
      const { access_token, user: userData } = response.data;
      setToken(access_token);
      setUser(userData);
      await AsyncStorage.setItem('token', access_token);
      return true;
    } catch (err) {
      const message =
        err.response?.data?.detail || 'Error al iniciar sesión';
      setError(message);
      return false;
    }
  };

  const register = async (email, password, name, phone) => {
    try {
      setError(null);
      const response = await client.post('/api/auth/register', {
        email,
        password,
        name,
        phone: phone || null,
      });
      const { access_token, user: userData } = response.data;
      setToken(access_token);
      setUser(userData);
      await AsyncStorage.setItem('token', access_token);
      return true;
    } catch (err) {
      const message =
        err.response?.data?.detail || 'Error al registrarse';
      setError(message);
      return false;
    }
  };

  const logout = async () => {
    setToken(null);
    setUser(null);
    setError(null);
    await AsyncStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider
      value={{ user, token, loading, error, login, register, logout, setError }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
