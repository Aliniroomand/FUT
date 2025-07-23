// TransferRangeAssignment.jsx
import { useEffect, useState } from "react";
import { getCardRanges, createCardRange, updateCardRange, deleteCardRange } from "../../../services/api";
import RangeForm from "./RangeForm";
import RangeList from "./RangeList";

export default function TransferRangeAssignment() {
  const [ranges, setRanges] = useState([]);
  const [selected, setSelected] = useState(null);

  const fetchRanges = async () => {
    try {
      const data = await getCardRanges();
      setRanges(data);
    } catch (err) {
      console.error("Failed to fetch card ranges:", err);
    }
  };

  useEffect(() => {
    fetchRanges();
  }, []);

  const handleCreate = async (range) => {
    try {
      await createCardRange(range);
      await fetchRanges();
    } catch (err) {
      console.error("Create failed:", err);
    }
  };

  const handleUpdate = async (range) => {
    try {
      await updateCardRange(range.id, range);
      await fetchRanges();
      setSelected(null);
    } catch (err) {
      console.error("Update failed:", err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteCardRange(id);
      await fetchRanges();
    } catch (err) {
      console.error("Delete failed:", err);
    }
  };

  return (
    <div className="p-4 space-y-6">
      <h2 className="text-xl font-semibold">مدیریت بازه‌های قیمتی</h2>
      <RangeForm onSubmit={selected ? handleUpdate : handleCreate} initialData={selected} />
      <RangeList
        ranges={ranges}
        onEdit={setSelected}
        onDelete={handleDelete}
      />
    </div>
  );
}
