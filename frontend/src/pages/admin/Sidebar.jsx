import { NavLink } from "react-router-dom";
import { useState } from "react";
import {
  FaChevronDown,
  FaChevronUp,
  FaHome,
  FaMoneyBillWave,
  FaExchangeAlt,
  FaGamepad,
  FaUserPlus,
  FaUsers,
  FaListOl,
  FaTasks
} from "react-icons/fa";
import { GiCardExchange } from "react-icons/gi";
import LogoutBTN from "../../helper/LogoutBTN";

const AdminSidebar = ({ isOpen, setIsOpen }) => {
  const [openDropdowns, setOpenDropdowns] = useState({});

  const toggleDropdown = (label) => {
    setOpenDropdowns((prev) => ({
      ...prev,
      [label]: !prev[label],
    }));
  };

  const links = [
    { to: "/admin/dashboard", label: "صفحه اصلی داشبورد", icon: <FaHome size={25} /> },
    { to: "/admin/mainPrices", label: "تعیین قیمت خرید و فروش", icon: <FaMoneyBillWave size={25} /> },
    { to: "/admin/transactions", label: "گزارش تراکنش‌ها", icon: <FaExchangeAlt size={25} /> },
    {
      label: "مدیریت کارت‌های انتقال",
      icon: <GiCardExchange size={25}/>,
      subItems: [
        { to: "/admin/rangeManagement/player", label: "مدیریت بازیکنان", icon: <FaUsers size={25} /> },
        { to: "/admin/rangeManagement/range", label: "مدیریت بازه‌ها", icon: <FaListOl size={25} /> },
        { to: "/admin/rangeManagement/method", label: "مدیریت روش‌های انتقال", icon: <FaTasks size={25} /> },
      ],
    },
    { to: "/admin/ea-accounts", label: "EA مدیریت اکانت‌های ", icon: <FaGamepad size={25} /> },
    { to: "/admin/make-admin", label: "ارتقای کاربر به ادمین", icon: <FaUserPlus size={25} /> },
  ];

  return (
    <aside
      className={`fixed md:static  right-0 h-full z-50 w-64 bg-dark-hard p-4 space-y-4 border-r bg-white/10 backdrop-blur-md transform transition-transform duration-300 top-12 
        ${isOpen ? "translate-x-0" : "translate-x-full"} md:translate-x-0 `}
    >
      {/* دکمه بستن برای موبایل */}
      <div className="flex justify-between items-center md:hidden mb-4">
        <button className="cursor-pointer" onClick={() => setIsOpen(false)}>
          ✕
        </button>
      </div>

      {/* لینک‌ها */}
      {links.map((link, index) =>
        link.subItems ? (
          <div key={index}>
            <button
              onClick={() => toggleDropdown(link.label)}
              className="w-full flex justify-between items-center py-2 font-semibold hover:bg-white text-shadow-lg text-shadow-black hover:text-amber-800 rounded"
            >
              <span className="flex items-center gap-2 flex-row-reverse">
                {link.icon}
                {link.label}
              </span>
              {openDropdowns[link.label] ? (
                <FaChevronUp size={12} className="text-xs" />
              ) : (
                <FaChevronDown size={12} className="text-xs" />
              )}
            </button>
            {openDropdowns[link.label] && (
              <div className="pr-6 mt-1 space-y-1">
                {link.subItems.map((sub) => (
                  <NavLink
                    key={sub.to}
                    to={sub.to}
                    className={({ isActive }) =>
                      `block py-2 rounded-lg transition hover:bg-white text-shadow-lg text-shadow-black hover:text-amber-950 ${
                        isActive
                          ? "bg-amber-500 text-dark-hard"
                          : "hover:bg-amber-800"
                      }`
                    }
                  >
                    <span className="flex items-center gap-2 flex-row-reverse">
                      {sub.icon}
                      {sub.label}
                    </span>
                  </NavLink>
                ))}
              </div>
            )}
          </div>
        ) : (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `block py-2 rounded-lg transition hover:bg-white text-shadow-lg text-shadow-black hover:text-amber-950 ${
                isActive ? "bg-amber-500 text-dark-hard" : "hover:bg-amber-800"
              }`
            }
          >
            <span className="flex items-center gap-2 flex-row-reverse">
              {link.icon}
              {link.label}
            </span>
          </NavLink>
        )
      )}
      <LogoutBTN />
    </aside>
  );
};

export default AdminSidebar;
