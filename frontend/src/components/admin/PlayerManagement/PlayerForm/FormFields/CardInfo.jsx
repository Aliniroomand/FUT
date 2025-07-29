import React from "react";
import { InputField } from "./FormInputs";
import { CARD_TYPES, PLAYERS_POSITION } from "@/helper/cardTypes";

export const CardInfoSection = ({ formData, handleChange }) => (
  <div className="space-y-2">
    <h3 className="font-medium text-amber-400 mb-2">اطلاعات کارت</h3>
    <InputField
      label="* ورژن کارت"
      name="version"
      value={formData.version || ""}
      onChange={handleChange}
      type="select"
      required
    >
      <option className="text-black"  value="">-- انتخاب کنید --</option>
      {CARD_TYPES.low_price_card_types.map((type, index) => (
        <option className="text-black bg-white/10 backdrop-blur-md"  key={index} value={type}>
          {type}
        </option>
      ))}
    </InputField>
    <InputField
      label="* ریتینگ"
      name="rating"
      value={formData.rating || 0}
      onChange={handleChange}
      required
    />
    <InputField
      label="*کمستری"
      name="chemistry"
      type="number"
      value={formData.chemistry || 0}
      onChange={handleChange}
      required
    />
    <InputField
      label="پوزیشن"
      name="position"
      value={formData.position || ""}
      onChange={handleChange}
      type="select"
      required
    >
      <option value="">-- انتخاب پوزیشن --</option>
      {PLAYERS_POSITION.all_positions.map((pos, index) => (
        <option className="text-black" key={index} value={pos}>
          {pos}
        </option>
      ))}
    </InputField>
  </div>
);