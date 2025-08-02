import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { login, getProfile } from "@/services/auth";

import { jwtDecode } from "jwt-decode";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
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

  const validate = () => {
    const newErrors = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!email) newErrors.email = "ایمیل الزامی است";
    else if (!emailRegex.test(email)) newErrors.email = "ایمیل معتبر نیست";

    if (!password) newErrors.password = "رمز عبور الزامی است";
    else if (password.length < 6)
      newErrors.password = "رمز عبور باید حداقل ۶ کاراکتر باشد";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    try {
      const response = await login({ email, password });
      // Store both tokens if present
      if (response?.access_token) {
        localStorage.setItem("access_token", response.access_token);
      }
      if (response?.refresh_token) {
        localStorage.setItem("refresh_token", response.refresh_token);
      }
      // Always navigate after successful login
      if (response && response.access_token) {
        if (Boolean(response.is_admin)) {
          navigate("/admin/dashboard", { replace: true });
        } else {
          navigate("/profile", { replace: true });
        }
      }
    } catch (err) {
      toast.error(err.response.data.detail);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <form
        onSubmit={handleSubmit}
        className="glass-dark w-full max-w-sm p-8 rounded-xl shadow-lg border border-[var(--color-gold-shadow)]"
      >
        <h2 className="text-2xl font-bold text-center text-[var(--color-gold)] mb-6">
          ورود کاربران
        </h2>

        <label className="block mb-4">
          <span className="text-[var(--color-text-primary)]">ایمیل</span>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={`mt-1 w-full px-4 py-2 rounded-lg bg-[var(--color-dark-1)] text-[var(--color-text-primary)] border focus:outline-none focus:ring focus:border-[var(--color-gold)] ${
              errors.email
                ? "border-red-500"
                : "border-[var(--color-gold-shadow)]"
            }`}
          />
          {errors.email && (
            <p className="text-red-500 text-sm mt-1">{errors.email}</p>
          )}
        </label>

        <label className="block mb-6">
          <span className="text-[var(--color-text-primary)]">رمز عبور</span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={`mt-1 w-full px-4 py-2 rounded-lg bg-[var(--color-dark-1)] text-[var(--color-text-primary)] border focus:outline-none focus:ring focus:border-[var(--color-gold)] ${
              errors.password
                ? "border-red-500"
                : "border-[var(--color-gold-shadow)]"
            }`}
          />
          {errors.password && (
            <p className="text-red-500 text-sm mt-1">{errors.password}</p>
          )}
        </label>

        <button
          type="submit"
          className="w-full py-2 bg-[var(--color-gold)] hover:bg-[var(--color-gold-accent)] text-[var(--color-dark)] font-semibold rounded-lg shadow-md transition"
        >
          ورود
        </button>
        <p className="mt-4 text-center text-sm text-[var(--color-text-secondary)]">
          حساب ندارید؟{" "}
          <a
            href="/register"
            className="text-[var(--color-gold)] hover:underline"
          >
            ثبت‌نام کنید
          </a>
        </p>
      </form>
    </div>
  );
};

export default Login;
