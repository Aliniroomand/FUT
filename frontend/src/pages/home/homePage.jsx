import { Link } from "react-router-dom";
import coin from "@/assets/coin-2.webp";
import messi from "@/assets/messi.webp";
import ronaldo from "@/assets/ronaldo.webp";
import mbappe from "@/assets/mbape.webp";
import bgCoin from "@/assets/plainCoin.webp";
import LivePriceTicker from "../../components/Show_live_price";
import MobileLayout from "./MobileLayout";

const HomePage = () => {
  return (
    <div className="relative min-h-screen text-white overflow-hidden flex flex-col">
      <h1 className="absolute lg:hidden top-0 glass-dark w-1/3 rounded-3xl right-1/3 text-2xl ">به سایت رسمی اوس پوری خوش اومدی </h1>
      {/* سکه مرکزی و بازیکن‌ها */}
      <div className="flex-grow relative">
        {/* Desktop layout */}
        <div className="hidden h-[700px] lg:grid grid-cols-3 absolute bottom-0 w-full items-end justify-items-center">
          <div className="relative h-full w-full col-span-1">
            <img
              src={mbappe}
              alt="mbappe"
              className="absolute h-[600px] w-auto bottom-0 left-4"
            />
            <a
              className="w-34 h-34 home-links left-4 top-48"
              style={{ backgroundImage: `url(${bgCoin})` }}
              href="https://t.me/your_bot"
              target="_blank"
              rel="noreferrer"
            >
              ورود کاربران
            </a>
          </div>

          <div className="relative w-96 h-96 flex items-center justify-center swing col-span-1 -bottom-2">
            <img src={coin} alt="Fut Coin" className="absolute w-full h-full" />
            <img src={messi} alt="Messi" className="absolute -top-50 w-40" />
            <Link
              className="home-links w-30 h-30 -left-12 -top-12"
              style={{ backgroundImage: `url(${bgCoin})` }}
              to="#"
            >
              پشتیبانی و<br /> تماس با ما
            </Link>
            <Link
              className="home-links w-30 h-30 -right-12 -top-12"
              style={{ backgroundImage: `url(${bgCoin})` }}
              to="#"
            >
              سوالات و<br /> متدها
            </Link>
          </div>

          <div className="relative h-full w-full col-span-1">
            <img
              src={ronaldo}
              alt="Ronaldo"
              className="absolute h-[600px] w-auto bottom-0 right-4"
            />
            <Link
              className="home-links w-30 h-30 right-16 top-60"
              style={{ backgroundImage: `url(${bgCoin})` }}
              to="#"
            >
              بات تلگرام
            </Link>
          </div>
        </div>

    <MobileLayout/>
      </div>
    </div>
  );
};

export default HomePage;
