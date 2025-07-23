// RangeList.jsx
export default function RangeList({ ranges, onEdit, onDelete }) {
  return (
    <div className="space-y-2">
      {ranges.map((range) => (
          <div
          key={range.id}
          className="flex items-center justify-between  p-3 rounded shadow border"
          >
            {console.log(range)}
          <div className="text-sm w-full flex items-center justify-between ">
            <p className="text-amber-300 font-extrabold text-xl">
              از {range.min_value} تا {range.max_value}
            </p>
            <p>کارت جایگزین: {range.fallback_card_id || "ندارد"}</p>
            <span>
              <p>کارت اصلی: {range.primary_card_id}</p>
            </span>
          </div>
          <div className="flex gap-1 flex-col border-2 text-sm p-1">
            <button
              className=" hover:underline cursor-pointer"
              onClick={() => onEdit(range)}
            >
              ویرایش
            </button>
            <button
              className="text-red-600 hover:underline"
              onClick={() => onDelete(range.id)}
            >
              حذف
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
