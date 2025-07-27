import { useState } from "react";

export function CardRangeForm({ index, methods, onChange }) {
  const [formData, setFormData] = useState({
    min_price: "",
    max_price: "",
    player_name: "",
    transfer_method_id: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    const updated = { ...formData, [name]: value };
    setFormData(updated);
    onChange(index, updated);
  };

  return (
    <div className="border p-4 rounded-xl shadow space-y-4 ">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <input
          name="min_price"
          value={formData.min_price}
          onChange={handleChange}
          className="border p-2 rounded"
          placeholder="حداقل قیمت"
          type="number"
        />
        <input
          name="max_price"
          value={formData.max_price}
          onChange={handleChange}
          className="border p-2 rounded"
          placeholder="حداکثر قیمت"
          type="number"
        />
        <input
          name="player_name"
          value={formData.player_name}
          onChange={handleChange}
          className="border p-2 rounded"
          placeholder="نام بازیکن"
        />
        <select
          name="transfer_method_id"
          value={formData.transfer_method_id}
          onChange={handleChange}
          className="border p-2 rounded"
        >
          <option value="">انتخاب روش انتقال</option>
          {Array.isArray(methods) && methods.map((m) => (
            <option key={m.id} value={m.id}>
              {m.name}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
