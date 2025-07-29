import { useEffect, useState } from "react";
import { getPlayerCards } from "../../../services/api";

export default function RangeForm({ onSubmit, initialData, onCancel }) {
  const [formData, setFormData] = useState({
    min_value: "",
    max_value: "",
    description: "",
    primary_card_id: "",
    fallback_card_id: "",
  });
  
  const [playerCards, setPlayerCards] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPlayerCards = async () => {
      try {
        const data = await getPlayerCards();
        setPlayerCards(data);
      } catch (error) {
        console.error("Error fetching player cards:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchPlayerCards();
  }, []);

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // تبدیل مقادیر به عدد
    const processedData = {
      ...formData,
      min_value: parseFloat(formData.min_value),
      max_value: parseFloat(formData.max_value),
    };
    
    onSubmit(processedData);
  };

  if (loading) return <div>در حال بارگذاری...</div>;

  return (
    <form onSubmit={handleSubmit} className=" space-y-4">
      <div className="grid  grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
          *  حداقل موجودی مشتری
          </label>
          <input
            type="number"
            name="min_value"
            value={formData.min_value}
            onChange={handleChange}
            className="w-full p-2 rounded bg-white/30 backdrop-blur-md border border-gray-600 text-white"
            required
            min="0"
            step="0.01"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
             * حداکثر موجودی مشتری
          </label>
          <input
            type="number"
            name="max_value"
            value={formData.max_value}
            onChange={handleChange}
            className="w-full p-2 rounded bg-white/30 backdrop-blur-md border border-gray-600 text-white"
            required
            min="0"
            step="0.01"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
           * کارت اصلی
          </label>
          <select
            name="primary_card_id"
            value={formData.primary_card_id}
            onChange={handleChange}
            className="w-full p-2 rounded bg-white/30 backdrop-blur-md border border-gray-600 text-white"
            required
          >
            <option value="">انتخاب کنید</option>
            {playerCards.map((card) => (
              <option className="text-black" key={card.id} value={card.id}>
                {card.name} - {card.rating} ({card.version})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            کارت جایگزین
          </label>
          <select
            name="fallback_card_id"
            value={formData.fallback_card_id}
            onChange={handleChange}
            className="w-full p-2 rounded bg-white/30 backdrop-blur-md border border-gray-600 text-white"
          >
            <option value="">انتخاب کنید (اختیاری)</option>
            {playerCards.map((card) => (
              <option className="text-black" key={card.id} value={card.id}>
                {card.name} - {card.rating} ({card.version})
              </option>
            ))}
          </select>
        </div>

        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-300 mb-1">
            توضیحات
          </label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            className="w-full p-2 rounded bg-white/30 backdrop-blur-md border border-gray-600 text-white"
            rows={3}
            placeholder="توضیحات مربوط به این بازه قیمتی"
          />
        </div>
      </div>

      <div className="flex justify-end gap-2 pt-4">
        {initialData && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-500 transition"
          >
            انصراف
          </button>
        )}
        <button
          type="submit"
          className="px-4 py-2 bg-amber-600 text-white rounded hover:bg-amber-500 transition"
        >
          {initialData ? "ذخیره تغییرات" : "ایجاد بازه جدید"}
        </button>
      </div>
    </form>
  );
}