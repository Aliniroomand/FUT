import React from "react";
import { useNavigate } from "react-router-dom";
import mbape from "@/assets/pageNotFound.webp";
const NotFoundPage = () => {
  const navigate = useNavigate();

  return (
    <div className="flex items-center justify-center h-screen bg-white/20 backdrop-blur-xs text-[var(--color-text-primary)]">
      <div className="text-center z-50">
        <h1 className="text-6xl font-bold">404</h1>
        <p className="mt-4 text-xl text-[var(--color-text-secondary)]">
          این صفحه‌رو پیدا نکردم
        </p>

        <div className="mt-6 flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate("/")}
            className="px-6 py-2 rounded-md font-semibold bg-[var(--color-gold)] text-[var(--color-dark)] hover:bg-[var(--color-gold-light)] transition-all duration-200"
          >
            بازگشت به صفحه اصلی
          </button>

          <button
            onClick={() => navigate(-1)}
            className="px-6 py-2 rounded-md font-semibold border border-[var(--color-gold)] text-[var(--color-gold)] bg-transparent hover:bg-[var(--color-dark)] hover:text-[var(--color-gold-light)] transition-all duration-200"
          >
            بازگشت به صفحه قبلی
          </button>
        </div>
      </div>
      <div>
        <img
          src={mbape}
          alt="mbape"
          className="absolute h-auto w-auto bottom-0 left-2"
        />
      </div>
    </div>
  );
};

export default NotFoundPage;
