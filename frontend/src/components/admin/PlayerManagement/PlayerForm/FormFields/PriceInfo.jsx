import React from "react";
import { InputField } from "./FormInputs";

export const PriceInfoSection = ({ formData, handleChange }) => (
  <div className="space-y-2">
    <h3 className="font-medium text-amber-400 mb-2">اطلاعات قیمت</h3>
    <InputField
      label="قیمت پیشنهادی"
      name="bid_price"
      value={formData.bid_price ?? 0}
      onChange={handleChange}
    />
    <InputField
      label="قیمت خرید فوری"
      name="buy_now_price"
      value={formData.buy_now_price ?? 0}
      onChange={handleChange}
    />
    <InputField
      label="حداقل محدوده قیمت"
      name="price_range_min"
      value={formData.price_range_min ?? 0}
      onChange={handleChange}
    />
    <InputField
      label="حداکثر محدوده قیمت"
      name="price_range_max"
      value={formData.price_range_max ?? 0}
      onChange={handleChange}
    />
    <InputField
      label="تعداد قرارداد"
      name="contract_number"
      type="number"
      value={formData.contract_number || 0}
      onChange={handleChange}
    />
    <InputField
      label="تعداد مالکین"
      name="owner_number"
      type="number"
      value={formData.owner_number || 0}
      onChange={handleChange}
    />
  </div>
);