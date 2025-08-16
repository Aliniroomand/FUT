import { Link, useNavigate } from "react-router-dom";
import sandoghMiddle from "@/assets/sandogh-left.webp";
import sandoghRight from "@/assets/sandogh-right.webp";
import mainCoin from "@/assets/mainCoin.webp";
import ghaabLeft from "@/assets/ghaab-left.webp";
import MobileLayout from "./MobileLayout";
import { getUserRole } from "@/utils/auth";

const HomePage = () => {
  return (
    <div className="relative min-h-screen text-white overflow-hidden flex flex-col">
      {/* عنوان بالای صفحه */}
      <div className="absolute top-0 md:w-2/4 md:right-1/4 mx-2 rounded-full px-2 text-base glass-dark">
        
      <h1 className=" top-0  fut-gold-text font-extrabold  sm:text-2xl py-2 ">
        به اولین سامانه مدیریت سکه ادمین + هوش مصنوعی خوش اومدید
      </h1>
      </div>

      {/* Desktop layout */}
      <div className="hidden lg:grid grid-cols-3 absolute w-full h-[700px] items-end justify-items-center">
        {/* ستون اول */}
        <div id="1" className="relative  h-full w-full col-span-1">
          {/* بخش ۱-۱ */}
          <div className="absolute left-20 top-12 h-1/2 w-full ">
            <img
              src={ghaabLeft}
              alt="ghaabLeft"
              className="absolute h-55 rounded-2xl top-0"
            />
            <Link
              className="home-links w-30 h-30 text-amber-950 top-12 left-11"
              to="#"
            >
              پشتیبانی <br /> تماس با ما
            </Link>
          </div>

          {/* بخش ۱-۲ */}
          <div className="absolute  h-1/2 w-full bottom-0 left-0 ">
            <img
              src={sandoghMiddle}
              alt="sandoghMiddle"
              className="absolute w-85 left-10 bottom-20"
            />
            <Link
              className="absolute w-34 h-34 home-links left-38 bottom-26 text-shadow-2xl text-3xl! text-nowrap text-amber-950 shadow-white -skew-y-6"
              to={(() => {
                const role = getUserRole();
                if (role === "admin") return "/admin/dashboard";
                if (role === "user") return "/user/dashboard";
                return "/login";
              })()}
              rel="noreferrer"
            >
              ورود کاربران
            </Link>
          </div>
        </div>
        <div className="relative w-full h-full col-span-1 top-16 swing ">
          <img
            src={mainCoin}
            alt="mainCoin"
            className="absolute h-auto w-full "
          />
        </div>
        {/* ستون دوم */}
        <div id="2" className="relative h-full w-full col-span-1">
          {/* بخش ۲-۱ */}
          <div className="absolute w-full h-1/2  ">
            <img
              src={ghaabLeft}
              alt="ghaabLeft"
              className="absolute h-60 right-20 top-12 "
            />
            <Link
              className="home-links w-30 h-30 text-amber-950 right-35 top-28 text-2xl!"
              to="#"
            >
              سوالات متداول
            </Link>
          </div>

          {/* بخش ۲-۲ */}
          <div className="absolute h-1/2 w-full bottom-0 ">
            <img
              src={sandoghRight}
              alt="sandoghRight"
              className="absolute h-60 w-auto top-0 right-4"
            />
            <Link
              className="home-links w-30 h-30 right-39 bottom-30 text-amber-950 skew-y-8 text-3xl! text-nowrap"
              to="#"
            >
              ربات تلگرام
            </Link>
          </div>
        </div>
      </div>
      <MobileLayout />
    </div>
  );
};

export default HomePage;
