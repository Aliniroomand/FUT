import React, { useEffect, useState } from "react";
import { BaseInfoSection } from "./PlayerForm/FormFields/BaseInfo";
import { CardInfoSection } from "./PlayerForm/FormFields/CardInfo";
import { PriceInfoSection } from "./PlayerForm/FormFields/PriceInfo";

export default function PlayerForm({ onSubmit, initialData, onCancel }) {
  const [formData, setFormData] = useState({
    name: "",
    club: "",
    position: "",
    version: "",
    rating: "",
    chemistry: 0,
    bid_price: "",
    buy_now_price: "",
    price_range_min: "",
    price_range_max: "",
    games_played: 0,
    contract_number: 0,
    owner_number: 0,
  });

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <BaseInfoSection formData={formData} handleChange={handleChange} />
        <CardInfoSection formData={formData} handleChange={handleChange} />
        <PriceInfoSection formData={formData} handleChange={handleChange} />
      </div>

      <div className="flex justify-end gap-3 pt-4 border-t border-gray-700">
        {initialData && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-500 transition-colors"
          >
            انصراف
          </button>
        )}
        <button
          type="submit"
          className="px-4 py-2 bg-amber-600 text-white rounded hover:bg-amber-500 transition-colors"
        >
          {initialData ? "ذخیره تغییرات" : "ایجاد بازیکن جدید"}
        </button>
      </div>
    </form>
  );
}