import { Link } from "react-router-dom";
import {
  FaHome,
  FaUserCircle,
  FaQuestionCircle,
  FaTelegramPlane,
  FaHeadset,
} from "react-icons/fa";
import coin from "@/assets/icon.webp"


const Navbar = () => {
  return (
    <>
      {/* mobile nav */}
      <nav className="fixed z-[100]  sm:hidden glass-dark w-svw p-1 text-white text-nowrap flex justify-around items-center">
          <Link to="/faq" className="grid place-items-center ">
            <span className="text-center w-fit">
              <FaQuestionCircle size={25} />
            </span>
            <p className="text-shadow-lg text-shadow-black text-xs">سوالات </p>
          </Link>

          <Link to="/support" className="grid place-items-center  items-center">
            <span>
              <FaHeadset size={25} />
            </span>
            <p className="text-shadow-lg text-shadow-black text-xs">پشتیبانی</p>
          </Link>

          <Link to="/" className="grid place-items-center ">

            <p className=" logo fut-gold-text text-2xl!">Sell Your FUT</p>
          </Link>
          <Link to="/bot" className="grid place-items-center  ">
            <span>
              <FaTelegramPlane size={25} />
            </span>
            <p className="text-shadow-lg text-shadow-black text-xs">ربات تلگرام</p>
          </Link>

          <Link to="/user/dashboard" className="grid place-items-center  ">
            <span>
              <FaUserCircle size={25} />
            </span>
            <p className="text-shadow-lg text-shadow-black text-xs">داشبورد</p>
          </Link>
      </nav>
      {/* desktop */}
      <nav className="hidden h-1/12 z-100 fixed glass-dark w-3/5 left-1/5 rounded-full p-1 text-white text-nowrap sm:flex justify-between px-2 items-center bg-red-500 ">
        <div>
          <Link to="/" className="flex items-center justify-between gap-3  ">
            <span>
              <img src={coin} alt="coin" />
            </span>
            <p className=" logo fut-gold-text">SellYourFUT</p>
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
