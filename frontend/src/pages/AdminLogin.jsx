import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

const AdminLogin = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // TODO: Call your auth API here
      if (email === 'ali@gmail.com' && password === '1234') {
        localStorage.setItem('isAdminLoggedIn', 'true');
        toast.success('ورود موفق');
        navigate('/admin');
      } else {
        throw new Error('اطلاعات نامعتبر');
      }
    } catch (err) {
      toast.error(err.message);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen ">
      <form onSubmit={handleSubmit} className=" p-8 rounded-lg shadow-lg w-full max-w-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">ورود ادمین</h2>
        <label className="block mb-4">
          <span className="text-gray-700">ایمیل</span>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-amber-500"
            required
          />
        </label>
        <label className="block mb-6">
          <span className="text-gray-700">رمز عبور</span>
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
          className="w-full bg-amber-500 text-dark-hard py-2 rounded-lg font-semibold hover:bg-amber-600"
        >
          ورود
        </button>
      </form>
    </div>
  );
};

export default AdminLogin;
