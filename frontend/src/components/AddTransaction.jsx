import React, { useState, useEffect } from "react";
import { getTransactions, createTransaction } from "@/services/transactions";

const AddTransacton = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getTransactions();
      setTransactions(data || []);
    } catch (err) {
      console.error(err);
      setError(err.message || "خطا در دریافت تراکنش‌ها");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTransaction = async () => {
    setCreating(true);
    setError(null);
    try {
      const randomAmount = Math.floor(Math.random() * 1000) + 1; // عدد رندوم
      const randomSuccess = Math.random() < 0.5 ? 1 : 0;
      const randomSettled = Math.random() < 0.5 ? 1 : 0;
      const randomDebt = Math.floor(Math.random() * 500) + 1;

      // این مقادیر باید از اطلاعات کاربر و admin prices گرفته شوند
      const currentUser = { id: 1, phone: "09120000000", email: "test@example.com" };
      const adminPrices = { buy_price: 4500 }; // فرضی، در عمل باید از API بگیری

      const newTransaction = {
        user_id: currentUser.id,
        card_id: 1,
        transfer_method_id: 1,
        amount: randomAmount,
        transaction_type: "sell",
        is_successful: randomSuccess,
        is_settled: randomSettled,
        buy_price: adminPrices.buy_price,
        sell_price: null,
        customer_phone: currentUser.phone,
        customer_email: currentUser.email,
        debt_or_credit: randomDebt,
        debt_or_credit_type: "debt",
        transfer_multiplier: 1.9,
        
      };

      const created = await createTransaction(newTransaction);
      setTransactions((prev) => [created, ...prev]);
    } catch (err) {
      console.error(err);
      setError(err.message || "خطا در ایجاد تراکنش");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div>
      <h1>Transactions</h1>
      <button className="bg-red-400 w-svw" onClick={handleCreateTransaction} disabled={creating}>
        {creating ? "در حال ایجاد..." : "ایجاد تراکنش جدید"}
      </button>
      {loading && <div>Loading...</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}
      <ul>
        {transactions.map((t) => (
          <li key={t.id}>
            {t.customer_email || t.customer_phone} — {t.amount} — {t.transaction_type}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AddTransacton;
