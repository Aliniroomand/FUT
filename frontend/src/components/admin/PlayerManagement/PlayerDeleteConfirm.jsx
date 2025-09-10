import { useState } from "react";
import { deletePlayerCard } from "@/services/playerCardsApi";

export default function PlayerDeleteConfirm({
  deps,
  player,
  otherPlayers,
  onClose,
  onDeleted,
}) {
  const [replacementId, setReplacementId] = useState(null);

  const confirmDeleteWithReplace = async () => {
    try {
      await deletePlayerCard(player.id, replacementId || null, false);
      onDeleted();
      onClose();
    } catch (err) {
      console.error(err);
      alert("خطا در حذف با جایگزین");
    }
  };

  const confirmDeleteForce = async () => {
    try {
      await deletePlayerCard(player.id, null, true);
      onDeleted();
      onClose();
    } catch (err) {
      console.error(err);
      alert("خطا در حذف بازه‌ها و کارت");
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
      <div className="bg-gray-900 text-white rounded-lg shadow-lg p-6 w-full max-w-lg">
        <h4 className="text-lg font-bold text-red-400 mb-4">
          هشدار: وابستگی پیدا شد
        </h4>

        <div className="space-y-3 text-right text-sm leading-6">
          {deps.primary_ranges?.length > 0 && (
            <>
              <p>
                این بازیکن در بازه‌های زیر به عنوان{" "}
                <strong className="text-amber-400">اصلی</strong> وجود دارد و با
                حذف این بازیکن این بازه‌ها نیز حذف خواهند شد:
              </p>
              <ul className="list-disc pr-6">
                {deps.primary_ranges.map((r) => (
                  <li key={`p-${r.id}`}>
                    بازه #{r.id}: {r.min_value} الی {r.max_value}
                  </li>
                ))}
              </ul>
            </>
          )}

          {deps.fallback_ranges?.length > 0 && (
            <>
              <p>
                این بازیکن در بازه‌های زیر به عنوان{" "}
                <strong className="text-blue-400">جایگزین</strong> وجود دارد:
              </p>
              <ul className="list-disc pr-6">
                {deps.fallback_ranges.map((r) => (
                  <li key={`f-${r.id}`}>
                    بازه #{r.id}: {r.min_value} الی {r.max_value}
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>

        <p className="mt-4">
          آیا می‌خواهید قبل از حذف، یک کارت جایگزین انتخاب کنید؟ در غیر این صورت
          با حذف کارت، بازه‌های مرتبط نیز حذف خواهند شد.
        </p>

        <div className="flex gap-2 items-center mt-4">
          <select
            className="px-2 py-1 rounded bg-gray-800 border border-gray-600 text-sm"
            value={replacementId}
            onChange={(e) =>
              setReplacementId(e.target.value ? Number(e.target.value) : null)
            }
          >
            <option value="">-- جایگزین انتخاب نشده --</option>
            {otherPlayers
              .filter((op) => op.id !== player.id)
              .map((op) => (
                <option key={op.id} value={op.id}>
                  {op.name} (id: {op.id})
                </option>
              ))}
          </select>

          <button
            onClick={() => {
              if (replacementId) {
                confirmDeleteWithReplace();
              } else {
                confirmDeleteForce();
              }
            }}
            className="px-3 py-1 bg-red-600 hover:bg-red-700 rounded text-sm"
          >
            بله، حذف کن
          </button>

          <button
            onClick={onClose}
            className="px-3 py-1 bg-gray-600 hover:bg-gray-700 rounded text-sm"
          >
            خیر، منصرف شدم
          </button>
        </div>
      </div>
    </div>
  );
}
