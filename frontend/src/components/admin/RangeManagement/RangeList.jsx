// RangeList.jsx
export default function RangeList({ ranges, onEdit, onDelete }) {
  if (ranges.length === 0) {
    return <div className="text-gray-400 text-center py-4">هیچ بازه‌ای ایجاد نشده است</div>;
  }

  return (
    <div className="space-y-2">
      {ranges.map(range => (
        <div key={range.id} className="bg-gray-700 p-3 rounded-lg flex justify-between items-center">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="font-bold text-amber-400">
                {range.min_value} - {range.max_value}
              </span>
              <span className="text-sm text-gray-300">{range.description}</span>
            </div>
            <div className="text-sm text-gray-400">
              <span>کارت اصلی: {range.primary_card?.name || range.primary_card_id}</span>
              {range.fallback_card_id && (
                <span className="mr-4"> | کارت جایگزین: {range.fallback_card?.name || range.fallback_card_id}</span>
              )}
            </div>
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={() => onEdit(range)}
              className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-500"
            >
              ویرایش
            </button>
            <button
              onClick={() => onDelete(range.id)}
              className="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-500"
            >
              حذف
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}