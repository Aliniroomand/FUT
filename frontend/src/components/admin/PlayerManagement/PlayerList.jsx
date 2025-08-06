import { useState } from 'react';
import toast from 'react-hot-toast';
import { CARD_TYPES, PLAYERS_POSITION } from "@/helper/cardTypes";

export default function PlayerList({ players, onDelete, onUpdate }) {
  const [editingPlayerId, setEditingPlayerId] = useState(null);
  const [formData, setFormData] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleEditClick = (player) => {
    setFormData(player);
    setEditingPlayerId(player.id);
  };

  const handleSave = async (playerId) => {
    const success = await onUpdate(playerId, formData);
    if (success) {
      setEditingPlayerId(null);
    }
  };

  const handleCancel = () => {
    setEditingPlayerId(null);
    toast('ویرایش لغو شد', { icon: '⚠️' });
  };

const handleDelete = async (playerId) => {
  try {
    const usage = await checkPlayerUsage(playerId);

    if (usage.is_used) {
      const rangesInfo = usage.ranges.map(r => `${r.min_value} - ${r.max_value}`).join(', ');

      toast.custom((t) => (
        <div className={`bg-white/10 text-white p-4 rounded shadow-xl border border-yellow-500 ${t.visible ? 'animate-enter' : 'animate-leave'}`}>
          <p className="text-sm mb-2 leading-6">
            این بازیکن در بازه‌های زیر استفاده شده است:<br />
            <span className="text-amber-400">{rangesInfo}</span><br />
            با حذف این بازیکن، بازه‌های مربوطه نیز حذف خواهند شد.<br />
            آیا مطمئن هستید؟
          </p>
          <div className="flex justify-end gap-2 mt-4">
            <button
              onClick={() => toast.dismiss(t.id)}
              className="px-3 py-1 bg-gray-600 rounded hover:bg-gray-700 text-sm"
            >
              انصراف
            </button>
            <button
              onClick={async () => {
                toast.dismiss(t.id);
                try {
                  await deleteRangesWithPrimaryCard(playerId); // حذف بازه‌ها
                  await deletePlayerCard(playerId);             // حذف بازیکن
                  onDelete(playerId);
                  toast.success("بازیکن و بازه‌های مرتبط با موفقیت حذف شدند");
                } catch (err) {
                  toast.error("خطا در حذف بازیکن یا بازه‌ها");
                  console.error(err);
                }
              }}
              className="px-3 py-1 bg-red-600 hover:bg-red-700 rounded text-sm"
            >
              حذف نهایی
            </button>
          </div>
        </div>
      ), { duration: Infinity });
    } else {
      // بدون استفاده در بازه
      toast.custom((t) => (
        <div className={`bg-white/10 text-white p-4 rounded shadow-xl border border-red-600 ${t.visible ? 'animate-enter' : 'animate-leave'}`}>
          <p className="text-sm mb-2">آیا از حذف این بازیکن مطمئن هستید؟</p>
          <div className="flex justify-end gap-2 mt-4">
            <button
              onClick={() => toast.dismiss(t.id)}
              className="px-3 py-1 bg-gray-600 rounded hover:bg-gray-700 text-sm"
            >
              انصراف
            </button>
            <button
              onClick={async () => {
                toast.dismiss(t.id);
                try {
                  await deletePlayerCard(playerId);
                  onDelete(playerId);
                  toast.success("بازیکن با موفقیت حذف شد");
                } catch (err) {
                  toast.error("خطا در حذف بازیکن");
                  console.error(err);
                }
              }}
              className="px-3 py-1 bg-red-600 hover:bg-red-700 rounded text-sm"
            >
              حذف
            </button>
          </div>
        </div>
      ), { duration: Infinity });
    }
  } catch (err) {
    toast.error("خطا در بررسی وضعیت بازیکن");
    console.error(err);
  }
};
  const displayValue = (value) => {
    return value || value === 0 ? value : <span className="text-gray-500 italic">این مقدار رو وارد نکردی</span>;
  };

  if (players.length === 0) {
    return <div className="text-gray-400 text-center py-4">هیچ بازیکنی ایجاد نشده است</div>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full ">
        <thead className="glass-light text-base  ">
          <tr className='divide-x divide-gray-600'>
            <th className="px-4 py-3 font-medium text-gray-800  tracking-wider">نام</th>
            <th className="px-4 py-3 font-medium text-gray-800  tracking-wider">باشگاه</th>
            <th className="px-4 py-3 font-medium text-gray-800  tracking-wider">پوزیشن</th>
            <th className="px-4 py-3 font-medium text-gray-800  tracking-wider">ورژن</th>
            <th className="px-4 py-3 font-medium text-gray-800  tracking-wider">رتبه</th>
            <th className="px-4 py-3 font-medium text-gray-800  tracking-wider">کمستری</th>
            <th className="px-4 py-3 font-medium text-gray-800  tracking-wider">قیمت پیشنهادی</th>
            <th className="px-4 py-3 font-medium text-gray-800  tracking-wider">قیمت خرید فوری</th>
            <th className="px-4 py-3 font-medium text-gray-800  tracking-wider">بازی‌ها</th>
            <th className="px-4 py-3 font-medium text-gray-800  tracking-wider">عملیات</th>
          </tr>
        </thead>
        <tbody className="bg-white/10 backdrop-blur-md divide-y divide-gray-700">
          {players.map(player => {
            const isEditing = editingPlayerId === player.id;
            return (
              <tr key={player.id} className={isEditing ? "bg-gray-75 divide-x divide-gray-600" : "divide-x divide-gray-600"}>
                {/* Name */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-white">
                  {isEditing ? (
                    <input
                      name="name"
                      value={formData.name || ''}
                      onChange={handleChange}
                      className="glass-light text-white px-2 py-1 rounded text-sm w-full"
                      placeholder="نام بازیکن"
                    />
                  ) : (
                    displayValue(player.name)
                  )}
                </td>
                
                {/* Club */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-300">
                  {isEditing ? (
                    <input
                      name="club"
                      value={formData.club || ''}
                      onChange={handleChange}
                      className="glass-light text-white px-2 py-1 rounded text-sm w-full"
                      placeholder="باشگاه"
                    />
                  ) : (
                    displayValue(player.club)
                  )}
                </td>
                
                {/* Position */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-300">
                  {isEditing ? (
                    <select
                      name="position"
                      value={formData.position || ''}
                      onChange={handleChange}
                      className="glass-light text-white px-2 py-1 rounded text-sm w-full"
                    >
                      <option value="">-- انتخاب پوزیشن --</option>
                      {PLAYERS_POSITION.all_positions.map((pos, index) => (
                        <option key={index} value={pos}>{pos}</option>
                      ))}
                    </select>
                  ) : (
                    displayValue(player.position)
                  )}
                </td>
                
                {/* Version */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-300">
                  {isEditing ? (
                    <select
                      name="version"
                      value={formData.version || ''}
                      onChange={handleChange}
                      className="glass-light text-white px-2 py-1 rounded text-sm w-full"
                    >
                      <option value="">-- انتخاب کنید --</option>
                      {CARD_TYPES.low_price_card_types.map((type, index) => (
                        <option key={index} value={type}>{type}</option>
                      ))}
                    </select>
                  ) : (
                    displayValue(player.version)
                  )}
                </td>
                
                {/* Rating */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-amber-400 font-medium">
                  {isEditing ? (
                    <input
                      name="rating"
                      value={formData.rating || ''}
                      onChange={handleChange}
                      className="glass-light text-white px-2 py-1 rounded text-sm w-full"
                      placeholder="رتبه"
                    />
                  ) : (
                    displayValue(player.rating)
                  )}
                </td>
                
                {/* Chemistry */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-center text-gray-300">
                  {isEditing ? (
                    <input
                      name="chemistry"
                      type="number"
                      value={formData.chemistry || 0}
                      onChange={handleChange}
                      className="glass-light text-white px-2 py-1 rounded text-sm w-full"
                    />
                  ) : (
                    displayValue(player.chemistry)
                  )}
                </td>
                
                {/* Bid Price */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-300">
                  {isEditing ? (
                    <input
                      name="bid_price"
                      value={formData.bid_price || ''}
                      onChange={handleChange}
                      className="glass-light text-white px-2 py-1 rounded text-sm w-full"
                      placeholder="قیمت پیشنهادی"
                    />
                  ) : (
                    displayValue(player.bid_price)
                  )}
                </td>
                
                {/* Buy Now Price */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-300">
                  {isEditing ? (
                    <input
                      name="buy_now_price"
                      value={formData.buy_now_price || ''}
                      onChange={handleChange}
                      className="glass-light text-white px-2 py-1 rounded text-sm w-full"
                      placeholder="قیمت خرید فوری"
                    />
                  ) : (
                    displayValue(player.buy_now_price)
                  )}
                </td>
                
                {/* Games Played */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-center text-gray-300">
                  {isEditing ? (
                    <input
                      name="games_played"
                      type="number"
                      value={formData.games_played || 0}
                      onChange={handleChange}
                      className="glass-light text-white px-2 py-1 rounded text-sm w-full"
                    />
                  ) : (
                    displayValue(player.games_played)
                  )}
                </td>
                
                {/* Actions */}
                <td className="px-4 py-3 whitespace-nowrap text-sm font-medium">
                  <div className="flex flex-col sm:flex-row gap-2">
                    {isEditing ? (
                      <>
                        <button
                          onClick={() => handleSave(player.id)}
                          className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-500 transition-colors text-sm"
                        >
                          ذخیره
                        </button>
                        <button
                          onClick={handleCancel}
                          className="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-500 transition-colors text-sm"
                        >
                          انصراف
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          onClick={() => handleEditClick(player)}
                          className="px-3 py-1 bg-amber-600 text-white rounded hover:bg-amber-500 transition-colors text-sm"
                        >
                          ویرایش
                        </button>
                        <button
                          onClick={() => onDelete(player.id)}
                          className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-500 transition-colors text-sm"
                        >
                          حذف
                        </button>
                      </>
                    )}
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}