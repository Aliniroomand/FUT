import React from "react";
import { InputField } from "./FormInputs";

export const BaseInfoSection = ({ formData, handleChange }) => (
  <div className="space-y-2">
    <h3 className="font-medium text-amber-400 mb-2">اطلاعات پایه</h3>
    <InputField
      label="* نام بازیکن"
      name="name"
      value={formData.name}
      onChange={handleChange}
      required
    />
    <InputField
      label="باشگاه"
      name="club"
      value={formData.club}
      onChange={handleChange}
    />
    <InputField
      label="ملیت"
      name="nation"
      value={formData.nation}
      onChange={handleChange}
    />
  </div>
);