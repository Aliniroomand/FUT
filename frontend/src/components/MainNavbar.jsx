import { Link } from "react-router-dom";
import {
  FaHome,
  FaUserCircle,
  FaQuestionCircle,
  FaTelegramPlane,
  FaHeadset,
} from "react-icons/fa";

const Navbar = () => {
  return (
    <>
      {/* mobile nav */}
      <nav className="fixed h-15 sm:hidden glass-dark w-svw py-1 text-white text-nowrap flex justify-around items-center">
          <Link to="/faq" className="grid place-items-center ">
            <span className="text-center w-fit">
              <FaQuestionCircle size={25} />
            </span>
            <p className="text-xs">سوالات </p>
          </Link>

          <Link to="/support" className="grid place-items-center  items-center">
            <span>
              <FaHeadset size={25} />
            </span>
            <p className="text-xs">پشتیبانی</p>
          </Link>

          <Link to="/" className="grid place-items-center ">
            <span>
              <FaHome size={25} />
            </span>
            <p className="text-xs">صفحه اصلی</p>
          </Link>
          <Link to="/bot" className="grid place-items-center  ">
            <span>
              <FaTelegramPlane size={25} />
            </span>
            <p className="text-xs">ربات تلگرام</p>
          </Link>

          <Link to="/user/dashboard" className="grid place-items-center  ">
            <span>
              <FaUserCircle size={25} />
            </span>
            <p className="text-xs">داشبورد</p>
          </Link>
      </nav>
      {/* desktop */}
      <nav className="hidden fixed glass-dark w-3/5 left-1/5 h-15 rounded-full py-2 text-white text-nowrap sm:flex justify-between px-2 items-center">
        <div>
          <Link to="/" className="flex items-center justify-between gap-3  ">
            <span>
              <FaHome size={32} />
            </span>
            <p className="text-md">صفحه اصلی</p>
          </Link>
        </div>
        <div className="flex gap-6 items-center">
          <Link to="/faq" className="flex items-center justify-between gap-3  ">
            <span className="text-center w-fit">
              <FaQuestionCircle size={32} />
            </span>
            <p className="text-md">سوالات متداول</p>
          </Link>

          <Link to="/support" className="flex items-center justify-between gap-3">
            <span>
              <FaHeadset size={32} />
            </span>
            <p className="text-md">پشتیبانی</p>
          </Link>

          <Link to="/bot" className="flex items-center justify-between gap-3  ">
            <span>
              <FaTelegramPlane size={32} />
            </span>
            <p className="text-md">ربات تلگرام</p>
          </Link>

          <Link to="/user/dashboard" className="flex items-center justify-between gap-3  ">
            <span>
              <FaUserCircle size={32} />
            </span>
            <p className="text-md">داشبورد</p>
          </Link>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
