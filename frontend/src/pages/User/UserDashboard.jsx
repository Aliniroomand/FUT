import React, { useEffect, useState } from "react";
import { getProfile, logout } from "@/services/auth";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import LogoutBTN from "../../helper/LogoutBTN";

const UserDashboard = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await getProfile();
        setProfile(data);
      } catch (err) {
        toast.error("دریافت اطلاعات کاربر ناموفق بود");
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  if (loading)
    return <div className="text-center mt-8">در حال بارگذاری...</div>;
  if (!profile)
    return <div className="text-center mt-8">اطلاعاتی یافت نشد.</div>;

  return (
    <div className="max-w-xl mx-auto bg-dark-soft p-6 rounded shadow mt-8">
      <h1 className="text-2xl font-bold text-amber-500 mb-4">پروفایل کاربری</h1>
      <div className="mb-4">
        <div>
          <b>نام:</b> {profile.first_name || "-"}
        </div>
        <div>
          <b>نام خانوادگی:</b> {profile.last_name || "-"}
        </div>
        <div>
          <b>ایمیل:</b> {profile.email}
        </div>
        <div>
          <b>شماره موبایل:</b> {profile.phone_number}
        </div>
        <div>
          <b>شماره حساب:</b> {profile.bank_account_number || "-"}
        </div>
        <div>
          <b>نام حساب بانکی:</b> {profile.bank_account_name || "-"}
        </div>
      </div>
      <LogoutBTN />
    </div>
  );
};

export default UserDashboard;
