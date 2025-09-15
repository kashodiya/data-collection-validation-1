



























import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

// Create context
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Set up axios defaults
  axios.defaults.baseURL = 'http://localhost:51922/api/v1';
  
  // Set up axios interceptor for token
  useEffect(() => {
    const interceptor = axios.interceptors.request.use(
      config => {
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      error => {
        return Promise.reject(error);
      }
    );

    return () => {
      axios.interceptors.request.eject(interceptor);
    };
  }, [token]);

  // Check if token is valid and get user profile
  useEffect(() => {
    const verifyToken = async () => {
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        // Check if token is expired
        const decodedToken = jwtDecode(token);
        const currentTime = Date.now() / 1000;
        
        if (decodedToken.exp < currentTime) {
          // Token is expired
          logout();
          setLoading(false);
          return;
        }

        // Get user profile
        const response = await axios.get('/auth/profile');
        setCurrentUser(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error verifying token:', error);
        logout();
        setLoading(false);
      }
    };

    verifyToken();
  }, [token]);

  // Login function
  const login = async (username, password) => {
    try {
      setError(null);
      
      // Create form data for OAuth2 password flow
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      
      const response = await axios.post('/auth/login', formData);
      
      const { access_token } = response.data;
      
      // Save token to localStorage
      localStorage.setItem('token', access_token);
      setToken(access_token);
      
      // Get user profile
      const profileResponse = await axios.get('/auth/profile', {
        headers: {
          Authorization: `Bearer ${access_token}`
        }
      });
      
      setCurrentUser(profileResponse.data);
      
      return true;
    } catch (error) {
      console.error('Login error:', error);
      setError(error.response?.data?.detail || 'Login failed. Please check your credentials.');
      return false;
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setCurrentUser(null);
  };

  // Check if user has a specific role
  const hasRole = (role) => {
    if (!currentUser) return false;
    
    // Role hierarchy: admin > analyst > external
    const roleHierarchy = {
      'external': 1,
      'analyst': 2,
      'admin': 3
    };
    
    const userRoleLevel = roleHierarchy[currentUser.role] || 0;
    const requiredRoleLevel = roleHierarchy[role] || 999;
    
    return userRoleLevel >= requiredRoleLevel;
  };

  // Context value
  const value = {
    currentUser,
    token,
    loading,
    error,
    login,
    logout,
    hasRole
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};



























