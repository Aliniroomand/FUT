import React from "react";
import { InputField, CheckboxField } from "./FormInputs";
import { CARD_TYPES } from "@/helper/cardTypes";

export const CardInfoSection = ({ formData, handleChange }) => (
  <div className="space-y-2">
    <h3 className="font-medium text-amber-400 mb-2">اطلاعات کارت</h3>
    <InputField
      label="* Card Version"
      name="version"
      value={formData.version || ""}
      onChange={handleChange}
      type="select"
      required
    >
      <option value="">-- انتخاب کنید --</option>
      {CARD_TYPES.low_price_card_types.map((type, index) => (
        <option key={index} value={type}>
          {type}
        </option>
      ))}
    </InputField>
    <InputField
      label="* rating"
      name="rating"
      type="number"
      value={formData.rating}
      onChange={handleChange}
      required
    />
    <InputField
      label="chemistry"
      name="chemistry"
      type="number"
      value={formData.chemistry}
      onChange={handleChange}
    />

  </div>
);