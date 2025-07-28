export default function RangeList({ ranges, onEdit, onDelete }) {
  if (ranges.length === 0) {
    return (
      <div className="text-gray-400 text-center py-6 bg-white/10 backdrop-blur-md rounded-lg">
        هیچ بازه‌ای ایجاد نشده است
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {ranges.map((range) => (
        <div 
          key={range.id} 
          className="bg-white/10 backdrop-blur-md p-4 rounded-lg border border-gray-700"
        >
          <div className="flex justify-between items-start">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <span className="font-bold text-lg text-amber-400">
                  {range.min_value.toLocaleString()} - {range.max_value.toLocaleString()}
                </span>
                {range.description && (
                  <span className="text-sm text-gray-300 bg-white/30 backdrop-blur-md px-2 py-1 rounded">
                    {range.description}
                  </span>
                )}
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="bg-white/30 backdrop-blur-md p-3 rounded">
                  <span className="block text-sm text-gray-400 mb-1">کارت اصلی:</span>
                  <span className="font-medium text-white">
                    {range.primary_card?.name || 'نامشخص'} 
                    {range.primary_card && ` (${range.primary_card.rating})`}
                  </span>
                </div>
                
                {range.fallback_card_id && (
                  <div className="bg-white/30 backdrop-blur-md p-3 rounded">
                    <span className="block text-sm text-gray-400 mb-1">کارت جایگزین:</span>
                    <span className="font-medium text-white">
                      {range.fallback_card?.name || 'نامشخص'} 
                      {range.fallback_card && ` (${range.fallback_card.rating})`}
                    </span>
                  </div>
                )}
              </div>
            </div>
            
            <div className="flex gap-2">
              <button
                onClick={() => onEdit(range)}
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
        </div>
      ))}
    </div>
  );
}