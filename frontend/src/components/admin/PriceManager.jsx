import React, { useEffect, useState } from "react";
import { getLatestPrice, setPrice } from "../../services/api";
import toast from "react-hot-toast";

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
      setOriginalBuyPrice(inputBuyPrice);
      setOriginalSellPrice(inputSellPrice);
    } catch {
      toast.error("خطا در ذخیره قیمت‌ها");
    }
  };

  if (loading) return <p className="text-[var(--color-text-primary)]">در حال بارگذاری...</p>;

  return (
    <div className="bg-white/30 backdrop-blur-md p-6 rounded-xl shadow-lg max-w-3xl mx-auto text-[var(--color-text-primary)]">
      <h2 className="text-2xl font-bold mb-6 text-[var(--color-gold-accent)] border-b border-[var(--color-gold-shadow)] pb-2">
        مدیریت قیمت سکه
      </h2>

      <form onSubmit={handleSubmit} className="flex flex-col gap-6">

        {/* باکس قیمت خرید */}
        <div className="bg-white/30 backdrop-blur-md border-l-4 border-green-500 p-4 rounded-md shadow-sm">
          <label className="block mb-2 font-semibold text-green-800">
            قیمت پایه خرید هر 100 کا (تومان):
          </label>
          <input
            type="number"
            value={inputBuyPrice}
            onChange={(e) => setInputBuyPrice(e.target.value)}
            className="w-full p-2 rounded bg-[var(--color-dark)] border border-gray-700 text-[var(--color-text-primary)] focus:outline-none focus:ring-1 focus:ring-green-800"
            placeholder="مثلاً 200"
          />
          <p className="mt-2 text-sm text-green-800 font-bold">
            قیمت خرید فعلی: {originalBuyPrice} تومان
          </p>
        </div>

        {/* باکس قیمت فروش */}
        <div className="bg-[#1f1f1f] border-l-4 border-red-500 p-4 rounded-md shadow-sm">
          <label className="block mb-2 font-semibold text-red-400">
            قیمت فروش هر 100 کا (تومان):
          </label>
          <input
            type="number"
            value={inputSellPrice}
            onChange={(e) => setInputSellPrice(e.target.value)}
            className="w-full p-2 rounded bg-[var(--color-dark)] border border-gray-700 text-[var(--color-text-primary)] focus:outline-none focus:ring-1 focus:ring-red-500"
            placeholder="مثلاً 200"
          />
          <p className="mt-2 text-sm text-red-400 font-bold">
            قیمت فروش فعلی: {originalSellPrice} تومان
          </p>
        </div>

        {/* دکمه ذخیره */}
        <div className="text-left">
          <button
            type="submit"
            className="bg-[var(--color-gold)] hover:bg-[var(--color-gold-light)] text-[var(--color-dark)] font-bold py-2 px-6 rounded-md transition-all duration-200"
          >
            ذخیره قیمت‌ها
          </button>
        </div>
      </form>
    </div>
  );
};

export default PriceManager;
