
import { useState } from 'react';
import RangeForm from './RangeForm';

export default function RangeList({ ranges, onEdit, onDelete }) {
  const [editingId, setEditingId] = useState(null);

  const handleEdit = (range) => {
    setEditingId(range.id);
  };

  const handleCancel = () => {
    setEditingId(null);
  };

  return ranges.length === 0 ? (
    <div className="text-gray-400 text-center py-6 bg-white/10 backdrop-blur-md rounded-lg">
      هیچ بازه‌ای ایجاد نشده است
    </div>
  ) : (
    <div className="space-y-3 ">
      {ranges.map((range) => (
        <div
          key={range.id}
          className="bg-white/10 backdrop-blur-md p-4 rounded-lg border  border-gray-700"
        >
          {editingId === range.id ? (
            <RangeForm
              initialData={{
                min_value: range.min_value,
                max_value: range.max_value,
                description: range.description,
                primary_card_id: range.primary_card?.id || '',
                fallback_card_id: range.fallback_card?.id || '',
              }}
              onSubmit={(data) => {
                onEdit({ ...data, id: range.id });
                setEditingId(null);
              }}
              onCancel={handleCancel}
            />
          ) : (
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-3 mb-2 ">
                <span className="font-extrabold bg-black/50 backdrop-blur-md rounded-4xl p-4 shadow-gold-accent shadow text-xl text-gold">
                  محدوده از {range.min_value.toLocaleString()} تا {range.max_value.toLocaleString()}
                </span>

                {range.description && (
                  <span className="text-sm bg-white/30 backdrop-blur-md px-2 py-1 rounded">
                    {range.description}
                  </span>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div className="bg-gold-accent backdrop-blur-md p-3 rounded">
                    <span className="block text-md text-gold mb-1 font-extrabold">کارت اصلی:</span>
                    <span className="font-medium text-white">
                      {range.primary_card?.name || 'نامشخص'}
                      {range.primary_card && ` (${range.primary_card.rating})`}
                    </span>
                  </div>

                  {range.fallback_card && (
                    <div className="bg-dark-1 backdrop-blur-md p-3 rounded">
                      <span className="block text-md font-extrabold text-gold mb-1">کارت جایگزین:</span>
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
