import { useState, useEffect } from "react";
import {
  getPlayerCards,
  createPlayerCard,
  updatePlayerCard,
} from "@/services/playerCardsApi";
import PlayerForm from "./PlayerForm";
import PlayerList from "./PlayerList";
import toast from "react-hot-toast";

export default function PlayerManagement() {
  const [playerCards, setPlayerCards] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchPlayerCards = async () => {
    try {
      setLoading(true);
      const data = await getPlayerCards();
      setPlayerCards(data);
    } catch (error) {
      console.error("Error fetching player cards:", error);
      toast.error("خطا در دریافت اطلاعات بازیکنان");
    } finally {
      setLoading(false);
    }
  };

  const playerDeleteHandler = (player) => {
    setPlayerCards((prev) => prev.filter((player) => player.id !== deletedId));
  };

  useEffect(() => {
    fetchPlayerCards();
  }, []);

  const handleCreate = async (formData) => {
    try {
      await createPlayerCard(formData);
      await fetchPlayerCards();
      toast.success("بازیکن جدید با موفقیت ایجاد شد");
    } catch (error) {
      console.error("Error creating player card:", error);
      toast.error("خطا در ایجاد بازیکن جدید");
    }
  };

  const handleUpdate = async (id, formData) => {
    try {
      await updatePlayerCard(id, formData);
      await fetchPlayerCards();
      toast.success("اطلاعات بازیکن با موفقیت به‌روزرسانی شد");
      return true;
    } catch (error) {
      console.error("Error updating player card:", error);
      toast.error("خطا در به‌روزرسانی بازیکن");
      return false;
    }
  };

  if (loading)
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-amber-500 text-lg">
          در حال بارگذاری اطلاعات بازیکنان...
        </div>
      </div>
    );

  return (
    <div className="space-y-6 p-4">
      <h2 className="text-xl font-bold text-amber-500">
        مدیریت کارت‌های بازیکنان
      </h2>
      <p className="text-sm font-bold text-red-500">
        فیلدهایی که با (*) نشان گذاری شده اند پرکردنشون الزامیه
      </p>

      <div className="bg-gold-900 p-4 rounded-lg">
        <PlayerForm onSubmit={handleCreate} initialData={null} />
      </div>

      <div className="bg-white/10 backdrop-blur-md p-4 rounded-lg">
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-amber-400">
            لیست بازیکنان
          </h3>
          <p className="text-sm text-white mt-1">
            تعداد بازیکنان:{" "}
            <span className="text-red-300"> {playerCards.length} </span> برای
            ویرایش روی دکمه ویرایش در هر سطر کلیک کنید
          </p>
        </div>

        <PlayerList
          players={playerCards}
          onUpdate={handleUpdate}
          onDelete={(deletedId) => {
            // فیلتر کردن بازیکن حذف شده
            setPlayerCards((prev) => prev.filter((p) => p.id !== deletedId));
            toast.success("بازیکن با موفقیت حذف شد");
          }}
        />
      </div>
    </div>
  );
}
