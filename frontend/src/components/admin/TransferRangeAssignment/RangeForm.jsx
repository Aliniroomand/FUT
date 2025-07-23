// RangeForm.jsx
import { useState, useEffect } from "react";

const fakeCards = [
  { id: 1, name: "کارت طلایی" },
  { id: 2, name: "کارت نقره‌ای" },
  { id: 3, name: "کارت برنزی" },
];

export default function RangeForm({ onSubmit, initialData }) {
  const [form, setForm] = useState({
    method_id: 1, // فعلاً ثابت
    start_price: "",
    end_price: "",
    primary_card_id: "",
    fallback_card_id: "",
  });

  useEffect(() => {
    if (initialData) {
      setForm(initialData);
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form);
    if (!initialData) {
      setForm({
        method_id: 1,
        start_price: "",
        end_price: "",
        primary_card_id: "",
        fallback_card_id: "",
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 rounded shadow">
      <input
        type="number"
        name="start_price"
        placeholder="شروع بازه"
        value={form.start_price}
        onChange={handleChange}
        className="p-2 border rounded"
        required
      />
      <input
        type="number"
        name="end_price"
        placeholder="پایان بازه"
        value={form.end_price}
        onChange={handleChange}
        className="p-2 border rounded"
        required
      />
      <select
        name="primary_card_id"
        value={form.primary_card_id}
        onChange={handleChange}
        className="p-2 border rounded"
        required
      >
        <option value="">کارت اصلی را انتخاب کنید</option>
        {fakeCards.map((card) => (
          <option key={card.id} value={card.id}>
            {card.name}
          </option>
        ))}
      </select>
      <select
        name="fallback_card_id"
        value={form.fallback_card_id}
        onChange={handleChange}
        className="p-2 border rounded"
      >
        <option value="">کارت جایگزین (اختیاری)</option>
        {fakeCards.map((card) => (
          <option key={card.id} value={card.id}>
            {card.name}
          </option>
        ))}
      </select>
      <button type="submit" className="col-span-2 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition">
        {initialData ? "ویرایش بازه" : "ثبت بازه جدید"}
      </button>
    </form>
  );
}
