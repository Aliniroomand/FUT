// src/components/admin/Alerts/AlertsPage.jsx
import React, { useEffect, useState, useCallback } from "react";
import { subscribeAlerts, startAlertsPoll, stopAlertsPoll } from "@/services/alerts";
import { resolveAlert } from "@/services/eaAccountApi";
import toast from "react-hot-toast";
import AlertItem from "./AlertItem";

const AlertsPage = () => {
  const [alerts, setAlerts] = useState([]);
  const refresh = useCallback((list) => {
    setAlerts(list || []);
  }, []);

  useEffect(() => {
    // start polling when component mounts (idempotent)
    startAlertsPoll({ intervalMs: 3000 });
    const unsub = subscribeAlerts(refresh);
    return () => {
      unsub();
      // do NOT stop global poll here — keep it running app-wide if you prefer
      // stopAlertsPoll();
    };
  }, [refresh]);

  const onResolve = async (alertId) => {
    try {
      await resolveAlert(alertId);
      toast.success("حله کاکام!!! ارور پاک شد !!");
      // optimistic local update
      setAlerts(prev => prev.filter(a => String(a.id) !== String(alertId)));
    } catch (e) {
      console.error(e);
      toast.error("خطا هنگام برطرف کردن هشدار");
    }
  };

  return (

    <div className="p-4 glass-dark">
      <h2 className="text-xl font-bold mb-4 text-amber-500">هشدارهای زنده</h2>
      {alerts.length === 0 && <div className="text-green-600">هشدار فعالی وجود ندارد</div>}
      <div className="space-y-3 mt-3">
        {alerts.map(a => (
          <AlertItem key={a.id} alert={a} onResolve={() => onResolve(a.id)} />
        ))}
      </div>
    </div>
  );
};

export default AlertsPage;
