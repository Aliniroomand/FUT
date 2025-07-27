import { useState, useEffect, useCallback } from "react";
import {
  getCardRanges,
  createCardRange,
  updateCardRange,
  deleteCardRange,
} from "../../../services/api";
import RangeForm from "./RangeForm";
import RangeList from "./RangeList";
import toast, { Toaster } from "react-hot-toast";

export default function RangeManagement() {
  const [ranges, setRanges] = useState([]);
  const [selectedRange, setSelectedRange] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchRanges = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getCardRanges();
      setRanges(data);
    } catch (error) {
      console.error("Error fetching ranges:", error);
      toast.error("خطا در دریافت اطلاعات بازه‌ها");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchRanges();
  }, [fetchRanges]);

  const handleSubmit = useCallback(
    async (formData) => {
      try {
        if (selectedRange) {
          await updateCardRange(selectedRange.id, formData);
          toast.success("بازه با موفقیت ویرایش شد");
        } else {
          await createCardRange(formData);
          toast.success("بازه جدید با موفقیت ایجاد شد");
        }
        setSelectedRange(null);
        await fetchRanges();
      } catch (error) {
        console.error("Error saving range:", error);
        toast.error("خطا در ذخیره‌سازی بازه");
      }
    },
    [selectedRange, fetchRanges]
  );

  const handleInlineEdit = useCallback(
    async (formData) => {
      try {
        await updateCardRange(formData.id, formData);
        toast.success("بازه با موفقیت ویرایش شد");
        await fetchRanges();
      } catch (error) {
        console.error("Error updating range:", error);
        toast.error("خطا در ویرایش بازه");
      }
    },
    [fetchRanges]
  );

  // تایید حذف با toast و گزینه های تایید و لغو
  const handleDelete = useCallback(
    (id) => {
      const confirmDelete = () => {
        deleteCardRange(id)
          .then(() => {
            toast.success("بازه با موفقیت حذف شد");
            fetchRanges();
          })
          .catch((error) => {
            console.error("Error deleting range:", error);
            toast.error("خطا در حذف بازه");
          });
      };

      toast(
        (t) => (
          <div className="flex flex-col space-y-3">
            <div>آیا از حذف این بازه مطمئن هستید؟</div>
            <div className="flex justify-end space-x-2">
              <button
                className="px-3 py-1 rounded bg-gray-300 text-gray-800"
                onClick={() => toast.dismiss(t.id)}
              >
                لغو
              </button>
              <button
                className="px-3 py-1 rounded bg-red-600 text-white"
                onClick={() => {
                  confirmDelete();
                  toast.dismiss(t.id);
                }}
              >
                حذف
              </button>
            </div>
          </div>
        ),
        {
          duration: Infinity,
          position: "top-center",
          style: { minWidth: "250px" },
        }
      );
    },
    [fetchRanges]
  );

  if (loading) {
    return (
      <div className="text-center py-8 text-white">در حال بارگذاری...</div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-gray-800 rounded-xl p-6">
        <h2 className="text-2xl font-bold text-amber-400 mb-6">
          {selectedRange ? "ویرایش بازه قیمتی" : "ایجاد بازه قیمتی جدید"}
        </h2>
        <RangeForm
          onSubmit={handleSubmit}
          initialData={selectedRange}
          onCancel={() => setSelectedRange(null)}
        />
      </div>

      <div className="bg-gray-800 rounded-xl p-6">
        <h2 className="text-2xl font-bold text-amber-400 mb-4">
          لیست بازه‌های قیمتی
        </h2>
        <RangeList
          ranges={ranges}
          onEdit={handleInlineEdit}
          onDelete={handleDelete}
        />
      </div>
    </div>
  );
}
