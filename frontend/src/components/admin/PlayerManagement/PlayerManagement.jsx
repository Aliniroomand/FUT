import { useState, useEffect } from 'react';
import { getPlayerCards, createPlayerCard, updatePlayerCard, deletePlayerCard } from '@/services/api';
import PlayerForm from './PlayerForm';
import PlayerList from './PlayerList';

export default function PlayerManagement() {
  const [playerCards, setPlayerCards] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchPlayerCards = async () => {
    try {
      setLoading(true);
      const data = await getPlayerCards();
      setPlayerCards(data);
    } catch (error) {
      console.error('Error fetching player cards:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlayerCards();
  }, []);

  const handleSubmit = async (formData) => {
    try {
      if (selectedPlayer) {
        await updatePlayerCard(selectedPlayer.id, formData);
      } else {
        await createPlayerCard(formData);
      }
      await fetchPlayerCards();
      setSelectedPlayer(null);
    } catch (error) {
      console.error('Error saving player card:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('آیا از حذف این بازیکن مطمئن هستید؟')) {
      try {
        await deletePlayerCard(id);
        await fetchPlayerCards();
      } catch (error) {
        console.error('Error deleting player card:', error);
      }
    }
  };

  if (loading) return <div>در حال بارگذاری...</div>;

  return (
    <div className="space-y-6 p-4">
      <h2 className="text-xl font-bold text-amber-500">مدیریت کارت‌های بازیکنان</h2>
      <p className="text-sm font-bold text-red-500">فیلدهایی که با (*) نشان گذاری شده اند پرکردنشون الزامیه</p>
      
      <div className="bg-gold-900 p-4 rounded-lg">
        <PlayerForm 
          onSubmit={handleSubmit} 
          initialData={selectedPlayer} 
          onCancel={() => setSelectedPlayer(null)}
        />
      </div>

      <div className="bg-gray-800 p-4 rounded-lg">
        <PlayerList 
          players={playerCards} 
          onEdit={setSelectedPlayer} 
          onDelete={handleDelete} 
        />
      </div>
    </div>
  );
}