// src/pages/login/Register.jsx
import React, { useState } from 'react';
import { toast } from 'react-hot-toast';
import { register } from '@/services/api';  // استفاده از متد register

const Register = () => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [email, setEmail]           = useState('');
  const [password, setPassword]     = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await register({ phone_number: phoneNumber, email, password });
      toast.success('ثبت‌نام با موفقیت انجام شد');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'خطا در ثبت‌نام');
    }
  };

  return (
    <div className="flex items-center justify-center h-screen">
      <form onSubmit={handleSubmit} className="p-8 glass-dark rounded-lg shadow-lg w-full max-w-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">ثبت‌نام</h2>

        <label className="block mb-4">
          <span className="">شماره تلفن</span>
          <input
            type="tel"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-amber-500"
            required
          />
        </label>

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
          <span className="">رمز عبور</span>
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
          className="w-full bg-gold text-dark-hard cursor-pointer transition text-black py-2 rounded-lg font-semibold hover:bg-gold-accent"
        >
          ثبت‌نام
        </button>
      </form>
    </div>
  );
};

export default Register;
