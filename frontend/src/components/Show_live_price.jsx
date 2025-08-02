import { useEffect, useState } from "react";
import { getLatestPrice } from "../services/api";
import toast from "react-hot-toast"

export default function LivePriceTicker() {
  const [prices, setPrices] = useState({ buy: null, sell: null });

  useEffect(() => {
    fetchPrices();
    const interval = setInterval(fetchPrices, 15000); // هر ۱۵ ثانیه آپدیت شود
    return () => clearInterval(interval);
  }, []);

  const fetchPrices = async () => {
    try {
      const data = await getLatestPrice();
      console.log(data.buy_price)
      setPrices({
        buy: data.buy_price,
        sell: data.sell_price,
      });
    } catch (err) {
      toast.error("خطا در دریافت قیمت:", err);
    }
  };
  return (
    <div className="fixed bottom-0 right-1/4 z-50  bg-amber-950 px-4 py-2 rounded-xl shadow-xl flex flex-row justify-between gap-1 text-md text-white w-2/4  animate-slideDown">
      <div className="flex justify-between gap-4">
        <span className="text-green-600">تعرفه خرید:</span>
        <span className="text-green-600 font-bold">
          {prices.buy || prices.buy === 0 ? `${prices.buy} 🪙` : "____"}
        </span>
      </div>
      <div className="flex justify-between gap-4">
        <span className="text-red-600">تعرفه فروش:</span>
        <span className="text-red-600 font-bold">
          {prices.sell || prices.sell === 0 ? `${prices.sell.toLocaleString()} 🪙` : "..."}
        </span>
      </div>
    </div>
  );
}
