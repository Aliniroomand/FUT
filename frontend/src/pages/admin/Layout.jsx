// src/layouts/AdminLayout.jsx
import { Outlet } from "react-router-dom";
import { useState } from "react";
import { FaBars } from "react-icons/fa";
import Sidebar from "@/pages/admin/Sidebar";
import Navbar from "@/components/MainNavbar";
import OneLineAlertShow from "@/components/admin/Alerts/OneLineAlertShow";
import LiveAlertsAndPendingTxs from "../../components/admin/Alerts/OneLineAlertShow";

const AdminLayout = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
    <Navbar/>
      <div className="flex flex-row-reverse min-h-screen bg-dark-soft text-white relative  ">
        {/* دکمه منوی موبایل */}
        <button
          className="md:hidden absolute top-12 glass-dark right-0 rounded-bl-full p-3 pl-5 pb-4 z-50 cursor-pointer"
          onClick={() => setIsOpen(true)}
        >
          <FaBars size={24} />
        </button>

        {/* سایدبار جداشده */}
        <Sidebar isOpen={isOpen} setIsOpen={setIsOpen} />

        {/* محتوای اصلی */}
        <main className="flex-1 p-4 md:p-6 overflow-x-auto mt-13">
          <Outlet />
          <OneLineAlertShow/>
          <LiveAlertsAndPendingTxs/>
        </main>
      </div>
    </>
  );
};

export default AdminLayout;
