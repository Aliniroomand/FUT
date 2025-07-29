import React, { useEffect, useState } from "react";
import { getLatestPrice, setPrice } from "../../services/api";
import toast from "react-hot-toast";

const PriceManager = () => {
  const [originalBuyPrice, setOriginalBuyPrice] = useState(null);
  const [originalSellPrice, setOriginalSellPrice] = useState(null);
  const [inputBuyPrice, setInputBuyPrice] = useState("");
  const [inputSellPrice, setInputSellPrice] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getLatestPrice()
      .then((data) => {
        setOriginalBuyPrice(data.buy_price ?? "");
        setOriginalSellPrice(data.sell_price ?? "");
        setInputBuyPrice(data.buy_price ?? "");
        setInputSellPrice(data.sell_price ?? "");
      })
      .catch(() => {
        toast.error("خطا در بارگذاری قیمت‌ها");
      })
      .finally(() => setLoading(false));
  }, []);

  const handleBuyPriceSave = async () => {
    if (inputBuyPrice === "" || isNaN(Number(inputBuyPrice))) {
      toast.error("لطفاً قیمت خرید را به صورت عددی وارد کنید");
      return;
    }
    try {
      // علاوه بر buy_price، sell_price را هم از state می‌‌فرستیم
      await setPrice({
        buy_price: Number(inputBuyPrice),
        sell_price:
          originalSellPrice !== "" ? Number(originalSellPrice) : undefined,
      });
      toast.success("قیمت خرید با موفقیت ذخیره شد");
      setOriginalBuyPrice(inputBuyPrice);
    } catch (error) {
      console.error(
        "BuyPriceSave error detail:",
        error.response?.data || error
      );
      toast.error("خطا در ذخیره قیمت خرید");
    }
  };

  const handleSellPriceSave = async () => {
    if (inputSellPrice === "" || isNaN(Number(inputSellPrice))) {
      toast.error("لطفاً قیمت فروش را به صورت عددی وارد کنید");
      return;
    }
    try {
      // علاوه بر sell_price، buy_price را هم از state می‌فرستیم
      await setPrice({
        sell_price: Number(inputSellPrice),
        buy_price:
          originalBuyPrice !== "" ? Number(originalBuyPrice) : undefined,
      });
      toast.success("قیمت فروش با موفقیت ذخیره شد");
      setOriginalSellPrice(inputSellPrice);
    } catch (error) {
      console.error(
        "SellPriceSave error detail:",
        error.response?.data || error
      );
      toast.error("خطا در ذخیره قیمت فروش");
    }
  };

  if (loading)
    return (
      <p className="text-[var(--color-text-primary)]">در حال بارگذاری...</p>
    );

  return (
    <div className="glass-light p-6 rounded-xl shadow-lg max-w-3xl mx-auto text-[var(--color-text-primary)]">
      <h2 className="text-2xl font-bold mb-6 text-[var(--color-gold-accent)] border-b border-[var(--color-gold-shadow)] pb-2">
        مدیریت قیمت سکه
      </h2>

      <div className="flex flex-col gap-6">
        {/* باکس قیمت خرید */}
        <div className="glass-light border-l-4 border-green-500 p-4 rounded-md shadow-sm">
          <label className="block mb-2 font-semibold text-green-800">
            قیمت پایه خرید هر 100 کا (تومان):
          </label>
          <input
            type="number"
            value={inputBuyPrice ?? ""}
            onChange={(e) => setInputBuyPrice(e.target.value)}
            className="w-full p-2 rounded bg-[var(--color-dark)] border border-gray-700 text-[var(--color-text-primary)] focus:outline-none focus:ring-1 focus:ring-green-800"
            placeholder="مثلاً 200"
          />
          <p className="mt-2 text-sm text-green-800 font-bold">
            {`قیمت خرید فعلی: ${
              originalBuyPrice ? `${originalBuyPrice} تومان` : "نامشخص"
            }`}
          </p>
          <button
            onClick={handleBuyPriceSave}
            className="mt-3 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded"
          >
            ذخیره قیمت خرید
          </button>
        </div>

        {/* باکس قیمت فروش */}
        <div className="bg-[#1f1f1f] border-l-4 border-red-500 p-4 rounded-md shadow-sm">
          <label className="block mb-2 font-semibold text-red-400">
            قیمت فروش هر 100 کا (تومان):
          </label>
          <input
            type="number"
            value={inputSellPrice ?? ""}
            onChange={(e) => setInputSellPrice(e.target.value)}
            className="w-full p-2 rounded bg-[var(--color-dark)] border border-gray-700 text-[var(--color-text-primary)] focus:outline-none focus:ring-1 focus:ring-red-500"
            placeholder="مثلاً 200"
          />
          <p className="mt-2 text-sm text-red-400 font-bold">
            {`قیمت فروش فعلی: ${
              originalSellPrice ? `${originalSellPrice} تومان` : "نامشخص"
            }`}
          </p>
          <button
            onClick={handleSellPriceSave}
            className="mt-3 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded"
          >
            ذخیره قیمت فروش
          </button>
        </div>
      </div>
    </div>
  );
};

export default PriceManager;
