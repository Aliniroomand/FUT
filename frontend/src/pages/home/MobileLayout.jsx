import React from "react";
import { Link } from "react-router-dom";
import coin from "@/assets/MainCoin.webp";
import bgCoin from "@/assets/plainCoin.webp";
import ghaabLeft from "@/assets/ghaab-left.webp";
import LivePriceTicker from "@/components/Show_live_price";
import sandoghMiddle from "@/assets/sandogh-left.webp";
import sandoghRight from "@/assets/sandogh-right.webp";
import { getUserRole } from "@/utils/auth";

const MobileLayout = () => {
  return (
    <>
      <div className="lg:hidden w-svw h-svh flex flex-col items-center justify-center relative  p-2">
        <div className="absolute  w-fit h-auto flex items-center justify-center top-45 z-60 swing">
          <img src={coin} className="h-50" alt="Fut Coin" />
        </div>
        <div>
          <img
            src={ghaabLeft}
            alt="ghaabLeft"
            className="absolute h-30 rounded-2xl top-15 right-1"
          />
          <Link
            className="home-links w-10 h-10 right-11 top-25 text-xs! text-orange-950"
            to="#"
          >
            سوالات متداول
          </Link>
        </div>
        <div>
          <img
            src={ghaabLeft}
            alt="ghaabLeft"
            className="absolute h-30 rounded-2xl top-15 left-1"
          />
          <Link
            className="home-links w-10 h-10 left-10 top-25 text-xs! text-orange-950"
            to="#"
          >
            پشتیبانی
            <br />و تماس
          </Link>
        </div>
        <div>
          <img
            src={sandoghMiddle}
            alt="sandoghMiddle"
            className="absolute h-30 rounded-2xl bottom-35 left-1"
          />
          <Link
            className="absolute w-20 h-20 home-links left-12 bottom-35 text-shadow-2xl ! text-nowrap text-amber-950 shadow-white -skew-y-6"
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
        <div>
          <img
            src={sandoghRight}
            alt="sandoghRight"
            className="absolute h-30 rounded-2xl bottom-35 right-0"
          />
          <Link
            className="home-links w-20 h-20 right-16 bottom-33 text-amber-950 skew-y-8  text-nowrap"
            to="#"
          >
            ربات تلگرام
          </Link>
        </div>
      </div>
      <LivePriceTicker />
    </>
  );
};

export default MobileLayout;
