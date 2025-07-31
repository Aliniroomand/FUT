import React, { useState } from "react";
import { resetPassword } from "@/services/reset";
import { toast } from "react-hot-toast";

const ResetPassword = () => {
  const [newPassword, setNewPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const token = localStorage.getItem("reset_token");
      if (!token) {
        toast.error("توکن بازیابی یافت نشد!");
        return;
      }
      await resetPassword({ token, new_password: newPassword });
      toast.success("رمز عبور با موفقیت تغییر یافت!");
    } catch (err) {
      toast.error(err.response?.data?.detail || "خطا در تغییر رمز عبور");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <form onSubmit={handleSubmit} className="glass-dark w-full max-w-sm p-8 rounded">
        <h2 className="text-2xl font-bold text-center text-[var(--color-gold)] mb-6">تغییر رمز عبور</h2>
        <label className="block mb-4">
          <span className="text-[var(--color-text-primary)]">رمز عبور جدید</span>
          <input
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            className="mt-1 w-full px-4 py-2 rounded-lg bg-[var(--color-dark-1)] text-[var(--color-text-primary)] border border-[var(--color-gold-shadow)] focus:outline-none focus:ring focus:border-[var(--color-gold)]"
            required
          />
        </label>
        <button
          type="submit"
          className="bg-amber-500 hover:bg-amber-600 text-white font-bold py-2 rounded w-full"
          disabled={loading}
        >
          {loading ? "در حال ارسال..." : "تغییر رمز عبور"}
        </button>
      </form>
    </div>
  );
};

export default ResetPassword;
