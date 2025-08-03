import { useEffect, useState } from "react";
import { getLatestPrice } from "../services/api";
import toast from "react-hot-toast";

export default function LivePriceTicker() {
  const [prices, setPrices] = useState({ buy: null, sell: null });

  useEffect(() => {
    fetchPrices();
  }, []);

  const fetchPrices = async () => {
    try {
      const data = await getLatestPrice();
      console.log(data.buy_price);
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
      fixed bottom-0 z-50 glass-dark px-4 py-2 shadow-xl animate-slideDown
      flex flex-row justify-between gap-4 text-md text-white
      w-full left-0 right-0 rounded-none
      sm:rounded-xl sm:w-2/4 sm:left-auto sm:right-1/4
    ">
      <div className="flex justify-between gap-4 text-shadow-white">
        <span className="text-green-600">تعرفه خرید:</span>
        <span className="text-green-600 font-bold">
          {prices.buy || prices.buy === 0 ? `${prices.buy} 🪙` : "دریافت نشد🪙"}
        </span>
      </div>
      <div className="flex justify-between gap-4">
        <span className="text-red-600">تعرفه فروش:</span>
        <span className="text-red-600 font-bold">
          {prices.sell || prices.sell === 0 ? `${prices.sell} 🪙` : "دریافت نشد🪙"}

        </span>
      </div>
    </div>
  );
}
