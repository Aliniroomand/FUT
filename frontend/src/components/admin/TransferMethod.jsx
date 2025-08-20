import React, { useEffect, useState } from 'react';
import {
  getTransferMethods,
  createTransferMethod,
  updateTransferMethod,
  deleteTransferMethod,
} from '@/services/transferAndRanges';

const TransferMethods = () => {
  const [methods, setMethods] = useState([]);
  const [newMethod, setNewMethod] = useState({ name: '', description: '', logic: '', is_active: true, multiplier: 1 });
  const [loading, setLoading] = useState(true);
  const [editId, setEditId] = useState(null);
  const [editMethod, setEditMethod] = useState({ name: '', description: '', logic: '', is_active: true, multiplier: 1 });

  useEffect(() => {
    fetchMethods();
  }, []);

  const fetchMethods = async () => {
    setLoading(true);
    const data = await getTransferMethods();
    setMethods(data);
    setLoading(false);
  };

  const handleAdd = async () => {
    if (!newMethod.name.trim()) {
      alert('نام روش را وارد کنید');
      return;
    }
    // ensure multiplier is a number
  const numeric = Number(newMethod.multiplier) || 1;
  const payload = { ...newMethod, multiplier: numeric, transfer_multiplier: numeric };
  await createTransferMethod(payload);
  setNewMethod({ name: '', description: '', logic: '', is_active: true, multiplier: 1 });
    fetchMethods();
  };

  const startEdit = (method) => {
  setEditId(method.id);
  setEditMethod({ ...method, multiplier: method.multiplier ?? method.transfer_multiplier ?? 1 });
  };

  const handleEditChange = (e) => {
    const { name, value, type, checked } = e.target;
    setEditMethod(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : type === 'number' ? (value === '' ? '' : Number(value)) : value,
    }));
  };

  const saveEdit = async () => {
  const numeric = Number(editMethod.multiplier) || Number(editMethod.transfer_multiplier) || 1;
  const payload = { ...editMethod, multiplier: numeric, transfer_multiplier: numeric };
  await updateTransferMethod(editId, payload);
    setEditId(null);
    fetchMethods();
  };

  const handleDelete = async (id) => {
    if (window.confirm('آیا مطمئن هستید حذف شود؟')) {
      await deleteTransferMethod(id);
      fetchMethods();
    }
  };

  if (loading) return <p className="text-white">در حال بارگذاری...</p>;

  return (
    <div className="glass-dark p-4 rounded-xl shadow-md text-white mt-8">
      <h2 className="text-xl mb-4 text-[#B8860B]">مدیریت شیوه‌های انتقال</h2>
      
      {/* فرم اضافه کردن */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="نام روش انتقال"
          name="name"
          value={newMethod.name}
          onChange={e => setNewMethod({...newMethod, name: e.target.value})}
          className="p-2 rounded bg-gray-900 border border-gray-700 w-full mb-2 text-white"
        />
        <textarea
          placeholder="توضیحات (اختیاری)"
          name="description"
          value={newMethod.description}
          onChange={e => setNewMethod({...newMethod, description: e.target.value})}
          className="p-2 rounded bg-gray-900 border border-gray-700 w-full mb-2 text-white"
        />
        <textarea
          placeholder="منطق کاری انتقال (logic)"
          name="logic"
          value={newMethod.logic}
          onChange={e => setNewMethod({...newMethod, logic: e.target.value})}
          className="p-2 rounded bg-gray-900 border border-gray-700 w-full mb-2 text-white"
          rows={3}
        />
        <input
          type="number"
          placeholder="ضریب انتقال (multiplier)"
          name="multiplier"
          value={newMethod.multiplier}
          onChange={e => setNewMethod({...newMethod, multiplier: e.target.value})}
          className="p-2 rounded bg-gray-900 border border-gray-700 w-full mb-2 text-white"
          step="0.01"
        />
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            name="is_active"
            checked={newMethod.is_active}
            onChange={e => setNewMethod({...newMethod, is_active: e.target.checked})}
          />
          فعال باشد
        </label>
        <button
          onClick={handleAdd}
          className="mt-2 bg-[#A2711D] hover:bg-[#B8860B] text-black font-bold py-2 px-4 rounded"
        >
          افزودن روش
        </button>
      </div>

      {/* جدول روش‌ها */}
      <table className="w-full text-white border border-gray-700 rounded">
        <thead>
          <tr className="bg-[#1C1C1C]">
            <th className="p-2 border border-gray-700">نام</th>
            <th className="p-2 border border-gray-700">توضیحات</th>
            <th className="p-2 border border-gray-700">منطق انتقال</th>
            <th className="p-2 border border-gray-700">ضریب انتقال</th>
            <th className="p-2 border border-gray-700">فعال</th>
            <th className="p-2 border border-gray-700">عملیات</th>
          </tr>
        </thead>
        <tbody>
          {methods.map((method) =>
            editId === method.id ? (
              <tr key={method.id} className="bg-white/10 backdrop-blur-md">
                <td className="p-2 border border-gray-700">
                  <input
                    name="name"
                    value={editMethod.name}
                    onChange={handleEditChange}
                    className="w-full p-1 rounded bg-gray-900 border border-gray-600 text-white"
                  />
                </td>
                <td className="p-2 border border-gray-700">
                  <textarea
                    name="description"
                    value={editMethod.description}
                    onChange={handleEditChange}
                    className="w-full p-1 rounded bg-gray-900 border border-gray-600 text-white"
                  />
                </td>
                <td className="p-2 border border-gray-700">
                  <textarea
                    name="logic"
                    value={editMethod.logic}
                    onChange={handleEditChange}
                    className="w-full p-1 rounded bg-gray-900 border border-gray-600 text-white"
                    rows={3}
                  />
                </td>
                <td className="p-2 border border-gray-700">
                  <input
                    type="number"
                    name="multiplier"
                    value={editMethod.multiplier}
                    onChange={handleEditChange}
                    className="w-full p-1 rounded bg-gray-900 border border-gray-600 text-white"
                    step="0.01"
                  />
                </td>
                <td className="p-2 border border-gray-700 text-center">
                  <input
                    type="checkbox"
                    name="is_active"
                    checked={editMethod.is_active}
                    onChange={handleEditChange}
                  />
                </td>
                <td className="p-2 border border-gray-700 space-x-2">
                  <button onClick={saveEdit} className="bg-[#A2711D] px-2 rounded hover:bg-[#B8860B]">ذخیره</button>
                  <button onClick={() => setEditId(null)} className="bg-red-600 px-2 rounded hover:bg-red-700">لغو</button>
                </td>
              </tr>
            ) : (
              <tr key={method.id} className="hover:glass-light">
                <td className="p-2 border border-gray-700">{method.name}</td>
                <td className="p-2 border border-gray-700">{method.description}</td>
                <td className="p-2 border border-gray-700 whitespace-pre-wrap max-w-xs overflow-hidden text-ellipsis">{method.logic}</td>
                <td className="p-2 border border-gray-700 text-center">{method.multiplier ?? method.transfer_multiplier ?? '-'}</td>
                <td className="p-2 border border-gray-700 text-center">{method.is_active ? '✔' : '✘'}</td>
                <td className="p-2 border border-gray-700 space-x-2">
                  <button onClick={() => startEdit(method)} className="bg-[#A2711D] px-2 rounded hover:bg-[#B8860B]">ویرایش</button>
                  <button onClick={() => handleDelete(method.id)} className="bg-red-600 px-2 rounded hover:bg-red-700">حذف</button>
                </td>
              </tr>
            )
          )}
        </tbody>
      </table>
    </div>
  );
};

export default TransferMethods;
