import React, { useEffect, useState } from 'react';
import { getLatestPrice, setPrice } from '../services/api';

const PriceManager = () => {
  const [buyPrice, setBuyPrice] = useState('');
  const [sellPrice, setSellPrice] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getLatestPrice()
      .then(data => {
        setBuyPrice(data.buy_price);
        setSellPrice(data.sell_price);
      })
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await setPrice(Number(buyPrice), Number(sellPrice));
    alert('قیمت‌ها با موفقیت ذخیره شدند');
  };

  if (loading) return <p className="text-white">در حال بارگذاری...</p>;

  return (
    <div className="bg-black p-4 rounded-xl shadow-md text-white">
      <h2 className="text-xl mb-4 text-[#B8860B]">مدیریت قیمت سکه</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label>
          قیمت خرید:
          <input
            type="number"
            value={buyPrice}
            onChange={(e) => setBuyPrice(e.target.value)}
            className="w-full p-2 rounded bg-gray-900 border border-gray-700 text-white"
          />
        </label>
        <label>
          قیمت فروش:
          <input
            type="number"
            value={sellPrice}
            onChange={(e) => setSellPrice(e.target.value)}
            className="w-full p-2 rounded bg-gray-900 border border-gray-700 text-white"
          />
        </label>
        <button type="submit" className="bg-[#A2711D] text-black font-bold py-2 px-4 rounded hover:bg-[#B8860B] transition">
          ذخیره
        </button>
      </form>
    </div>
  );
};

export default PriceManager;
