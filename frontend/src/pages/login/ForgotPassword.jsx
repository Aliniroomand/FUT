import React, { useState } from "react";
import { requestReset } from "@/services/reset";
import { toast } from "react-hot-toast";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await requestReset(email);
      toast.success("لینک بازیابی رمز عبور ارسال شد!");
    } catch (err) {
      toast.error(err.response?.data?.detail || "خطا در ارسال ایمیل بازیابی");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <form onSubmit={handleSubmit} className="glass-dark w-full max-w-sm p-8 rounded">
        <h2 className="text-2xl font-bold text-center text-[var(--color-gold)] mb-6">فراموشی رمز عبور</h2>
        <label className="block mb-4">
          <span className="text-[var(--color-text-primary)]">ایمیل</span>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 w-full px-4 py-2 rounded-lg bg-[var(--color-dark-1)] text-[var(--color-text-primary)] border border-[var(--color-gold-shadow)] focus:outline-none focus:ring focus:border-[var(--color-gold)]"
            required
          />
        </label>
        <button
          type="submit"
          className="bg-amber-500 hover:bg-amber-600 text-white font-bold py-2 rounded w-full"
          disabled={loading}
        >
          {loading ? "در حال ارسال..." : "ارسال لینک بازیابی"}
        </button>
      </form>
    </div>
  );
};

export default ForgotPassword;
