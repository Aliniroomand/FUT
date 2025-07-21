import React, { useEffect, useState } from "react";
import { getLatestPrice, setPrice } from "../services/api";
import toast, { Toaster } from "react-hot-toast";

const PriceManager = () => {
  const [originalBuyPrice, setOriginalBuyPrice] = useState("");
  const [originalSellPrice, setOriginalSellPrice] = useState("");
  const [inputBuyPrice, setInputBuyPrice] = useState("");
  const [inputSellPrice, setInputSellPrice] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getLatestPrice()
      .then((data) => {
        setOriginalBuyPrice(data.buy_price);
        setOriginalSellPrice(data.sell_price);
        setInputBuyPrice(data.buy_price);
        setInputSellPrice(data.sell_price);
      })
      .catch(() => {
        toast.error("خطا در بارگذاری قیمت‌ها");
      })
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (inputBuyPrice === "" || inputSellPrice === "") {
      toast.error("لطفاً هر دو قیمت را وارد کنید");
      return;
    }

    try {
      await setPrice(Number(inputBuyPrice), Number(inputSellPrice));
      toast.success("قیمت‌ها با موفقیت ذخیره شدند");

      // به‌روزرسانی مقدار اصلی با مقدار ذخیره شده
      setOriginalBuyPrice(inputBuyPrice);
      setOriginalSellPrice(inputSellPrice);
    } catch {
      toast.error("خطا در ذخیره قیمت‌ها");
    }
  };

  if (loading) return <p className="text-white">در حال بارگذاری...</p>;

  return (
    <div className="bg-black p-4 rounded-xl shadow-md text-white max-w-md mx-auto">
      <h2 className="text-xl mb-4 text-[#B8860B]">مدیریت قیمت سکه</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label>قیمت خرید:</label>
        <input
          type="number"
          value={inputBuyPrice}
          onChange={(e) => setInputBuyPrice(e.target.value)}
          className="w-full p-2 rounded bg-gray-900 border border-gray-700 text-white"
          placeholder="مقداری جدید"
        />
        <p className="text-green-600 text-xl font-bold">
          قیمت خرید فعلی : {originalBuyPrice}
        </p>

        <label>قیمت فروش:</label>
        <input
          type="number"
          value={inputSellPrice}
          onChange={(e) => setInputSellPrice(e.target.value)}
          className="w-full p-2 rounded bg-gray-900 border border-gray-700 text-white"
          placeholder="مقداری جدید"
        />
        <p className="text-red-500 text-xl font-bold">
          قیمت فروش فعلی : {originalSellPrice}
        </p>

        <button
          type="submit"
          className="bg-[#A2711D] text-black font-bold py-2 px-4 rounded hover:bg-[#B8860B] transition"
        >
          ذخیره
        </button>
      </form>
    </div>
  );
};

export default PriceManager;
