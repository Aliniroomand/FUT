// src/layouts/AdminLayout.jsx
import { Outlet } from "react-router-dom";
import { useState } from "react";
import { FaBars } from "react-icons/fa";
import Sidebar from "@/pages/admin/Sidebar";
import Navbar from "../../components/MainNavbar";

const AdminLayout = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
    <Navbar/>
      <div className="flex flex-row-reverse min-h-screen bg-dark-soft text-white relative  ">
        {/* دکمه منوی موبایل */}
        <button
          className="md:hidden absolute top-4 right-4 z-40 cursor-pointer"
          onClick={() => setIsOpen(true)}
        >
          <FaBars size={24} />
        </button>

        {/* سایدبار جداشده */}
        <Sidebar isOpen={isOpen} setIsOpen={setIsOpen} />

        {/* محتوای اصلی */}
        <main className="flex-1 p-4 md:p-6 overflow-x-auto">
          <Outlet />
        </main>
      </div>
    </>
  );
};

export default AdminLayout;
