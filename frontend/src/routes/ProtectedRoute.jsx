import React from 'react';
import { Navigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

function getIsAdmin() {
  const token = localStorage.getItem('access_token');
  if (!token) return false;
  try {
    const decoded = jwtDecode(token);
    return !!decoded.is_admin;
  } catch {
    return false;
  }
}

// مسیرهای فقط برای ادمین‌ها
export const AdminRoute = ({ children }) => {
  const token = localStorage.getItem('access_token');
  const isAdmin = getIsAdmin();
  if (!token || !isAdmin) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

// مسیرهای فقط برای کاربران معمولی
export const UserRoute = ({ children }) => {
  const token = localStorage.getItem('access_token');
  const isAdmin = getIsAdmin();
  if (!token || isAdmin) {
    return <Navigate to="/login" replace />;
  }
  return children;
};
