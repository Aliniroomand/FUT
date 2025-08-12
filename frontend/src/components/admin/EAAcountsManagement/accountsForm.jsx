import { useState } from "react";

function AccountForm({ onAdd, loading }) {
  const [form, setForm] = useState({ name: "", email: "", platform: "", daily_limit: "" });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.name || !form.email || !form.platform) {
      toast.error("لطفا همه فیلدهای ضروری را پر کنید");
      return;
    }
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
      <input name="daily_limit" type="number" placeholder="سقف روزانه" value={form.daily_limit} onChange={handleChange} className="p-2 rounded border border-amber-400 bg-dark-hard text-white" />
      <button type="submit" disabled={loading} className="bg-amber-400 text-dark-hard px-3 py-1 rounded shadow hover:bg-amber-500">افزودن اکانت</button>
    </form>
  );
}

export default AccountForm