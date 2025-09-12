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
import requests
import asyncio
import re
import unicodedata
from bot.services.backend_client import get_player_card_meta, get_futbin_price_from_backend


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
        if resp.status_code == 200:
                try:
                        return resp.json()
                except Exception:
                        return json.loads(resp.text or "{}")
        else:
                logger.warning("futbin GET %s -> %s", url, resp.status_code)
                return None
    except Exception as exc:
        logger.exception("futbin GET failed url=%s err=%s", url, exc)
        return None

# --------------- Public API ---------------

# local slugify (مطابق backend)
def _slugify(name: str) -> str:
    s = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9\s-]", "", s).strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return s

# public async API that other modules await
async def get_price_for_player(player_id: int, platform: str = "console") -> Optional[int]:
    """Async: return integer price or None. Uses backend /futbin/price as primary source."""
    key = f"price:{player_id}"
    cached = _price_cache.get(key)
    if cached is not None:
        return cached

    # rate-limit check (local)
    if not _allow_request():
        logger.info("futbin price denied by ratelimiter")
        return cached  # maybe None

    # first: get player meta from backend to build slug
    try:
        player = await get_player_card_meta(player_id)
    except Exception as exc:
        logger.exception("Failed to get player meta for futbin price: %s", exc)
        player = None

    slug = _slugify(player.get("name", "")) if player else str(player_id)

    # call backend futbin endpoint (backend does actual scraping/parsing)
    try:
        res = await get_futbin_price_from_backend(player_id, slug, platform)
        print("qqqqqqqqqqq:",res)
    except Exception as exc:
        logger.exception("call to backend /futbin/price failed for player=%s: %s", player_id, exc)
        return None

    # backend returns {"player_id":..., "platform":..., "price": "<text>"...}
    price_val = res.get("price")
    if not price_val:
        return None

    # normalize price string -> int (e.g. "123,000" -> 123000)
    raw = str(price_val).replace(",", "").strip()
    # sometimes backend may return extra chars, try to extract digits
    digits = re.findall(r"\d+", raw)
    if not digits:
        return None
    price = int("".join(digits))

    _price_cache.set(key, price)
    return price
