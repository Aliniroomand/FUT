import React from "react";
import { Link } from "react-router-dom";
import coin from "@/assets/coin-2.webp";
import messi from "@/assets/messi.webp";
import ronaldo from "@/assets/ronaldo.webp";
import mbappe from "@/assets/mbape.webp";
import bgCoin from "@/assets/plainCoin.webp";
import LivePriceTicker from "../../components/Show_live_price";

const MobileLayout = () => {
  return (
      <>
      <h1 className="absolute top-0 glass-dark w-full rounded-3xl lg:hidden text-xl ">به سایت رسمی اوس پوری خوش اومدی </h1>
      <div className="lg:hidden w-svw h-svh flex flex-col items-center justify-center relative swing">

        <div className="relative w-90 flex items-center justify-center top-10 ">
          <img src={coin} alt="Fut Coin" />
          <img src={messi} alt="Messi" className="absolute w-32 -top-38" />
          <Link
            className="home-links w-20 h-20 top-30 left-0 "
            style={{ backgroundImage: `url(${bgCoin})` }}
            to="#"
          >
            پشتیبانی
            <br />و تماس
          </Link>
          <Link
            className="home-links w-20 h-20 right-0 top-30"
            style={{ backgroundImage: `url(${bgCoin})` }}
            to="#"
          >
            سوالات
            <br /> متداول
          </Link>
          <Link
            className="home-links w-20 h-20 right-10 bottom-0"
            style={{ backgroundImage: `url(${bgCoin})` }}
            to="#"
          >
            ورود کاربران
          </Link>
          <Link
            className="home-links w-20 h-20 left-10 bottom-0"
            style={{ backgroundImage: `url(${bgCoin})` }}
            to="#"
          >
            بات تلگرام
          </Link>
        </div>
      </div>
      <LivePriceTicker/>
    </>
  );
};

export default MobileLayout;
