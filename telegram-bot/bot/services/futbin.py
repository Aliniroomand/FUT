# bot/services/futbin.py
# -*- coding: utf-8 -*-
"""
سرویس ارتباط با Futbin با کش داخلی + نرخ‌دهی درخواست‌ها.
- از proxy.requests_get استفاده می‌کنیم تا همهٔ تنظیمات پراکسی/timeout یک‌جا باشد.
- کش ساده درون‌حافظه‌ای با TTL: برای قیمت‌ها 5 دقیقه، برای تصویرها 24 ساعت.
- نرخ‌دهی: حداکثر ~5 درخواست در دقیقه به صورت جهانی + تأخیر تصادفی بین 0.8 تا 1.6 ثانیه.
توجه: ساختار APIهای Futbin ممکن است تغییر کند؛ در صورت تغییر لازم است parsing به‌روز شود.
"""
from __future__ import annotations
import time
import json
import threading
import random
import logging
from collections import deque
from typing import Optional, Dict, Any

from bot.proxy import requests_get  # session تنظیم‌شده
from bot.config import settings

logger = logging.getLogger(__name__)

# ---------------- Cache ----------------
class _TTLCache:
    def __init__(self, ttl_seconds: int):
        self.ttl = ttl_seconds
        self._data: Dict[str, Any] = {}
        self._exp: Dict[str, float] = {}
        self._lock = threading.Lock()

    def get(self, key: str):
        now = time.time()
        with self._lock:
            exp = self._exp.get(key, 0)
            if exp and now < exp:
                return self._data.get(key)
            if key in self._data:
                # expired
                self._data.pop(key, None)
                self._exp.pop(key, None)
        return None

    def set(self, key: str, value: Any):
        with self._lock:
            self._data[key] = value
            self._exp[key] = time.time() + self.ttl

_price_cache = _TTLCache(ttl_seconds=300)   # 5 دقیقه
_image_cache = _TTLCache(ttl_seconds=86400) # 24 ساعت

# --------------- Rate-limit ---------------
_rl_lock = threading.Lock()
_rl_q = deque()  # timestamps of last requests
_RL_MAX_PER_MIN = 5

def _allow_request() -> bool:
    """حداکثر _RL_MAX_PER_MIN درخواست در 60 ثانیه."""
    now = time.time()
    with _rl_lock:
        while _rl_q and now - _rl_q[0] > 60.0:
            _rl_q.popleft()
        if len(_rl_q) < _RL_MAX_PER_MIN:
            _rl_q.append(now)
            return True
        return False

def _polite_delay():
    time.sleep(random.uniform(0.8, 1.6))

# --------------- Helpers ---------------
def _get_json(url: str, timeout: int = 10) -> Optional[dict]:
    try:
        resp = requests_get(url, timeout=timeout, headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json,text/plain,*/*",
        })
        if getattr(resp, "status_code", None) == 200:
            try:
                return resp.json()
            except Exception:
                return json.loads(getattr(resp, "text", "") or "{}")
        else:
            logger.warning("futbin GET %s -> %s", url, getattr(resp, "status_code", None))
            return None
    except Exception as exc:
        logger.exception("futbin GET failed url=%s err=%s", url, exc)
        return None

# --------------- Public API ---------------
def get_player_price(player_id: int) -> Optional[int]:
    """
    تلاش برای دریافت قیمت تقریبی خرید (Buy Now / Lowest). اگر موفق نشد، None.
    کش و rate-limit رعایت می‌شود.
    """
    key = f"price:{player_id}"
    cached = _price_cache.get(key)
    if cached is not None:
        return cached

    if not _allow_request():
        logger.info("futbin price denied by ratelimiter")
        return cached  # ممکنه None باشه؛ handler باید fallback داشته باشه

    _polite_delay()
    # نمونهٔ یکی از endpointها؛ ممکن است لازم شود تغییرش دهید
    url = f"https://www.futbin.com/24/playerPrices?player={player_id}"
    data = _get_json(url, timeout=12)
    price = None
    try:
        # ساختار رایج: {'LCPrice': '123,000', ...} یا در prices['ps'] / ['xbox'] ...
        if not data:
            price = None
        elif isinstance(data, dict) and "LCPrice" in data:
            raw = str(data.get("LCPrice", "")).replace(",", "").strip()
            price = int(raw) if raw.isdigit() else None
        elif isinstance(data, dict) and "prices" in data:
            # برداشتن یک پلتفرم (مثلاً ps)
            for plat in ("ps", "ps4", "ps5", "xbox", "pc"):
                p = data["prices"].get(plat) if isinstance(data["prices"], dict) else None
                if p and "LCPrice" in p:
                    raw = str(p.get("LCPrice", "")).replace(",", "").strip()
                    if raw.isdigit():
                        price = int(raw)
                        break
    except Exception:
        logger.exception("parse futbin price failed for player=%s", player_id)
        price = None

    if price is not None:
        _price_cache.set(key, price)
    return price

def get_player_image_url(player_id: int) -> Optional[str]:
    """
    URL تصویر کارت بازیکن را برمی‌گرداند (کش‌شده). اگر به هر دلیل نتوانستیم، None.
    """
    key = f"img:{player_id}"
    cached = _image_cache.get(key)
    if cached is not None:
        return cached

    # چند مسیر معمول در futbin/cdn
    candidates = [
        f"https://cdn.futbin.com/content/fifa24/img/players/{player_id}.png",
        f"https://www.futbin.com/images/players/{player_id}.png",
    ]
    # اینجا درخواست واقعی نمی‌زنیم؛ فقط URL می‌دهیم و تلگرام خودش لود می‌کند.
    # اگر خواستید صحت URL را چک کنید، می‌توانید HEAD بزنید (اما ریسک rate-limit دارد).
    url = candidates[0]
    _image_cache.set(key, url)
    return url
