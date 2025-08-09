import { useState, useEffect } from 'react';
import { getPlayerCards, createPlayerCard, updatePlayerCard, deletePlayerCard } from '@/services/playerCardsApi';
import PlayerForm from './PlayerForm';
import PlayerList from './PlayerList';
import toast from 'react-hot-toast';

export default function PlayerManagement() {
  const [playerCards, setPlayerCards] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchPlayerCards = async () => {
    try {
      setLoading(true);
      const data = await getPlayerCards();
      setPlayerCards(data);
    } catch (error) {
      console.error('Error fetching player cards:', error);
      toast.error('خطا در دریافت اطلاعات بازیکنان');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlayerCards();
  }, []);

  const handleCreate = async (formData) => {
    try {
      await createPlayerCard(formData);
      await fetchPlayerCards();
      toast.success('بازیکن جدید با موفقیت ایجاد شد');
    } catch (error) {
      console.error('Error creating player card:', error);
      toast.error('خطا در ایجاد بازیکن جدید');
    }
  };

  const handleUpdate = async (id, formData) => {
    try {
      await updatePlayerCard(id, formData);
      await fetchPlayerCards();
      toast.success('اطلاعات بازیکن با موفقیت به‌روزرسانی شد');
      return true;
    } catch (error) {
      console.error('Error updating player card:', error);
      toast.error('خطا در به‌روزرسانی بازیکن');
      return false;
    }
  };

  const handleDelete = async (id) => {
    toast.custom((t) => (
      <div className={`${t.visible ? 'animate-enter' : 'animate-leave'} 
        bg-white/10 backdrop-blur-md border border-amber-500 rounded-lg p-4 shadow-lg`}>
        <p className="text-white mb-4">آیا از حذف این بازیکن مطمئن هستید؟</p>
        <div className="flex justify-end space-x-2">
          <button
            onClick={() => {
              toast.dismiss(t.id);
            }}
            className="px-4 py-2 text-sm text-white bg-gray-600 rounded hover:glass-light"
          >
            انصراف
          </button>
          <button
            onClick={async () => {
              toast.dismiss(t.id);
              try {
                await deletePlayerCard(id);
                await fetchPlayerCards();
                toast.success('بازیکن با موفقیت حذف شد');
              } catch (error) {
                console.error('Error deleting player card:', error);
                toast.error('خطا در حذف بازیکن');
              }
            }}
            className="px-4 py-2 text-sm text-white bg-red-600 rounded hover:bg-red-700"
          >
            حذف
          </button>
        </div>
      </div>
    ), {
      duration: Infinity, // toast تا زمانی که کاربر عملی انجام دهد باقی می‌ماند
    });
  };

  if (loading) return (
    <div className="flex justify-center items-center h-64">
      <div className="text-amber-500 text-lg">در حال بارگذاری اطلاعات بازیکنان...</div>
    </div>
  );

  return (
    <div className="space-y-6 p-4">
      <h2 className="text-xl font-bold text-amber-500">مدیریت کارت‌های بازیکنان</h2>
      <p className="text-sm font-bold text-red-500">فیلدهایی که با (*) نشان گذاری شده اند پرکردنشون الزامیه</p>
      
      <div className="bg-gold-900 p-4 rounded-lg">
        <PlayerForm 
          onSubmit={handleCreate} 
          initialData={null}
        />
      </div>

      <div className="bg-white/10 backdrop-blur-md p-4 rounded-lg">
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-amber-400">لیست بازیکنان</h3>
          <p className="text-sm text-gray-400 mt-1">
            تعداد بازیکنان: <span className='text-red-300'> {playerCards.length} </span>  برای ویرایش روی دکمه ویرایش در هر سطر کلیک کنید
          </p>
        </div>
        
        <PlayerList 
          players={playerCards} 
          onDelete={handleDelete}
          onUpdate={handleUpdate}
        />
      </div>
    </div>
  );
}