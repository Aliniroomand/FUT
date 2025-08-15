import React, { useEffect, useState } from "react";
import { fetchLiveAlerts, fetchPendingTransactions, resolveAlert } from "../../../services/eaAccountApi";

const alertColor = {
  CAPTCHA: "bg-red-100 border-red-400 text-red-700",
  RATE_LIMIT: "bg-yellow-100 border-yellow-400 text-yellow-700",
  ERROR: "bg-orange-100 border-orange-400 text-orange-700",
};

const LiveAlertsAndPendingTxs = () => {
  const [alerts, setAlerts] = useState([]);
  const [pendingTxs, setPendingTxs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchLiveAlerts().then(setAlerts);
    fetchPendingTransactions().then(setPendingTxs);
    const interval = setInterval(() => {
      fetchLiveAlerts().then(setAlerts);
      fetchPendingTransactions().then(setPendingTxs);
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleResolveAlert = async (alertId) => {
    setLoading(true);
    try {
      await resolveAlert(alertId);
      fetchLiveAlerts().then(setAlerts);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-dark-soft p-4 rounded shadow mt-8 max-w-4xl mx-auto">
      <h3 className="text-md font-bold mb-2 text-amber-400">هشدارهای لحظه‌ای</h3>
      <ul className="space-y-2">
        {alerts?.map((alert) => (
          <li key={alert.id} className={`border-l-4 p-3 rounded flex items-center justify-between ${alertColor[alert.type] || "bg-gray-100 border-gray-400 text-gray-700"}`}>
            <span>{alert.message}</span>
            <span className="mx-2 text-xs">({alert.type})</span>
            <button onClick={() => handleResolveAlert(alert.id)} className="bg-amber-400 text-dark-hard px-2 py-1 rounded shadow hover:bg-amber-500">حل هشدار</button>
          </li>
        ))}
      </ul>
      <h3 className="text-md font-bold mt-8 mb-2 text-amber-400">تراکنش‌های در حال انجام</h3>
      <ul className="space-y-2">
        {pendingTxs?.map((tx) => (
          <li key={tx.id} className="bg-dark-soft p-2 rounded flex gap-4 items-center text-white">
            <span>اکانت: <span className="font-bold text-amber-400">{tx.account_id}</span></span>
            <span>کاربر: {tx.user_id}</span>
            <span>مبلغ: {tx.amount}</span>
            <span>وضعیت: <span className="font-bold text-amber-400">{tx.status}</span></span>
          </li>
        ))}
      </ul>
      {error && <div className="text-red-500 mt-4">{error}</div>}
    </div>
  );
};

export default LiveAlertsAndPendingTxs;
 

