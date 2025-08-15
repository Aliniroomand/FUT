import React, { useEffect, useState, useCallback } from "react";
import {
  connectEAWebSocket,
  subscribeEAUpdates,
  disconnectEAWebSocket,
} from "@/services/eaWebSocketService"; // مسیر رو متناسب با پروژه‌ات بذار

const alertColor = {
  CAPTCHA: "bg-red-100 border-red-400 text-red-700",
  RATE_LIMIT: "bg-yellow-100 border-yellow-400 text-yellow-700",
  ERROR: "bg-orange-100 border-orange-400 text-orange-700",
};

const LiveAlertsAndPendingTxs = () => {
  const [alerts, setAlerts] = useState([]);

  // بهینه‌سازی با useCallback تا رندر اضافی نداشته باشیم
  const handleIncomingData = useCallback((data) => {
    if (data.alerts && Array.isArray(data.alerts)) {
      // فقط اگر تغییر کرده آپدیت کن
      setAlerts((prev) => {
        const same =
          prev.length === data.alerts.length &&
          prev.every((a, i) => a.id === data.alerts[i].id);
        return same ? prev : data.alerts;
      });
    }
  }, []);

  useEffect(() => {
    connectEAWebSocket();
    subscribeEAUpdates(handleIncomingData);
    return () => {
      disconnectEAWebSocket();
    };
  }, [handleIncomingData]);

  const filteredAlerts = alerts.filter((a) =>
    ["CAPTCHA", "RATE_LIMIT", "ERROR"].includes(a.type)
  );

  return (
    filteredAlerts.length > 0 && (
      <div className="fixed bottom-0 left-0 w-full bg-black/80 border-t border-gray-700 z-50">
        <div className="flex overflow-x-auto no-scrollbar text-sm">
          {filteredAlerts.map((alert, idx) => (
            <div
              key={alert.id || idx}
              className={`flex-shrink-0 px-4 py-2 border-r border-gray-600 whitespace-nowrap text-white font-medium ${alertColor[alert.type]}`}
            >
              {alert.type}: {alert.message}
            </div>
          ))}
        </div>
      </div>
    )
  );
};

export default LiveAlertsAndPendingTxs;
