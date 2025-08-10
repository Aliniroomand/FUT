import React from "react";
import { NavLink } from "react-router-dom";

const UserSidebar = ({ isOpen, setIsOpen }) => {
  const links = [
    { to: "/user/dashboard", label: "پروفایل کاربری" },
    { to: "/user/transactions", label: "گزارش تراکنش‌ها" },
  ];

  return (
    <aside
      className={`fixed md:static top-0 right-0 h-full z-50 w-64 bg-dark-hard p-4 space-y-4 border-r bg-white/10 backdrop-blur-md transform transition-transform duration-300 
        ${isOpen ? "translate-x-0" : "translate-x-full"} md:translate-x-0 `}
    >
      {/* دکمه بستن برای موبایل */}
      <div className="flex justify-between items-center md:hidden mb-4">
        <button className="cursor-pointer" onClick={() => setIsOpen(false)}>
          ✕
        </button>
      </div>
      {links.map((link) => (
        <NavLink
          key={link.to}
          to={link.to}
          className={({ isActive }) =>
            `block px-4 py-2 rounded-lg transition hover:bg-white hover:text-amber-950   ${
              isActive ? "bg-amber-500 text-dark-hard text-shadow-lg text-shadow-black" : "hover:bg-amber-800"
            }`
          }
        >
          {link.label}
        </NavLink>
      ))}
    </aside>
  );
};

export default UserSidebar;
