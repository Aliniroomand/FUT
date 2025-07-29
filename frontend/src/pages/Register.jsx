import React, { useState } from 'react';
import { toast } from 'react-hot-toast';
import { registerPhone } from '../services/api'; // برای ارسال شماره تلفن

const RegisterPhone = () => {
  const [phoneNumber, setPhoneNumber] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await registerPhone({ phone_number: phoneNumber });
      toast.success('شماره تلفن ثبت شد');
    } catch (err) {
      toast.error('خطا در ثبت شماره تلفن');
    }
  };

  return (
    <div className="flex items-center justify-center h-screen">
      <form onSubmit={handleSubmit} className="p-8 rounded-lg shadow-lg w-full max-w-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">ثبت‌نام</h2>
        <label className="block mb-4">
          <span className="text-gray-700">شماره تلفن</span>
          <input
            type="tel"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:border-amber-500"
            required
          />
        </label>
        <button
          type="submit"
          className="w-full bg-amber-500 text-dark-hard py-2 rounded-lg font-semibold hover:bg-amber-600"
        >
          ادامه
        </button>
      </form>
    </div>
  );
};

export default RegisterPhone;
