import React, { useState, useEffect } from "react";
import { toast } from "react-hot-toast";
import { register } from "@/services/auth";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { login } from "../../services/auth";

const Register = () => {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [errors, setErrors] = useState({});

  const validate = () => {
    const errs = {};

    if (!/^09\d{9}$/.test(phoneNumber)) {
      errs.phoneNumber = "شماره موبایل باید با 09 شروع شده و 11 رقم باشد";
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errs.email = "ایمیل معتبر وارد کنید";
    }

    if (password.length < 6) {
      errs.password = "رمز عبور باید حداقل ۶ کاراکتر باشد";
    }
    if (!confirmPassword) {
      errs.confirmPassword = "تأیید رمز عبور الزامی است";
    } else if (confirmPassword !== password) {
      errs.confirmPassword = "رمز عبور و تکرار آن یکسان نیستند";
    }

    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
        const decoded = jwtDecode(token);
        if (decoded.is_admin) {
          navigate("/admin/dashboard");
        } else {
          navigate("/profile");
        }
      } catch {}
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    try {
      const response = await register({
        phone_number: phoneNumber,
        email,
        password,
      });
      if (response && response.access_token) {
        console.log(response);
        localStorage.setItem("access_token", response.access_token);
        if (response.is_admin) {
          navigate("/admin/dashboard");
        } else {
          navigate("/profile");
        }
        toast.success("ثبت‌نام و ورود با موفقیت انجام شد");
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || "خطا در ثبت‌نام");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <form
        onSubmit={handleSubmit}
        className="glass-dark w-full max-w-sm p-8 rounded"
      >
        <h2 className="text-2xl font-bold text-center text-[var(--color-gold)] mb-6">
          فرم ثبت‌نام
        </h2>

        <label className="block mb-2">
          <span className="text-[var(--color-text-primary)]">شماره موبایل</span>
          <input
            type="tel"
            value={phoneNumber}
            placeholder="09...."
            onChange={(e) => setPhoneNumber(e.target.value)}
            className={`mt-1 w-full px-4 py-2 rounded-lg bg-[var(--color-dark-1)] text-[var(--color-text-primary)] border ${
              errors.phoneNumber
                ? "border-red-500"
                : "border-[var(--color-gold-shadow)]"
            } focus:outline-none focus:ring focus:border-[var(--color-gold)]`}
          />
          {errors.phoneNumber && (
            <p className="text-red-500 text-xs mt-1">{errors.phoneNumber}</p>
          )}
        </label>

        <label className="block mb-2">
          <span className="text-[var(--color-text-primary)]">ایمیل</span>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={`mt-1 w-full px-4 py-2 rounded-lg bg-[var(--color-dark-1)] text-[var(--color-text-primary)] border ${
              errors.email
                ? "border-red-500"
                : "border-[var(--color-gold-shadow)]"
            } focus:outline-none focus:ring focus:border-[var(--color-gold)]`}
          />
          {errors.email && (
            <p className="text-red-500 text-xs mt-1">{errors.email}</p>
          )}
        </label>

        <label className="block mb-4">
          <span className="text-[var(--color-text-primary)]">رمز عبور</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={`mt-1 w-full px-4 py-2 rounded-lg bg-[var(--color-dark-1)] text-[var(--color-text-primary)] border ${
              errors.password
                ? "border-red-500"
                : "border-[var(--color-gold-shadow)]"
            } focus:outline-none focus:ring focus:border-[var(--color-gold)]`}
          />
          {errors.password && (
            <p className="text-red-500 text-xs mt-1">{errors.password}</p>
          )}
        </label>
        <label className="block mb-4">
          <span className="text-[var(--color-text-primary)]">
            تأیید رمز عبور
          </span>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className={`mt-1 w-full px-4 py-2 rounded-lg bg-[var(--color-dark-1)] text-[var(--color-text-primary)] border ${
              errors.confirmPassword
                ? "border-red-500"
                : "border-[var(--color-gold-shadow)]"
            } focus:outline-none focus:ring focus:border-[var(--color-gold)]`}
          />
          {errors.confirmPassword && (
            <p className="text-red-500 text-xs mt-1">
              {errors.confirmPassword}
            </p>
          )}
        </label>

        <button
          type="submit"
          className="w-full py-2 bg-[var(--color-gold)] hover:bg-[var(--color-gold-accent)] text-[var(--color-dark)] font-semibold rounded-lg shadow-md transition"
        >
          ثبت‌نام
        </button>

        <p className="mt-4 text-center text-sm text-[var(--color-text-secondary)]">
          قبلاً حساب ساختید؟{" "}
          <a href="/login" className="text-[var(--color-gold)] hover:underline">
            وارد شوید
          </a>
        </p>
      </form>
    </div>
  );
};

export default Register;
