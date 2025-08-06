import { useState, useEffect } from "react";
import RangeForm from "./RangeForm";
import { getTransferMethod } from "@/services/api";

export default function RangeList({ ranges, onEdit, onDelete }) {
  const [editingId, setEditingId] = useState(null);
  const [methodName, setMethodName] = useState("");

  useEffect(() => {
    if (ranges.length > 0) {
      const methodId = ranges[0].transfer_method_id;
      fetchMethodName(methodId);
    }
  }, [ranges]);

  const fetchMethodName = async (methodId) => {
    try {
      const method = await getTransferMethod(methodId);
      setMethodName(method.name || "متد انتقال نامشخص");
    } catch (error) {
      console.error("خطا در دریافت نام متد انتقال:", error);
      setMethodName("متد انتقال نامشخص");
    }
  };

  const handleEdit = (range) => {
    setEditingId(range.id);
  };

  const handleCancel = () => {
    setEditingId(null);
  };

  if (ranges.length === 0) {
    return (
      <div className="text-gray-400 text-center py-6 bg-white/10 backdrop-blur-md rounded-lg">
        هیچ بازه‌ای ایجاد نشده است
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* عنوان کلی */}
      {/* لیست بازه‌ها */}
      {ranges.map((range) => (
        <div
          key={range.id}
          className="bg-white/10 backdrop-blur-md p-4 rounded-lg border border-gray-700"
        >
          {editingId === range.id ? (
            <RangeForm
              initialData={{
                min_value: range.min_value,
                max_value: range.max_value,
                description: range.description,
                primary_card_id: range.primary_card?.id || "",
                fallback_card_id: range.fallback_card?.id || "",
              }}
              onSubmit={(data) => {
                onEdit({ ...data, id: range.id });
                setEditingId(null);
              }}
              onCancel={handleCancel}
            />
          ) : (
            <div className="flex justify-between items-center">
              {/* نام متد انتقال */}
              <div className="text-xl text-gold text-center mb-6 bg-red-700 p-3 rounded-full">
                متد انتقال:{" "}
                <span className="text-goldfont-semibold">{methodName}</span>
              </div>
              <div className="flex flex-col gap-3 ">
                <span className="font-extrabold glass-dark rounded-4xl p-4 shadow-gold-accent shadow text-xl">
                  محدوده از
                  <span className="text-green-500">{" "}{range.min_value.toLocaleString()}{" "}
                  </span>
                  تا 
                  <span className="text-red-400">
                  {" "}{range.max_value.toLocaleString()}{" "}
                  </span>
                </span>

                {range.description && (
                  <span className="text-sm glass-light px-2 py-1 rounded">
                    {range.description}
                  </span>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div className="bg-gold-accent p-3 rounded-full">
                    <span className="block text-md text-gold mb-1 font-extrabold ">
                      کارت اصلی:
                    </span>
                    <span className="font-medium text-white">
                      {range.primary_card?.name || "نامشخص"}
                      {range.primary_card && ` (${range.primary_card.rating})`}
                    </span>
                  </div>

                  {range.fallback_card && (
                    <div className="bg-dark-1  p-3 rounded-full">
                      <span className="block text-md font-extrabold text-gold mb-1">
                        کارت جایگزین:
                      </span>
                      <span className="font-medium text-gold-accent">
                        {range.fallback_card.name}
                        {` (${range.fallback_card.rating})`}
                      </span>
                    </div>
                  )}
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <button
                  onClick={() => handleEdit(range)}
                  className="px-3 py-1.5 bg-blue-600 text-white rounded text-sm hover:bg-blue-500 transition"
                >
                  ویرایش
                </button>
                <button
                  onClick={() => onDelete(range.id)}
                  className="px-3 py-1.5 bg-red-600 text-white rounded text-sm hover:bg-red-500 transition"
                >
                  حذف
                </button>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
