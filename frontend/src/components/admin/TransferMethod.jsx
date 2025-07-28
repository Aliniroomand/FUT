import React, { useEffect, useState } from 'react';
import {
  getTransferMethods,
  createTransferMethod,
  updateTransferMethod,
  deleteTransferMethod,
} from '../../services/api';

const TransferMethods = () => {
  const [methods, setMethods] = useState([]);
  const [newMethod, setNewMethod] = useState({ name: '', description: '', is_active: true });
  const [loading, setLoading] = useState(true);
  const [editId, setEditId] = useState(null);
  const [editMethod, setEditMethod] = useState({ name: '', description: '', is_active: true });

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
    await createTransferMethod(newMethod);
    setNewMethod({ name: '', description: '', is_active: true });
    fetchMethods();
  };

  const startEdit = (method) => {
    setEditId(method.id);
    setEditMethod({ ...method });
  };

  const handleEditChange = (e) => {
    const { name, value, type, checked } = e.target;
    setEditMethod(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const saveEdit = async () => {
    await updateTransferMethod(editId, editMethod);
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
    <div className="bg-black p-4 rounded-xl shadow-md text-white mt-8">
      <h2 className="text-xl mb-4 text-[#B8860B]">مدیریت شیوه‌های انتقال</h2>
      
      {/* فرم اضافه کردن */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="نام روش انتقال"
          value={newMethod.name}
          onChange={e => setNewMethod({...newMethod, name: e.target.value})}
          className="p-2 rounded bg-gray-900 border border-gray-700 w-full mb-2 text-white"
        />
        <textarea
          placeholder="توضیحات (اختیاری)"
          value={newMethod.description}
          onChange={e => setNewMethod({...newMethod, description: e.target.value})}
          className="p-2 rounded bg-gray-900 border border-gray-700 w-full mb-2 text-white"
        />
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
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
              <tr key={method.id} className="hover:bg-white/30 backdrop-blur-md">
                <td className="p-2 border border-gray-700">{method.name}</td>
                <td className="p-2 border border-gray-700">{method.description}</td>
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
