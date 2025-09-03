// src/services/alerts.js
// سرویس مرکزی هشدارها — polling ساده + subscription + toast
import { fetchLiveAlerts } from "./eaAccountApi";
import toast from "react-hot-toast";

let _interval = null;
let _intervalMs = 3000;
let _subscribers = new Set();
let _seenIds = new Set();
let _lastAlerts = [];

async function _pollOnce() {
  try {
    const alerts = await fetchLiveAlerts();
    if (!Array.isArray(alerts)) return;
    // تبدیل به ساده‌شده (object) در صورت نیاز
    const normalized = alerts.map((a) => ({
      id:
        a.id ??
        a.ID ??
        `${a.player_id || "p"}_${a.platform || ""}_${a.created_at || ""}`,
      type: a.type || a.reason || "ERROR",
      message: a.message || a.reason || a.note || JSON.stringify(a),
      created_at: a.created_at || a.createdAt || a.created_at,
      raw: a,
    }));

    // پیدا کردن هشدارهای جدید (idهایی که قبلا ندیدیم)
    const newAlerts = normalized.filter((a) => !_seenIds.has(String(a.id)));
    if (newAlerts.length > 0) {
      // نشان دادن toast برای هر هشدار جدید
      newAlerts.forEach((a) => {
        const shortMsg = `${a.type}: ${String(a.message).slice(0, 120)}`;
        toast.error(
          ` اسو !  خطای جدید ! توی هشدار ها یه نگاهی بنداز`,
          {
            duration: 8000,
            style: {
              background: "red", // پس‌زمینه قرمز
              color: "white", // متن سفید
              padding: "12px 16px", // فاصله داخلی
              borderRadius: "8px", // گوشه‌های گرد
              boxShadow: "0 2px 10px rgba(0,0,0,0.3)", // سایه
            },
          }
        );
      });
    }

    // به‌روز کردن internal state
    normalized.forEach((a) => _seenIds.add(String(a.id)));
    _lastAlerts = normalized;

    // اطلاع به subscriberها
    _subscribers.forEach((cb) => {
      try {
        cb([..._lastAlerts]);
      } catch (e) {
        console.error("alerts subscriber error", e);
      }
    });
  } catch (e) {
    console.error("alerts poll failed", e);
  }
}

export function startAlertsPoll(opts = {}) {
  if (opts.intervalMs) _intervalMs = opts.intervalMs;
  if (_interval) return;
  // initial run
  _pollOnce();
  _interval = setInterval(_pollOnce, _intervalMs);
}

export function stopAlertsPoll() {
  if (_interval) {
    clearInterval(_interval);
    _interval = null;
  }
}

export function subscribeAlerts(cb) {
  _subscribers.add(cb);
  // immediately send current
  cb([..._lastAlerts]);
  return () => {
    _subscribers.delete(cb);
  };
}

export function getLastAlerts() {
  return [..._lastAlerts];
}

export function clearSeenIds() {
  _seenIds = new Set();
}
