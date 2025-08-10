import { NavLink } from 'react-router-dom';
import { useState } from 'react';
import { FaChevronDown, FaChevronUp } from 'react-icons/fa';
import LogoutBTN from '../../helper/LogoutBTN';

const AdminSidebar = ({ isOpen, setIsOpen }) => {
  const [openDropdowns, setOpenDropdowns] = useState({});

  const toggleDropdown = (label) => {
    setOpenDropdowns((prev) => ({
      ...prev,
      [label]: !prev[label],
    }));
  };

  const links = [
    { to: '/admin/dashboard', label: 'صفحه اصلی داشبورد' },
    { to: '/admin/mainPrices', label: 'تعیین قیمت خرید و فروش' },
    { to: '/admin/transactions', label: 'گزارش تراکنش‌ها' },
    {
        label: 'مدیریت کارت‌های انتقال',
        subItems: [
            { to: '/admin/rangeManagement/player', label: 'مدیریت بازیکنان' },
            { to: '/admin/rangeManagement/range', label: 'مدیریت بازه‌ها' },
            { to: '/admin/rangeManagement/method', label: 'مدیریت روش‌های انتقال' },
        ],
    },
    { to: '/admin/make-admin', label: 'ارتقای کاربر به ادمین' },
  ];

  return (
    <aside
      className={`fixed md:static top-0 right-0 h-full z-50 w-64 bg-dark-hard p-4 space-y-4 border-r bg-white/10 backdrop-blur-md transform transition-transform duration-300 
        ${isOpen ? 'translate-x-0' : 'translate-x-full'} md:translate-x-0 `}
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
              className="glass-dark w-full flex justify-between items-center px-4 py-2 font-semibold text-amber-400 hover:bg-white hover:text-amber-800 rounded "
            >
              {link.label}
              {openDropdowns[link.label] ? (
                <FaChevronUp className="text-xs" />
              ) : (
                <FaChevronDown className="text-xs" />
              )}
            </button>
            {openDropdowns[link.label] && (
              <div className="pl-6 mt-1 space-y-1">
                {link.subItems.map((sub) => (
                  <NavLink
                    key={sub.to}
                    to={sub.to}
                    className={({ isActive }) =>
                      `block px-3 py-1 text-sm transitiontext-shadow-lg text-shadow-black rounded-full ${
                        isActive ? 'bg-amber-500 text-dark-hard' : 'hover:bg-amber-800'
                      }`
                    }
                  >
                    {sub.label}
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
              `block px-4 py-2 rounded-lg transition hover:bg-white text-shadow-lg text-shadow-black hover:text-amber-950   ${
                isActive ? 'bg-amber-500 text-dark-hard' : 'hover:bg-amber-800'
              }`
            }
          >
            {link.label}
          </NavLink>
        )
      )}
      <LogoutBTN/>
    </aside>
  );
};

export default AdminSidebar;
