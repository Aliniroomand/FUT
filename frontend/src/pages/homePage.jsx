import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6">
      <h1 className="text-4xl font-bold mb-4">به وب‌اپلیکیشن ما خوش آمدید</h1>
      <p className="text-lg mb-6 text-center max-w-md">
        اینجا می‌توانید اطلاعات و گزارش‌های مختلف را مشاهده کنید و برای مدیریت به بخش ادمین وارد شوید.
      </p>
      <div className="space-x-4">
        <Link
          to="/"
          className="px-5 py-3 bg-amber-500 text-white rounded-lg hover:bg-amber-600"
        >
          مشاهده بخش عمومی
        </Link>
        <Link
          to="/login"
          className="px-5 py-3 border border-amber-500 text-amber-500 rounded-lg hover:bg-amber-50"
        >
          ورود ادمین
        </Link>
      </div>
    </div>
  );
};

export default HomePage;