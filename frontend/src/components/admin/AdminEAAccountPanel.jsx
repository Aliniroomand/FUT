
import React, { useEffect, useState } from "react";
import { useEAAccountLogic } from "../../hooks/eaAccountLogic";
import { addEAAccount, deleteEAAccount } from "../../services/eaAccountApi";
import TestTransaction from "./TestTransaction";

const statusColor = {
  active: "text-green-500",
  paused: "text-yellow-400",
  banned: "text-red-500",
};

function AccountForm({ onAdd, loading }) {
  const [form, setForm] = useState({ name: "", email: "", platform: "", daily_limit: "" });
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.name || !form.email || !form.platform) return;
    const payload = {
      name: form.name,
      email: form.email,
      platform: form.platform,
      daily_limit: form.daily_limit ? Number(form.daily_limit) : undefined,
      is_user_account: false,
      transferred_today: 0,
    };
    await onAdd(payload);
    setForm({ name: "", email: "", platform: "", daily_limit: "" });
  };
  return (
    <form className="mb-6 flex flex-col md:flex-row gap-2 items-center" onSubmit={handleSubmit}>
      <input name="name" type="text" placeholder="نام" value={form.name} onChange={handleChange} className="p-2 rounded border border-amber-400 bg-dark-hard text-white" />
      <input name="email" type="email" placeholder="ایمیل" value={form.email} onChange={handleChange} className="p-2 rounded border border-amber-400 bg-dark-hard text-white" />
      <input name="platform" type="text" placeholder="پلتفرم" value={form.platform} onChange={handleChange} className="p-2 rounded border border-amber-400 bg-dark-hard text-white" />
      <input name="daily_limit" type="number" placeholder="سقف روزانه" value={form.daily_limit} onChange={handleChange} className="p-2 rounded border border-amber-400 bg-dark-hard text-white w-24" />
      <button type="submit" disabled={loading} className="bg-amber-400 text-dark-hard px-3 py-1 rounded shadow hover:bg-amber-500">افزودن اکانت</button>
    </form>
  );
}

function AccountTable({ accounts, editId, editLimit, setEditId, setEditLimit, onEdit, onSave, onDelete, loading }) {
  return (
    <div className="overflow-x-auto">
        <TestTransaction/>
      <table className="min-w-full bg-dark-hard rounded-lg shadow">
        <thead>
          <tr className="bg-dark-soft text-amber-400">
            <th className="py-2 px-4">نام</th>
            <th className="py-2 px-4">ایمیل</th>
            <th className="py-2 px-4">پلتفرم</th>
            <th className="py-2 px-4">سقف روزانه</th>
            <th className="py-2 px-4">انتقال امروز</th>
            <th className="py-2 px-4">وضعیت</th>
            <th className="py-2 px-4">ویرایش سقف</th>
            <th className="py-2 px-4">حذف</th>
            <th className="py-2 px-4">پیشرفت روزانه</th>
          </tr>
        </thead>
        <tbody>
          {accounts?.map((acc) => {
            const limit = acc.daily_limit || 1000000;
            const percent = Math.min(100, (acc.transferred_today / limit) * 100);
            return (
              <tr key={acc.id} className="border-b border-dark-soft">
                <td className="py-2 px-4">{acc.name}</td>
                <td className="py-2 px-4">{acc.email}</td>
                <td className="py-2 px-4">{acc.platform}</td>
                <td className="py-2 px-4">
                  {editId === acc.id ? (
                    <input type="number" value={editLimit} onChange={(e) => setEditLimit(e.target.value)} className="p-1 rounded border border-amber-400 bg-dark-hard text-white w-20" />
                  ) : (
                    acc.daily_limit || <span className="text-xs text-gray-400">GLOBAL</span>
                  )}
                </td>
                <td className="py-2 px-4">{acc.transferred_today}</td>
                <td className={`py-2 px-4 font-bold ${statusColor[acc.status] || "text-gray-400"}`}>{acc.status}</td>
                <td className="py-2 px-4">
                  {editId === acc.id ? (
                    <button onClick={() => onSave(acc.id)} disabled={loading} className="bg-amber-400 text-dark-hard px-3 py-1 rounded shadow hover:bg-amber-500">ذخیره</button>
                  ) : (
                    <button onClick={() => onEdit(acc.id, acc.daily_limit || 0)} className="bg-dark-soft text-amber-400 border border-amber-400 px-3 py-1 rounded shadow hover:bg-amber-500 hover:text-white">ویرایش</button>
                  )}
                </td>
                <td className="py-2 px-4">
                  <button onClick={() => onDelete(acc.id)} disabled={loading} className="bg-red-400 text-white px-3 py-1 rounded shadow hover:bg-red-500">حذف</button>
                </td>
                <td className="py-2 px-4">
                  <div className="w-32 h-3 bg-gray-700 rounded">
                    <div className="h-3 rounded bg-amber-400" style={{ width: `${percent}%` }}></div>
                  </div>
                  <span className="text-xs text-gray-300 ml-2">{percent.toFixed(1)}%</span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
const AdminEAAccountPanel = () => {
  const [accounts, setAccounts] = useState([]);
  const [editId, setEditId] = useState(null);
  const [editLimit, setEditLimit] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const { fetchAccounts, handleEdit, handleSave } = useEAAccountLogic();

  useEffect(() => {
    fetchAccounts(setAccounts, setError);
  }, []);

  const handleAddAccount = async (payload) => {
    setLoading(true);
    setError(null);
    try {
      await addEAAccount(payload);
      await fetchAccounts(setAccounts, setError);
    } catch (err) {
      setError("خطا در افزودن اکانت");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAccount = async (id) => {
    setLoading(true);
    setError(null);
    try {
      await deleteEAAccount(id);
      await fetchAccounts(setAccounts, setError);
    } catch (err) {
      setError("خطا در حذف اکانت");
    } finally {
      setLoading(false);
    }
  };

  const handleEditWrapper = (id, limit) => handleEdit(setEditId, setEditLimit, id, limit);
  const handleSaveWrapper = (id) => handleSave(id, editLimit, setEditId, setLoading, () => fetchAccounts(setAccounts, setError), setError);

  return (
    <div className="glass-dark p-4 rounded shadow mt-8 max-w-6xl mx-auto">
      <h2 className="text-lg font-bold mb-4 text-amber-400"> EA مدیریت اکانت‌های </h2>
      <AccountForm onAdd={handleAddAccount} loading={loading} />
      <AccountTable
        accounts={accounts}
        editId={editId}
        editLimit={editLimit}
        setEditId={setEditId}
        setEditLimit={setEditLimit}
        onEdit={handleEditWrapper}
        onSave={handleSaveWrapper}
        onDelete={handleDeleteAccount}
        loading={loading}
      />
      {error && <div className="text-red-500 mt-4">{error}</div>}
    </div>
  );
};

export default AdminEAAccountPanel;
