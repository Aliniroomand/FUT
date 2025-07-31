import React, { useState } from "react";
import axios from "axios";
import { toast } from "react-hot-toast";

const MakeAdmin = () => {
  const [userId, setUserId] = useState("");
  const [loading, setLoading] = useState(false);

  const handleMakeAdmin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const token = localStorage.getItem("access_token");
      await axios.post(
        "http://localhost:8000/admin/make-admin",
        { user_id: userId },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success("کاربر با موفقیت ادمین شد!");
      setUserId("");
    } catch (err) {
      toast.error(
        err.response?.data?.detail || "خطا در ارتقای کاربر به ادمین!"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-dark-soft p-4 rounded shadow mt-8 max-w-md mx-auto">
      <h2 className="text-lg font-bold mb-2 text-amber-400">ارتقای کاربر به ادمین</h2>
      <form onSubmit={handleMakeAdmin} className="flex flex-col gap-2">
        <input
          type="number"
          placeholder="آیدی کاربر (user_id)"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="p-2 rounded border border-amber-400 bg-dark-hard text-white"
          required
        />
        <button
          type="submit"
          className="bg-amber-500 hover:bg-amber-600 text-white font-bold py-2 rounded"
          disabled={loading}
        >
          {loading ? "در حال ارسال..." : "ارتقا به ادمین"}
        </button>
      </form>
    </div>
  );
};

export default MakeAdmin;
