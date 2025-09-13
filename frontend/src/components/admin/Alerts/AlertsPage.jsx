// src/components/admin/Alerts/AlertsPage.jsx
import React, { useEffect, useState, useCallback } from "react";
import {
  subscribeAlerts,
  startAlertsPoll,
  stopAlertsPoll,
} from "@/services/alerts/alerts";
import {
  resolveAlert,
  fetchResolvedAlerts,
} from "@/services/alerts/alerts-handlers";
import toast from "react-hot-toast";
import AlertItem from "./AlertItem";
import SolvedAlertsList from "./SolvedAlertsList";

const AlertsPage = () => {
  const [alerts, setAlerts] = useState([]);
  const [solvedAlerts, setSolvedAlerts] = useState([]);

  const refresh = useCallback((list) => {
    setAlerts(list || []);
  }, []);

  // گرفتن هشدارهای حل‌شده موقع mount شدن
  useEffect(() => {
    const loadResolved = async () => {
      try {
        const wholeAlerts = await fetchResolvedAlerts();
        setSolvedAlerts(wholeAlerts || []);
      } catch (err) {
        console.error("خطا در گرفتن هشدارهای حل‌شده:", err);
        toast.error("نتونستم هشدارهای حل‌شده رو بگیرم");
      }
    };

    loadResolved();
  }, []);

  useEffect(() => {
    // start polling when component mounts (idempotent)
    startAlertsPoll({ intervalMs: 3000 });
    const unsub = subscribeAlerts(refresh);
    return () => {
      unsub();
    };
  }, [refresh]);

  const onResolve = async (alertId) => {
    try {
      await resolveAlert(alertId);
      toast.success("حله کاکام!!! ارور پاک شد !!");
      // optimistic local update
      setAlerts((prev) => prev.filter((a) => String(a.id) !== String(alertId)));
    } catch (e) {
      console.error(e);
      toast.error("خطا هنگام برطرف کردن هشدار");
    }
  };

  return (
    <div className="p-4 glass-dark">
      <h2 className="text-xl font-bold mb-4 text-red-500">هشدارهای زنده</h2>
      {alerts.length === 0 && (
        <div className="text-green-600">هشدار فعالی وجود ندارد</div>
      )}
      <div className="space-y-3 mt-3">
        {alerts.map((a) => (
          <AlertItem
            key={a.id}
            alert={a}
            onResolve={() => onResolve(a.id)}
            resolved={a.raw.resolved}
          />
        ))}
      </div>
      <SolvedAlertsList solvedAlerts={solvedAlerts} />
    </div>
  );
};

export default AlertsPage;
