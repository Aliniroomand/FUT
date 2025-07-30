import React from 'react';
import { Navigate } from 'react-router-dom';

// مسیرهای فقط برای ادمین‌ها
export const AdminRoute = ({ children }) => {
  const isAdmin = localStorage.getItem('isAdminLoggedIn') === 'true';
  const token = localStorage.getItem('access_token');

  if (!token || !isAdmin) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

// مسیرهای فقط برای کاربران معمولی
export const UserRoute = ({ children }) => {
  const isAdmin = localStorage.getItem('isAdminLoggedIn') === 'true';
  const token = localStorage.getItem('access_token');

  // اگر لاگین نیست یا ادمینه، نذار به صفحه کاربر بره
  if (!token || isAdmin) {
    return <Navigate to="/login" replace />;
  }

  return children;
};
