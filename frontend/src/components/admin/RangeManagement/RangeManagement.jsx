// src/components/admin/RangeManagement/RangeManagement.jsx

import { useState, useEffect } from 'react';
import {
  getCardRanges,
  createCardRange,
  updateCardRange,
  deleteCardRange,
} from '@/services/transferAndRanges';
import RangeForm from './RangeForm';
import RangeList from './RangeList';
import { toast } from 'react-hot-toast';

export default function RangeManagement() {
  const [ranges, setRanges] = useState([]);
  const [selectedRange, setSelectedRange] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchRanges = async () => {
    try {
      setLoading(true);
      const data = await getCardRanges();
      setRanges(data);
    } catch (error) {
      toast.error('خطا در دریافت اطلاعات بازه‌ها');
      console.error('Error fetching ranges:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRanges();
  }, []);

  const handleSubmit = async (formData) => {
    try {
      if (selectedRange) {
        await updateCardRange(selectedRange.id, formData);
      } else {
        await createCardRange(formData);
      }
      await fetchRanges();
      setSelectedRange(null);
    } catch (error) {
      toast.error('خطا در ذخیره‌سازی بازه');
      console.error('Error saving range:', error);
    }
  };

  const handleInlineEdit = async (formDataWithId) => {
    try {
      const { id, ...formData } = formDataWithId;
      await updateCardRange(id, formData);
      await fetchRanges();
      toast.success("تغییرات با موفقیت انجام شد")
    } catch (error) {
      toast.error('خطا در ویرایش بازه');
      console.error('Error updating range:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('آیا از حذف این بازه مطمئن هستید؟')) {
      try {
        await deleteCardRange(id);
        await fetchRanges();
      } catch (error) {
        toast.error('خطا در حذف بازه');
        console.error('Error deleting range:', error);
      }
    }
  };

  if (loading)
    return <div className="text-center py-8 text-white">در حال بارگذاری...</div>;

  return (
    <div className="space-y-6">
      <div className="bg-white/10 backdrop-blur-md rounded-xl p-6">
        <h2 className="text-2xl font-bold text-amber-400 mb-6">
          {selectedRange ? 'ویرایش بازه قیمتی' : 'ایجاد بازه قیمتی جدید'}
        </h2>
        <RangeForm
          onSubmit={handleSubmit}
          initialData={selectedRange}
          onCancel={() => setSelectedRange(null)}
        />
      </div>

      <div className="bg-white/10 backdrop-blur-md rounded-xl p-6">
        <h2 className="text-2xl font-bold text-amber-400 mb-4">لیست بازه‌های قیمتی</h2>
        <RangeList
          ranges={ranges}
          onEdit={handleInlineEdit}
          onDelete={handleDelete}
        />
      </div>
    </div>
  );
}
