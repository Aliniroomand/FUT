import { Link } from "react-router-dom";
import coin from "../assets/coin-2.webp";
import messi from "../assets/messi.webp";
import ronaldo from "../assets/ronaldo.webp";
import mbappe from "../assets/mbape.webp";
import bgCoin from "../assets/plainCoin.webp";
import AnimatedCoin from "@/helper/AnimatedCoin";
import LivePriceTicker from "../components/Show_live_price";

const HomePage = () => {
  return (
    <div className="relative min-h-screen text-white overflow-hidden flex flex-col">
      {/* لینک‌ها در بالای سکه */}
      <div className="flex justify-center flex-wrap gap-4 mt-4 z-10">
        <LivePriceTicker />
        {/* <AnimatedCoin text="خرید / فروش" to="/buy-sell" delay="0s" />
        <AnimatedCoin text="ورود کاربران" to="/login" delay="0.2s" />
        <AnimatedCoin text="پشتیبانی" to="/support" delay="0.4s" />
        <AnimatedCoin text="سوالات" to="/faq" delay="0.6s" />
        <AnimatedCoin text="قیمت لحظه‌ای" to="/live-price" delay="0.8s" /> */}
      </div>

      <div className="mt-8 z-10"></div>

      {/* سکه مرکزی و بازیکن‌ها */}
      <div className="flex-grow relative">
        {/* Desktop layout */}
        <div className="hidden h-full lg:grid grid-cols-4 absolute bottom-0 w-full items-end justify-items-center pb-4">
          {/* امباپه با سکه ربات تلگرام */}

          <div className="relative bottom-0 h-full w-full flex flex-col-reverse items-start left-0 px-4 ">
            <img
              src={mbappe}
              alt="Mbappe"
              className=" h-auto w-auto absolute bottom-0 animate-float-slow"
            />
            <div
              className="w-24 h-24 bg-cover bg-center bg-no-repeat mt-2 rounded-full flex items-center justify-center text-white text-md font-bold z-50 bottom-0 shadow-md "
              style={{
                backgroundImage: `url(${bgCoin})`,
              }}
            >
              <a
                className="w-24 h-24 bg-cover bg-center bg-no-repeat mt-2 rounded-full flex items-center justify-center text-white text-md font-bold z-50 bottom-0 shadow-md"
                style={{
                  backgroundImage: `url(${bgCoin})`,
                }}
                href="https://t.me/your_bot"
                target="_blank"
                rel="noreferrer"
              >
                ربات تلگرام
              </a>
            </div>
          </div>

          {/* سکه مرکزی */}
          <div className="col-span-2 relative flex justify-center items-end">
            <div className="relative w-96 h-96 flex items-center justify-center animate-float">
              <img
                src={coin}
                alt="Fut Coin"
                className="absolute w-full h-full animate-pulse "
              />
              <div className="absolute top-1/4 left-1/2 text-amber-500 text-xl font-bold -translate-x-1/2 -translate-y-1/2">
                به سایت اوس پوری خوش اومدید
              </div>
              {/* مسی بالای سکه */}
              <img src={messi} alt="Messi" className="absolute -top-26 w-24 " />
            </div>
          </div>
          <div className="h-full w-full">
            {/* رونالدو چپ */}
            <img
              src={ronaldo}
              alt="Ronaldo"
              className="absolute h-full w-auto bottom-0 right-4"
            />
          </div>
        </div>

        {/* Mobile layout */}
        <div className="lg:hidden flex flex-col items-center mt-8 mb-6">
          <div className="relative w-60 h-60 flex items-center justify-center">
            <img
              src={coin}
              alt="Fut Coin"
              className="w-full h-full animate-pulse"
            />
            <div className="absolute top-1/2 left-1/2 text-white text-xl font-bold -translate-x-1/2 -translate-y-1/2">
              FUT COIN
            </div>
            <img
              src={messi}
              alt="Messi"
              className="absolute -top-14 w-20 animate-float"
            />
            <img
              src={ronaldo}
              alt="Ronaldo"
              className="absolute left-[-20%] bottom-0 w-16 animate-float-slow"
            />
            <img
              src={mbappe}
              alt="Mbappe"
              className="absolute right-[-20%] bottom-0 w-16 animate-float-slow"
            />
          </div>

          <div
            className="w-24 h-24 bg-cover bg-center bg-no-repeat mt-4 rounded-full flex items-center justify-center text-black text-xs font-bold  shadow-2xl "
            style={{
              backgroundImage: `url(${bgCoin})`,
            }}
          >
            <a href="https://t.me/your_bot" target="_blank" rel="noreferrer">
              ربات تلگرام
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
