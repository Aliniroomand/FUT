
import React, { useState, useEffect } from "react";
import api from "../../services/api";

function TestTransaction() {
  const [amount, setAmount] = useState(0);
  const [accountId, setAccountId] = useState("");
  const [result, setResult] = useState("");
  const [accounts, setAccounts] = useState([]);
  const [usedAccount, setUsedAccount] = useState(null);

  useEffect(() => {
    // دریافت لیست اکانت‌ها برای انتخاب
    api.get("/ea-accounts/").then(res => setAccounts(res.data));
  }, []);

  const handleTx = async (e) => {
    e.preventDefault();
    setResult("");
    setUsedAccount(null);
    try {
      // ارسال تراکنش
      const res = await api.post("/transactions/", { account_id: accountId, amount: Number(amount) });
      setResult("موفق: " + (res.data?.message || "تراکنش ثبت شد"));
      // دریافت مجدد لیست اکانت‌ها برای نمایش پیشرفت
      const accRes = await api.get("/ea-accounts/");
      setAccounts(accRes.data);
      // پیدا کردن اکانت استفاده شده
      const used = accRes.data.find(acc => acc.id === Number(accountId));
      setUsedAccount(used);
    } catch (err) {
      setResult("خطا: " + (err?.response?.data?.detail || err?.message || "نامشخص"));
    }
  };

  return (
    <div className="glass-dark p-4 rounded shadow mt-8 max-w-xl mx-auto">
      <h3 className="text-md font-bold mb-2 text-amber-400">تست تراکنش</h3>
      <form className="flex gap-2 items-center" onSubmit={handleTx}>
        <select value={accountId} onChange={e => setAccountId(e.target.value)} className="p-2 rounded border border-amber-400 bg-dark-hard text-white">
          <option value="">انتخاب اکانت EA</option>
          {accounts.map(acc => (
            <option key={acc.id} value={acc.id}>{acc.name} ({acc.email})</option>
          ))}
        </select>
        <input type="number" placeholder="مبلغ" value={amount} onChange={e => setAmount(e.target.value)} className="p-2 rounded border border-amber-400 bg-dark-hard text-white w-24" />
        <button type="submit" className="bg-amber-400 text-dark-hard px-3 py-1 rounded shadow hover:bg-amber-500">انجام تراکنش</button>
      </form>
      {result && <div className="mt-2 text-white">{result}</div>}
      {usedAccount && (
        <div className="mt-4 p-2 bg-dark-soft rounded text-white">
          <div>اکانت استفاده شده: <b>{usedAccount.name}</b> ({usedAccount.email})</div>
          <div>پیشرفت روزانه: <b>{usedAccount.transferred_today}</b> / <b>{usedAccount.daily_limit || "GLOBAL"}</b></div>
        </div>
      )}
    </div>
  );
}

export default TestTransaction;
