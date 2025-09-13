// src/services/alerts.js  (پچ پیشنهادی)
import { fetchUnresolvedAlerts } from "./alerts-handlers";
import toast from "react-hot-toast";
let _interval = null;
let _intervalMs = 10000; // پیش‌فرض 10s — قابل override در startAlertsPoll
let _subscribers = new Set();
let _seenIds = new Set();
let _lastAlerts = [];
let _isRunning = false;
let _consecutiveErrors = 0;
const MAX_ERRORS_BEFORE_BACKOFF = 3;
const MAX_BACKOFF_MS = 60000;

async function _pollOnce() {
  if (_isRunning) return; // جلوگیری از poll موازی
  _isRunning = true;
  try {
    const alerts = await fetchUnresolvedAlerts();
    if (!Array.isArray(alerts)) {
      _isRunning = false;
      return;
    }

    // نرمال‌سازی و تبدیل created_at به Date برای مرتب‌سازی
    const normalized = alerts
      .map((a) => {
        const id = a.id ?? a.ID ?? `${a.player_id || "p"}_${a.platform || ""}_${a.created_at || ""}`;
        const created_at = a.created_at ?? a.createdAt ?? null;
        return {
          id: String(id),
          type: a.type || a.reason || "ERROR",
          message: a.message || a.reason || a.note || JSON.stringify(a),
          created_at,
          raw: a,
        };
      })
      .sort((x, y) => {
        const dx = x.created_at ? new Date(x.created_at).getTime() : 0;
        const dy = y.created_at ? new Date(y.created_at).getTime() : 0;
        return dy - dx;
      });

    // find new alerts
    const newAlerts = normalized.filter((a) => !_seenIds.has(String(a.id)));

    if (newAlerts.length > 0) {
      // اگر فقط یک هشدار جدید است، آن را جدا نمایش بده؛ در غیر این صورت یک خلاصه بده
      if (newAlerts.length === 1) {
        const a = newAlerts[0];
        toast.error(`${a.type}: ${String(a.message).slice(0, 120)}`, { duration: 8000 });
      } else {
        toast.error(`⚠️ ${newAlerts.length} هشدار جدید دریافت شد. برای جزئیات به بخش هشدارها بروید.`, {
          duration: 8000,
        });
      }
    }

    // update seen ids (در اینجا تنظیم ساده: همهٔ هشدارهای فعلی را به seen اضافه می‌کنیم)
    normalized.forEach((a) => _seenIds.add(String(a.id)));

    // update last alerts and notify subscribers
    _lastAlerts = normalized;
    _subscribers.forEach((cb) => {
      try {
        cb([..._lastAlerts]);
      } catch (e) {
        console.error("alerts subscriber error", e);
      }
    });

    // reset error counter on success
    _consecutiveErrors = 0;
  } catch (e) {
    console.error("alerts poll failed", e);
    _consecutiveErrors += 1;

    // ساده: اگر چند خطای متوالی داشتیم، backoff انجام بدهیم
    if (_consecutiveErrors >= MAX_ERRORS_BEFORE_BACKOFF) {
      // دو برابر کردن interval (تا max) و ری‌استارت interval
      const newMs = Math.min((_intervalMs || 10000) * 2, MAX_BACKOFF_MS);
      try {
        if (_interval) {
          clearInterval(_interval);
        }
        _interval = setInterval(_pollOnce, newMs);
      } catch (err) {
        console.error("failed to backoff alerts poll", err);
      }
    }
  } finally {
    _isRunning = false;
  }
}

export function startAlertsPoll(opts = {}) {
  if (opts.intervalMs) {
    _intervalMs = opts.intervalMs;
  }
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
  try {
    cb([..._lastAlerts]);
  } catch (e) {
    console.error("alerts subscriber cb failed on add", e);
  }
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
