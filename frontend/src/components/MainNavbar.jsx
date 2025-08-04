import { Link } from "react-router-dom";
import {
  FaHome,
  FaSignInAlt,
  FaUserCircle,
  FaPhoneAlt,
  FaQuestionCircle,
  FaTelegramPlane,
  FaHeadset,
} from "react-icons/fa";

const Navbar = () => {
  return (
    <nav className="glass-dark rounded-full text-white p-4 flex justify-between px-10 items-center">
      <div>
        <Link to="/" className="grid place-items-center gap-2">
          <span>
            <FaHome size={28} />
          </span>
          <p className="">صفحه اصلی</p>
        </Link>
      </div>
      <div className="flex gap-6 items-center">
        <Link to="/faq" className="grid place-items-center gap-2">
          <span className="text-center w-fit">
            <FaQuestionCircle size={28} />
          </span>
          <p className="">سوالات متداول</p>
        </Link>

        <Link to="/support" className="grid place-items-center items-center">
          <span>
            <FaHeadset size={28} />
          </span>
          <p className="">پشتیبانی</p>
        </Link>

        <Link to="/bot" className="grid place-items-center gap-2">
          <span>
            <FaTelegramPlane size={28} />
          </span>
          <p className="">ربات تلگرام</p>
        </Link>

        <Link to="/user/dashboard" className="grid place-items-center gap-2">
          <span>
            <FaUserCircle size={28} />
          </span>
          <p className="">داشبورد</p>
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
