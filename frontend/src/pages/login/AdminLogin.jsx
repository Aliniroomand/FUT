import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { login, getProfile } from '@/services/api';

const AdminLogin = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await login({ email, password });
    if (response && response.access_token) {
      localStorage.setItem('access_token', response.access_token);

      // بعد از لاگین، نقش کاربر را دریافت می‌کنیم
      const profile = await getProfile();
      if (profile.role === 'admin') {
        localStorage.setItem('isAdminLoggedIn', 'true');
        navigate('/admin/dashboard');
      } else {
        localStorage.setItem('isAdminLoggedIn', 'false');
        navigate('/profile');  // صفحه پروفایل کاربر معمولی (بعدا ساخته می‌شود)
      }
    }
  } catch (err) {
    toast.error('خطا در ورود');
    console.error('Login failed:', err);
  }
};

  return (
    <div className="flex items-center justify-center h-screen">
      <form onSubmit={handleSubmit} className="p-8 glass-dark rounded-lg shadow-lg w-full max-w-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">ورود ادمین</h2>
        <label className="block mb-4">
          <span className="">ایمیل</span>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-amber-500"
            required
          />
        </label>
        <label className="block mb-6">
          <span >رمز عبور</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-amber-500"
            required
          />
        </label>
        <button
          type="submit"
          className="w-full bg-gold text-dark-hard cursor-pointer transition text-black py-2 rounded-lg font-semibold hover:bg-amber-600"
        >
          ورود
        </button>
      </form>
    </div>
  );
};

export default AdminLogin;
