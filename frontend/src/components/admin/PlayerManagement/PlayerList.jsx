import { useState, useEffect } from "react";
import toast from "react-hot-toast";
import { CARD_TYPES, PLAYERS_POSITION } from "@/constants/cardTypes";
import {
  getPlayerCards,
  getPlayerDependencies,
  deletePlayerCard,
} from "@/services/playerCardsApi";
import PlayerDeleteConfirm from "@/components/admin/PlayerManagement/PlayerDeleteConfirm";

export default function PlayerList({ players, onDelete, onUpdate }) {
  const [editingPlayerId, setEditingPlayerId] = useState(null);
  const [formData, setFormData] = useState({});
  const [showConfirm, setShowConfirm] = useState(false);
  const [targetPlayer, setTargetPlayer] = useState(null);
  const [deps, setDeps] = useState(null);


  const onDeleteClick = async (player) => {
    try {
      // از API می‌پرسیم این بازیکن وابسته به چه بازه‌هایی هست
      const usage = await getPlayerDependencies(player.id);
      // usage => { primary_ranges: [...], fallback_ranges: [...] }
      const hasPrimary =
        usage.primary_ranges && usage.primary_ranges.length > 0;
      const hasFallback =
        usage.fallback_ranges && usage.fallback_ranges.length > 0;

      if (hasPrimary || hasFallback) {
        // اگر وابستگی داشت → باز می‌کنیم دیالوگ
        setTargetPlayer(player);
        setDeps(usage); // پاس دادن هر دو مجموعه
        setShowConfirm(true);
      } else {
        // اگر وابستگی نداشت → مستقیم حذف
        await deletePlayerCard(player.id);
        // اطلاع به والد که آیتم حذف شد
        if (typeof onDelete === "function") onDelete(player.id);
      }
    } catch (err) {
      // اگر backend 404 یا 500 داد، آن را نشان بده
      console.error("get dependencies error:", err);
      toast.error("خطا در بررسی وضعیت بازیکن");
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
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
    toast("ویرایش لغو شد", { icon: "⚠️" });
  };

  const displayValue = (value) => {
    return value || value === 0 ? (
      value
    ) : (
      <span className="text-gray-500 italic">----</span>
    );
  };

  if (!players || players.length === 0) {
    return (
      <div className="text-white text-center py-4">
        هیچ بازیکنی ایجاد نشده است
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full  ">
        <thead className="glass-light text-base  ">
          <tr className="divide-x divide-gray-600  ">
            <th className="px-4 py-3 font-medium text-white  tracking-wider ">
              id{" "}
            </th>
            <th className="px-4 py-3 font-medium text-white  tracking-wider">
              نام
            </th>
            <th className="px-4 py-3 font-medium text-white  tracking-wider">
              نوع کارت
            </th>
            <th className="px-4 py-3 font-medium text-white  tracking-wider">
              overall
            </th>
           
            <th className="px-4 py-3 font-medium text-white  tracking-wider">
              عملیات
            </th>
          </tr>
        </thead>
        <tbody className="bg-white/10 backdrop-blur-md divide-y divide-gray-700">
          {players.map((player) => {
            const isEditing = editingPlayerId === player.id;
            return (
              <tr
                key={player.id}
                className={
                  isEditing
                    ? "bg-gray-75 divide-x divide-gray-600"
                    : "divide-x divide-gray-600 "
                }
              >
                {/* id */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-white">
                  {isEditing ? (
                    <input
                      name="id"
                      value={formData.id || ""}
                      onChange={handleChange}
                      className="glass-light text-white px-2 py-1 rounded text-sm w-full"
                      placeholder="id بازیکن"
                    />
                  ) : (
                    displayValue(player.id)
                  )}
                </td>

                {/* Name */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-white">
                  {isEditing ? (
                    <input
                      name="name"
                      value={formData.name || ""}
                      onChange={handleChange}
                      className="glass-light text-white px-2 py-1 rounded text-sm w-full"
                      placeholder="نام بازیکن"
                    />
                  ) : (
                    displayValue(player.name)
                  )}
                </td>
                {/* Version */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-300">
                  {isEditing ? (
                    <select
                      name="version"
                      value={formData.version || ""}
                      onChange={handleChange}
                      className="glass-light text-white px-2 py-1 rounded text-sm w-full"
                    >
                      <option value="">-- انتخاب کنید --</option>
                      {CARD_TYPES.low_price_card_types.map((type, index) => (
                        <option key={index} value={type}>
                          {type}
                        </option>
                      ))}
                    </select>
                  ) : (
                    displayValue(player.version)
                  )}
                </td>

                {/* oVERALL Rating */}
                <td className="px-4 py-3 whitespace-nowrap text-sm text-amber-400 font-medium">
                  {isEditing ? (
                    <input
                      name="rating"
                      value={formData.rating || ""}
                      onChange={handleChange}
                      className="glass-light text-white px-2 py-1 rounded text-sm w-full"
                      placeholder="رتبه"
                    />
                  ) : (
                    displayValue(player.rating)
                  )}
                </td>

                
                {/* Actions */}
                <td className="px-4 py-3 whitespace-nowrap text-sm font-medium ">
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
                          onClick={() => onDeleteClick(player)}
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

      {showConfirm && targetPlayer && deps && (
        <PlayerDeleteConfirm
          deps={deps}
          player={targetPlayer}
          otherPlayers={players}
          onClose={() => setShowConfirm(false)}
          onDeleted={() => {
            // به والد اطلاع بده که آیتم حذف شده؛ اگر والد لیست را مدیریت می‌کند، باید onDelete را صدا بزند
            if (typeof onDelete === "function") onDelete(targetPlayer.id);
            // بستن دیالوگ و پاکسازی state
            setShowConfirm(false);
            setTargetPlayer(null);
            setDeps(null);
          }}
        />
      )}
    </div>
  );
}
