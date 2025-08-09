import { useEffect, useState } from "react";
import { getLatestPrice } from "@/services/transferAndRanges";
import toast from "react-hot-toast";

export default function LivePriceTicker() {
  const [prices, setPrices] = useState({ buy: null, sell: null });

  useEffect(() => {
    fetchPrices();
  }, []);

  const fetchPrices = async () => {
    try {
      const data = await getLatestPrice();
      setPrices({
        buy: data.buy_price,
        sell: data.sell_price,
      });
    } catch (err) {
      toast.error("خطا در دریافت قیمت:", err);
    }
  };

  return (
    <div className="
      absolute sm:top-0 z-50 bg-black/60 backdrop-blur-xs px-4 py-2 shadow-xl
      flex flex-row justify-between gap-4 text-md text-white
      w-full left-0 rounded-none border-2 border-black
      sm:rounded-xl sm:min-w-60 sm:left-0 sm:max-w-fit bottom-0 sm:bottom-auto 
    ">
      <div className="flex justify-between items-center  w-1/2">
        <span className=" text-yellow-500 text-shadow-2xl text-shadow-red-500 sm:text-md text-nowrap">🪙 خرید:</span>
        <span className=" text-yellow-500  font-bold text-md">
          {prices.buy || prices.buy === 0 ? `${prices.buy} ` : "دریافت نشد"}
        </span>
      </div>
      <div className="flex justify-between items-center   w-1/2">
        <span className="text-lime-500 text-shadow-2xl text-shadow-red-500 sm:text-md text-nowrap">🪙 فروش:</span>
        <span className="text-lime-500  font-bold text-md">
          {prices.sell || prices.sell === 0 ? `${prices.sell} ` : "دریافت نشد"}

        </span>
      </div>
    </div>
  );
}
