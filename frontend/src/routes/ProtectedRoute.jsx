import React from 'react';
import { Navigate } from 'react-router-dom';

// ساده: استفاده از localStorage برای ذخیره وضعیت ورود
const isAuthenticated = () => {
  return localStorage.getItem('isAdminLoggedIn') === 'true';
};

const ProtectedRoute = ({ children }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

export default ProtectedRoute;