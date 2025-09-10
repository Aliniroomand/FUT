import React, { useEffect, useState } from "react";
import { BaseInfoSection } from "./PlayerForm/FormFields/BaseInfo";
import { CardInfoSection } from "./PlayerForm/FormFields/CardInfo";

export default function PlayerForm({ onSubmit, initialData }) {
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
  });
  const [addPlayer,setAddPlayer]=useState(false)

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    } else {
      // Reset form when there's no initial data (creating new player)
      setFormData({
        id:"",
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
    addPlayer ? (
    <form onSubmit={handleSubmit} className="space-y-6 bg-white/10 backdrop-blur-md p-3 sp-2">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
        <BaseInfoSection formData={formData} handleChange={handleChange} />
        <CardInfoSection formData={formData} handleChange={handleChange} />
      </div>

      <div className="flex justify-end gap-3 pt-4 border-t border-gray-700">
        <button
          type="submit"
          className="px-4 py-2 bg-amber-600 text-white rounded hover:bg-amber-500 transition-colors"
        >
          ایجاد بازیکن جدید
        </button>
      </div>
    </form>)
    :
    <button className="cursor-pointer bg-black rounded-2xl p-3 hover:scale-110" onClick={()=>setAddPlayer((prev)=>!prev)}>ایجاد بازیکن جدید</button>
  );
}