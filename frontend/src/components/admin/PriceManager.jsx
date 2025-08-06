import React from "react";
import useAdminPrices from "@/hooks/useAdminPrices";

const PriceManager = () => {
  const {
    loading,
    originalBuyPrice,
    originalSellPrice,
    inputBuyPrice,
    inputSellPrice,
    showEditPrices,
    setShowEditPrices,
    setInputBuyPrice,
    setInputSellPrice,
    handleBuyPriceSave,
    handleSellPriceSave,
  } = useAdminPrices();

  if (loading)
    return <p className="text-[var(--color-text-primary)]">در حال بارگذاری...</p>;

  return (
    <div className="glass-light p-6 rounded-xl shadow-lg max-w-3xl mx-auto text-[var(--color-text-primary)]">
      <h2 className="text-2xl font-bold mb-6  pb-2">مدیریت قیمت سکه</h2>
      <div className="bg-amber-400 rounded-2xl ">
        <p className="mt-2 text-2xl text-green-800 font-bold">
          {`قیمت خرید فعلی: ${
            originalBuyPrice ? `${originalBuyPrice} تومان` : "نامشخص"
          }`}
        </p>
        <p className="mt-2 text-2xl text-red-600 font-bold">
          {`قیمت فروش فعلی: ${
            originalSellPrice ? `${originalSellPrice} تومان` : "نامشخص"
          }`}
        </p>
        <button
          onClick={() => setShowEditPrices((prev) => !prev)}
          className="glass-dark rounded-full p-2 w-4/5 text-xl cursor-pointer"
        >
          ویرایش
        </button>
      </div>
      {showEditPrices && (
        <div className="flex flex-col gap-6">
          <div className="glass-light border-l-4 border-green-500 p-4 rounded-md shadow-sm">
            <label className="block mb-2 font-semibold text-green-800">
              تغییر قیمت پایه خرید هر 100 کا (تومان)
            </label>
            <input
              type="number"
              value={inputBuyPrice ?? ""}
              onChange={(e) => setInputBuyPrice(e.target.value)}
              className="w-full p-2 rounded bg-[var(--color-dark)] border border-gray-700 text-[var(--color-text-primary)] focus:outline-none focus:ring-1 focus:ring-green-800"
              placeholder="مثلاً 200"
            />
            <button
              onClick={handleBuyPriceSave}
              className="mt-3 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded"
            >
              ذخیره قیمت خرید
            </button>
          </div>

          <div className="bg-[#1f1f1f] border-l-4 border-red-500 p-4 rounded-md shadow-sm">
            <label className="block mb-2 font-semibold text-red-400">
              تغییر قیمت فروش هر 100 کا (تومان)
            </label>
            <input
              type="number"
              value={inputSellPrice ?? ""}
              onChange={(e) => setInputSellPrice(e.target.value)}
              className="w-full p-2 rounded bg-[var(--color-dark)] border border-gray-700 text-[var(--color-text-primary)] focus:outline-none focus:ring-1 focus:ring-red-500"
              placeholder="مثلاً 200"
            />
            <button
              onClick={handleSellPriceSave}
              className="mt-3 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded"
            >
              ذخیره قیمت فروش
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PriceManager;