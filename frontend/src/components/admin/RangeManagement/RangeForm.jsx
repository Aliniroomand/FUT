import { useEffect, useState } from "react";
import { getPlayerCards, getTransferMethods } from "../../../services/api";

export default function RangeForm({ onSubmit, initialData, onCancel }) {
  const [formData, setFormData] = useState({
    min_value: "",
    max_value: "",
    description: "",
    primary_card_id: "",
    fallback_card_id: "",
    transfer_method_id: "",         // ← اضافه کردن فیلد
  });

  const [playerCards, setPlayerCards] = useState([]);
  const [transferMethods, setTransferMethods] = useState([]);  // ← لیست متدها
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");                      // ← پیام خطا

  // بارگذاری کارت‌ها و متدها
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [cards, methods] = await Promise.all([
          getPlayerCards(),
          getTransferMethods(),
        ]);
        setPlayerCards(cards);
        setTransferMethods(methods);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // مقداردهی اولیه اگر در حالت ویرایش باشیم
  useEffect(() => {
    if (initialData) {
      setFormData({
        min_value: initialData.min_value,
        max_value: initialData.max_value,
        description: initialData.description || "",
        primary_card_id: initialData.primary_card_id,
        fallback_card_id: initialData.fallback_card_id || "",
        transfer_method_id: initialData.transfer_method_id,  // ← مقداردهی
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setError("");
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // اعتبارسنجی ساده‌ی min < max
    if (parseFloat(formData.min_value) >= parseFloat(formData.max_value)) {
      setError("حداقل موجودی باید کمتر از حداکثر موجودی باشد");
      return;
    }
    // اطمینان از انتخاب شیوه انتقال
    if (!formData.transfer_method_id) {
      setError("لطفاً یک شیوه انتقال انتخاب کنید.");
      return;
    }

    // تبدیل به عدد
    const payload = {
      ...formData,
      min_value: parseFloat(formData.min_value),
      max_value: parseFloat(formData.max_value),
      primary_card_id: Number(formData.primary_card_id),
      fallback_card_id: formData.fallback_card_id
        ? Number(formData.fallback_card_id)
        : undefined,
      transfer_method_id: Number(formData.transfer_method_id),
    };

    onSubmit(payload);
  };

  if (loading) return <div>در حال بارگذاری...</div>;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <p className="text-red-500 text-base bg-amber-200 w-fit mx-auto p-3 rounded-full">
          {error}
        </p>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* حداقل */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            * حداقل موجودی مشتری
          </label>
          <input
            type="number"
            name="min_value"
            value={formData.min_value}
            onChange={handleChange}
            className="w-full p-2 rounded glass-light border border-gray-600 text-black"
            required
            min="0"
            step="0.01"
          />
        </div>

        {/* حداکثر */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            * حداکثر موجودی مشتری
          </label>
          <input
            type="number"
            name="max_value"
            value={formData.max_value}
            onChange={handleChange}
            className="w-full p-2 rounded glass-light border border-gray-600 text-black"
            required
            min="0"
            step="0.01"
          />
        </div>

        {/* کارت اصلی */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            * کارت اصلی
          </label>
          <select
            name="primary_card_id"
            value={formData.primary_card_id}
            onChange={handleChange}
            className="w-full p-2 rounded glass-light border border-gray-600 text-black"
            required
          >
            <option value="">انتخاب کنید</option>
            {playerCards.map((card) => (
              <option key={card.id} value={card.id}>
                {card.name} – {card.rating} ({card.version})
              </option>
            ))}
          </select>
        </div>

        {/* کارت جایگزین */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            کارت جایگزین
          </label>
          <select
            name="fallback_card_id"
            value={formData.fallback_card_id}
            onChange={handleChange}
            className="w-full p-2 rounded glass-light border border-gray-600 text-black"
          >
            <option value="">انتخاب کنید (اختیاری)</option>
            {playerCards.map((card) => (
              <option key={card.id} value={card.id}>
                {card.name} – {card.rating} ({card.version})
              </option>
            ))}
          </select>
        </div>

        {/* شیوه انتقال */}
        <div>
          <label className="block text-sm font-medium text-white mb-1">
            * شیوه انتقال
          </label>
          <select
            name="transfer_method_id"
            value={formData.transfer_method_id}
            onChange={handleChange}
            className="w-full p-2 rounded glass-light border border-gray-600 text-black"
            required
          >
            <option value="">انتخاب کنید</option>
            {transferMethods.length === 0 ? "بازه ای نیافت نشد" :transferMethods.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))}
          </select>
        </div>

        {/* توضیحات */}
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-300 mb-1">
            توضیحات
          </label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            className="w-full p-2 rounded glass-light border border-gray-600 text-black"
            rows={3}
            placeholder="توضیحات مربوط به این بازه قیمتی"
          />
        </div>
      </div>

      {/* دکمه‌های ارسال/انصراف */}
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