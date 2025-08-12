import React, { useEffect, useState } from "react";
import { useEAAccountLogic } from "../../../hooks/eaAccountLogic";
import { addEAAccount, deleteEAAccount, updateEADailyLimit } from "../../../services/eaAccountApi";
// import TestTransaction from "./TestTransaction";
import toast from "react-hot-toast";
import AccountTable from "./AccountTable";
import AccountForm from "./accountsForm";



const AdminEAAccountPanel = () => {
  const [accounts, setAccounts] = useState([]);
  const [editId, setEditId] = useState(null);
  const [editLimit, setEditLimit] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const { fetchAccounts, handleEdit } = useEAAccountLogic();

  useEffect(() => {
    fetchAccounts(setAccounts, (err) => toast.error(err?.message || "خطا در دریافت اطلاعات"));
  }, []);

  const handleAddAccount = async (payload) => {
    setLoading(true);
    try {
      await addEAAccount(payload);
      toast.success("اکانت با موفقیت اضافه شد");
      await fetchAccounts(setAccounts, (err) => toast.error(err?.message || "خطا در دریافت اطلاعات"));
    } catch (err) {
      toast.error(err.response?.data?.detail || err.message || "خطا در افزودن اکانت");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAccount = async (id) => {
    setLoading(true);
    try {
      await deleteEAAccount(id);
      toast.success("اکانت حذف شد");
      await fetchAccounts(setAccounts, (err) => toast.error(err?.message || "خطا در دریافت اطلاعات"));
    } catch (err) {
      toast.error(err.response?.data?.detail || err.message || "خطا در حذف اکانت");
    } finally {
      setLoading(false);
    }
  };

  const handleEditWrapper = (id, limit) => handleEdit(setEditId, setEditLimit, id, limit);

  const handleSaveWrapper = async (id) => {
    if (!editLimit) {
      setError("لطفاً مقدار سقف انتقال را وارد کنید.");
      return;
    }
    setLoading(true);
    try {
      await updateEADailyLimit(id, editLimit);
      setEditId(null);
      await fetchAccounts(setAccounts, (err) => setError(err?.message || "خطا در دریافت اطلاعات"));
      toast.success("سقف انتقال با موفقیت به‌روزرسانی شد");
    } catch (err) {
      const errorMessage = err ;
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-dark p-4 rounded shadow mt-8 max-w-6xl mx-auto">
      <h2 className="text-lg font-bold mb-4 text-amber-400">مدیریت اکانت‌های EA</h2>
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
    </div>
  );
};

export default AdminEAAccountPanel;
