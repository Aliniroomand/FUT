// RangeManagement.jsx
import { useState, useEffect } from 'react';
import { getCardRanges, createCardRange, updateCardRange, deleteCardRange } from '../../../services/api';
import RangeForm from './RangeForm';
import RangeList from './RangeList';

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
      console.error('Error saving range:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('آیا از حذف این بازه مطمئن هستید؟')) {
      try {
        await deleteCardRange(id);
        await fetchRanges();
      } catch (error) {
        console.error('Error deleting range:', error);
      }
    }
  };

  if (loading) return <div>در حال بارگذاری...</div>;

  return (
    <div className="space-y-6 p-4">
      <h2 className="text-xl font-bold text-amber-500">مدیریت بازه‌های قیمتی</h2>
      
      <div className="bg-gray-800 p-4 rounded-lg">
        <RangeForm 
          onSubmit={handleSubmit} 
          initialData={selectedRange} 
          onCancel={() => setSelectedRange(null)}
        />
      </div>

      <div className="bg-gray-800 p-4 rounded-lg">
        <RangeList 
          ranges={ranges} 
          onEdit={setSelectedRange} 
          onDelete={handleDelete} 
        />
      </div>
    </div>
  );
}