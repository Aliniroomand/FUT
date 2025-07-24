import React from "react";
import { InputField } from "./FormInputs";

export const PriceInfoSection = ({ formData, handleChange }) => (
  <div className="space-y-2">
    <h3 className="font-medium text-amber-400 mb-2">اطلاعات قیمت</h3>
    <InputField
      label="Bid"
      name="bid_price"
      value={formData.bid_price}
      onChange={handleChange}
    />
    <InputField
      label="Buy now"
      name="buy_now_price"
      value={formData.buy_now_price}
      onChange={handleChange}
    />
    <InputField
      label="آخرین قیمت فروش"
      name="last_sale_price"
      value={formData.last_sale_price}
      onChange={handleChange}
    />
  </div>
);