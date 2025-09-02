# app/services/futbin_client.py
"""
Futbin client: async price fetcher with:
- Redis caching (short TTL: 3-4s)
- Concurrency semaphore (MAX_FUTBIN_CONCURRENCY)
- JSON endpoint try -> HTML fallback
- CAPTCHA / protection detection -> create alert (deduped) + negative-cache
- Exposes clear_negative_block() helper for admin resolve endpoint
"""

import asyncio
import json
import re
import time
import hashlib
import traceback
from datetime import datetime
from typing import Optional, Dict, Any

import httpx
from bs4 import BeautifulSoup

from app.cache import get_redis
from app.config import (
    FUTBIN_CACHE_TTL,
    FUTBIN_NEGATIVE_CACHE_SECONDS,
    FUTBIN_ALERT_DEDUPE_SECONDS,
    MAX_FUTBIN_CONCURRENCY,
    FUTBIN_USER_AGENT,
    INTERNAL_ALERT_POST_URL,
    USE_DISTRIBUTED_LOCK,
)

import logging

logger = logging.getLogger("app.futbin_client")


def _sanitize_sample(html: str, max_len: int = 4096) -> str:
    """
    Remove script tags and trim length to max_len to avoid storing huge or sensitive blobs.
    """
    try:
        # remove <script>...</script>
        clean = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.S | re.I)
        # optionally remove inline event handlers (onclick=...) - simple heuristic
        clean = re.sub(r'on\w+="[^"]*"', "", clean, flags=re.I)
        return clean[:max_len]
    except Exception:
        logger.exception("Failed to sanitize HTML sample")
        return (html or "")[:max_len]

# concurrency limiter across this process
RATE_SEMAPHORE = asyncio.Semaphore(int(MAX_FUTBIN_CONCURRENCY or 2))

DEFAULT_TTL = int(FUTBIN_CACHE_TTL or 3)
NEGATIVE_CACHE_SECONDS = int(FUTBIN_NEGATIVE_CACHE_SECONDS or 60)
ALERT_DEDUPE_SECONDS = int(FUTBIN_ALERT_DEDUPE_SECONDS or 120)
INTERNAL_ALERT_URL = INTERNAL_ALERT_POST_URL or None

FUTBIN_BASE = "https://www.futbin.com"
FIFA_YEAR = 25  # update if necessary
REQUEST_TIMEOUT = 8.0


async def _random_delay():
    # tiny random jitter to avoid strictly regular patterns
    await asyncio.sleep(0.2 + (0.3 * (time.time() % 1)))


def _parse_price_text(s: str) -> int:
    s = s.strip().upper().replace(",", "").replace(" ", "")
    m = re.match(r"^([0-9]*\.?[0-9]+)([KM])?$", s)
    if m:
        val = float(m.group(1))
        unit = m.group(2)
        if unit == "K":
            val *= 1_000
        elif unit == "M":
            val *= 1_000_000
        return int(val)
    digits = re.sub(r"[^\d]", "", s)
    if digits:
        return int(digits)
    raise ValueError(f"Cannot parse price from: {s}")


async def _fetch_html(client: httpx.AsyncClient, url: str) -> str:
    r = await client.get(url, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.text


async def _extract_price_from_html(html: str, platform: str) -> Optional[int]:
    soup = BeautifulSoup(html, "html.parser")

    # Heuristic #1: look for common span/class patterns (fragile, but fast)
    selectors = [
        f"span.{platform}",
        f"span.{platform}-price",
        ".player-price",
        ".price",  # fallback
    ]
    for sel in selectors:
        tag = soup.select_one(sel)
        if tag and tag.text.strip():
            try:
                return _parse_price_text(tag.text)
            except Exception:
                pass

    # Heuristic #2: extract JSON from inline scripts
    scripts = soup.find_all("script", {"type": "text/javascript"})
    for sc in scripts:
        txt = sc.string or sc.text or ""
        if "prices" in txt.lower() or "player_prices" in txt.lower():
            jmatch = re.search(r"(\{(?:.|\s){10,}\})", txt)
            if jmatch:
                try:
                    payload = json.loads(jmatch.group(1))
                    # try to find platform->player->price structure
                    def search_for_price(obj):
                        if isinstance(obj, dict):
                            for k, v in obj.items():
                                if k.lower() == platform and isinstance(v, (int, float, str)):
                                    try:
                                        return int(v)
                                    except:
                                        pass
                            for v in obj.values():
                                res = search_for_price(v)
                                if res:
                                    return res
                        return None
                    res = search_for_price(payload)
                    if res:
                        return int(res)
                except Exception:
                    pass

    # Heuristic #3: regex near platform keyword
    regex = re.compile(rf"{platform}[^0-9]{{0,10}}([0-9\.,KMkm]+)")
    m = regex.search(html)
    if m:
        try:
            return _parse_price_text(m.group(1))
        except Exception:
            pass

    return None


# ---------- Alert / negative-cache helpers ----------


def _alert_dedupe_key(player_id: str, platform: str) -> str:
    h = hashlib.sha1(f"{player_id}:{platform}".encode()).hexdigest()
    return f"futbin:alert:dedupe:{h}"


def _negative_block_key(player_id: str, platform: str) -> str:
    return f"futbin:negative:{player_id}:{platform}"


def _cache_key(player_id: str, platform: str) -> str:
    return f"futbin:price:{player_id}:{platform}"


def _dist_lock_name(player_id: str, platform: str) -> str:
    return f"futbin:lock:{player_id}:{platform}"


async def _create_alert_payload(player_id: str, platform: str, reason: str, sample: Optional[str] = None) -> Dict[str, Any]:
    return {
        "type": "futbin_fetch_problem",
        "title": f"Futbin fetch problem for player {player_id} ({platform})",
        "player_id": player_id,
        "platform": platform,
        "reason": reason,
        "sample": sample,
        "severity": "high",
        "created_at": datetime.utcnow().isoformat(),
    }


async def _create_alert(player_id: str, platform: str, reason: str, sample_html: Optional[str] = None):
    redis = await get_redis()
    dedupe_k = _alert_dedupe_key(player_id, platform)
    # try setnx to prevent duplicates
    set_succeeded = await redis.setnx(dedupe_k, "1")
    if set_succeeded:
        await redis.expire(dedupe_k, int(ALERT_DEDUPE_SECONDS))
    else:
        # already alerted recently
        return

    if sample_html:
        sample_html = _sanitize_sample(sample_html, max_len=4096)
    payload = await _create_alert_payload(player_id, platform, reason, sample_html)

    logger.info("Creating futbin alert", extra={"player_id": player_id, "platform": platform, "reason": reason})
    # Try to use project CRUD if available
    created = False
    try:
        # expected signature could vary; adapt if your project uses db session param
        from app.crud.alerts import create_alert as db_create_alert  # type: ignore
        # many projects expect db session first; if so adapt this call accordingly
        try:
            # try calling as single-arg payload
            await db_create_alert(payload)
            created = True
        except TypeError:
            # fallback: try calling with kwargs if function expects them
            await db_create_alert(**payload)
            created = True
    except Exception:
        # fallback: POST to INTERNAL_ALERT_URL if configured
        if INTERNAL_ALERT_URL:
            try:
                async with httpx.AsyncClient() as c:
                    await c.post(INTERNAL_ALERT_URL, json=payload, timeout=5.0)
                created = True
            except Exception:
                logger.exception("Failed to create alert via INTERNAL POST")
        else:
            logger.exception("Failed to create alert via CRUD and no INTERNAL_ALERT_POST_URL set")

    if created:
        logger.warning("Created futbin alert", extra={"player_id": player_id, "platform": platform, "reason": reason})

    # set negative-cache for short time to avoid retry storms
    neg_k = _negative_block_key(player_id, platform)
    try:
        await redis.set(neg_k, "1", ex=int(NEGATIVE_CACHE_SECONDS))
        logger.info("Set negative-cache for player", extra={"player_id": player_id, "platform": platform, "expires_in": NEGATIVE_CACHE_SECONDS})
    except Exception:
        pass


# ---------- Public API ----------


async def get_player_price(player_id: str, platform: str = "pc", ttl: Optional[int] = None) -> Dict[str, Any]:
    """
    Returns dict:
    {
       "player_id": str,
       "platform": str,
       "price": int | None,
       "cached": bool,
       "fetched_at": iso timestamp,
       "note": optional info
    }
    """
    ttl = int(ttl) if ttl is not None else int(DEFAULT_TTL)
    redis = await get_redis()
    cache_k = _cache_key(player_id, platform)
    neg_k = _negative_block_key(player_id, platform)

    # short-circuit if negative-block active
    if await redis.get(neg_k):
        return {"player_id": player_id, "platform": platform, "price": None, "cached": True, "fetched_at": datetime.utcnow().isoformat(), "note": "negative_block_active"}

    # Try cache
    cached = await redis.get(cache_k)
    if cached:
        try:
            obj = json.loads(cached)
            return {"player_id": player_id, "platform": platform, "price": obj.get("price"), "cached": True, "fetched_at": obj.get("fetched_at")}
        except Exception:
            pass

    # Try distributed lock first (if enabled), otherwise fall back to process-local semaphore
    if USE_DISTRIBUTED_LOCK:
        lock_name = _dist_lock_name(player_id, platform)
        try:
            # redis is already obtained above
            async with (await redis.lock(lock_name, timeout=10)):
                # double-check cache inside distributed lock to avoid stampede
                cached = await redis.get(cache_k)
                if cached:
                    try:
                        obj = json.loads(cached)
                        return {"player_id": player_id, "platform": platform, "price": obj.get("price"), "cached": True, "fetched_at": obj.get("fetched_at")}
                    except Exception:
                        pass

                await _random_delay()

                headers = {"User-Agent": FUTBIN_USER_AGENT, "Accept": "text/html,application/json"}

                async with httpx.AsyncClient(headers=headers) as client:
                    # try JSON-ish endpoint first (best-effort)
                    json_endpoint = f"{FUTBIN_BASE}/{FIFA_YEAR}/playerPrices?player={player_id}&platform={platform}"
                    try:
                        r = await client.get(json_endpoint, timeout=REQUEST_TIMEOUT)
                        if r.status_code == 200 and r.headers.get("content-type", "").lower().startswith("application/json"):
                            payload = r.json()
                            # attempt to find a price value
                            price = None
                            if isinstance(payload, dict):
                                if "prices" in payload and isinstance(payload["prices"], dict):
                                    maybe = payload["prices"].get(platform) or payload["prices"].get(platform.lower()) or payload["prices"].get(platform.upper())
                                    if isinstance(maybe, dict):
                                        price = maybe.get(str(player_id)) or maybe.get(int(player_id)) or None
                                    elif isinstance(maybe, (int, float, str)):
                                        price = maybe
                                # fallback: search for any int value
                                if price is None:
                                    def find_int(d):
                                        if isinstance(d, dict):
                                            for v in d.values():
                                                res = find_int(v)
                                                if res:
                                                    return res
                                        if isinstance(d, int):
                                            return d
                                        return None
                                    price = find_int(payload)
                            if price:
                                obj = {"price": int(price), "fetched_at": datetime.utcnow().isoformat()}
                                await redis.set(cache_k, json.dumps(obj), ex=ttl)
                                return {"player_id": player_id, "platform": platform, "price": int(price), "cached": False, "fetched_at": obj["fetched_at"]}

                        # handle protective status codes
                            if r.status_code in (403, 429):
                                sample = (r.text[:1200] if r.text else None)
                                logger.warning("Futbin protective response detected", extra={"player_id": player_id, "platform": platform, "status": r.status_code})
                                await _create_alert(player_id, platform, reason=f"http_{r.status_code}_protection", sample_html=sample)
                                return {"player_id": player_id, "platform": platform, "price": None, "cached": False, "fetched_at": datetime.utcnow().isoformat(), "note": f"http_{r.status_code}"}
                    except httpx.HTTPStatusError as e:
                        status = getattr(e.response, "status_code", None)
                        if status in (403, 429):
                            sample = (getattr(e.response, "text", "")[:1200] if getattr(e.response, "text", None) else None)
                            logger.warning("Futbin protective response detected (exception)", extra={"player_id": player_id, "platform": platform, "status": status})
                            await _create_alert(player_id, platform, reason=f"http_{status}_protection", sample_html=sample)
                            return {"player_id": player_id, "platform": platform, "price": None, "cached": False, "fetched_at": datetime.utcnow().isoformat(), "note": f"http_{status}"}
                        # else continue to HTML fallback
                    except Exception:
                        # swallow and fallback to HTML
                        pass

                    # HTML fallback
                    try:
                        url = f"{FUTBIN_BASE}/{FIFA_YEAR}/player/{player_id}"
                        html = await _fetch_html(client, url)
                        lower_html = html.lower()
                        captcha_indicators = ["captcha", "are you human", "g-recaptcha", "please verify", "cloudflare", "check if you are human"]
                        is_captcha = any(k in lower_html for k in captcha_indicators)
                        if is_captcha:
                            sample = html[:1200]
                            logger.warning("Captcha/protection detected on Futbin page", extra={"player_id": player_id, "platform": platform})
                            await _create_alert(player_id, platform, reason="captcha_or_protection_detected", sample_html=sample)
                            return {"player_id": player_id, "platform": platform, "price": None, "cached": False, "fetched_at": datetime.utcnow().isoformat(), "note": "captcha_detected"}

                        price = await _extract_price_from_html(html, platform)
                        obj = {"price": price, "fetched_at": datetime.utcnow().isoformat()}
                        await redis.set(cache_k, json.dumps(obj), ex=ttl)
                        return {"player_id": player_id, "platform": platform, "price": price, "cached": False, "fetched_at": obj["fetched_at"]}
                    except httpx.HTTPStatusError as e:
                        status = getattr(e.response, "status_code", None)
                        if status in (403, 429):
                            sample = (getattr(e.response, "text", "")[:1200] if getattr(e.response, "text", None) else None)
                            logger.warning("Futbin protective response detected (HTML fallback)", extra={"player_id": player_id, "platform": platform, "status": status})
                            await _create_alert(player_id, platform, reason=f"http_{status}_protection", sample_html=sample)
                            return {"player_id": player_id, "platform": platform, "price": None, "cached": False, "fetched_at": datetime.utcnow().isoformat(), "note": f"http_{status}"}
                        raise
                    except Exception as e:
                        # save a short negative-cache record so we don't retry immediately
                        try:
                            await redis.set(_negative_block_key(player_id, platform), "1", ex=5)
                        except Exception:
                            pass
                        logger.exception("Failed to fetch/parse futbin data for player %s platform %s", player_id, platform)
                        raise RuntimeError(f"Failed to fetch/parse futbin data: {e}") from e
        except Exception as e:
            logger.exception("Failed acquiring distributed lock, falling back to semaphore: %s", e)

    # fallback to local semaphore (original behavior)
    async with RATE_SEMAPHORE:
        # double-check cache inside semaphore to avoid stampede
        cached = await redis.get(cache_k)
        if cached:
            try:
                obj = json.loads(cached)
                return {"player_id": player_id, "platform": platform, "price": obj.get("price"), "cached": True, "fetched_at": obj.get("fetched_at")}
            except Exception:
                pass

        await _random_delay()

        headers = {"User-Agent": FUTBIN_USER_AGENT, "Accept": "text/html,application/json"}

        async with httpx.AsyncClient(headers=headers) as client:
            # try JSON-ish endpoint first (best-effort)
            json_endpoint = f"{FUTBIN_BASE}/{FIFA_YEAR}/playerPrices?player={player_id}&platform={platform}"
            try:
                r = await client.get(json_endpoint, timeout=REQUEST_TIMEOUT)
                if r.status_code == 200 and r.headers.get("content-type", "").lower().startswith("application/json"):
                    payload = r.json()
                    # attempt to find a price value
                    price = None
                    if isinstance(payload, dict):
                        if "prices" in payload and isinstance(payload["prices"], dict):
                            maybe = payload["prices"].get(platform) or payload["prices"].get(platform.lower()) or payload["prices"].get(platform.upper())
                            if isinstance(maybe, dict):
                                price = maybe.get(str(player_id)) or maybe.get(int(player_id)) or None
                            elif isinstance(maybe, (int, float, str)):
                                price = maybe
                        # fallback: search for any int value
                        if price is None:
                            def find_int(d):
                                if isinstance(d, dict):
                                    for v in d.values():
                                        res = find_int(v)
                                        if res:
                                            return res
                                if isinstance(d, int):
                                    return d
                                return None
                            price = find_int(payload)
                    if price:
                        obj = {"price": int(price), "fetched_at": datetime.utcnow().isoformat()}
                        await redis.set(cache_k, json.dumps(obj), ex=ttl)
                        return {"player_id": player_id, "platform": platform, "price": int(price), "cached": False, "fetched_at": obj["fetched_at"]}

                # handle protective status codes
                if r.status_code in (403, 429):
                    sample = (r.text[:1200] if r.text else None)
                    await _create_alert(player_id, platform, reason=f"http_{r.status_code}_protection", sample_html=sample)
                    return {"player_id": player_id, "platform": platform, "price": None, "cached": False, "fetched_at": datetime.utcnow().isoformat(), "note": f"http_{r.status_code}"}
            except httpx.HTTPStatusError as e:
                status = getattr(e.response, "status_code", None)
                if status in (403, 429):
                    sample = (getattr(e.response, "text", "")[:1200] if getattr(e.response, "text", None) else None)
                    await _create_alert(player_id, platform, reason=f"http_{status}_protection", sample_html=sample)
                    return {"player_id": player_id, "platform": platform, "price": None, "cached": False, "fetched_at": datetime.utcnow().isoformat(), "note": f"http_{status}"}
                # else continue to HTML fallback
            except Exception:
                # swallow and fallback to HTML
                pass

            # HTML fallback
            try:
                url = f"{FUTBIN_BASE}/{FIFA_YEAR}/player/{player_id}"
                html = await _fetch_html(client, url)
                lower_html = html.lower()
                captcha_indicators = ["captcha", "are you human", "g-recaptcha", "please verify", "cloudflare", "check if you are human"]
                is_captcha = any(k in lower_html for k in captcha_indicators)
                if is_captcha:
                    sample = html[:1200]
                    await _create_alert(player_id, platform, reason="captcha_or_protection_detected", sample_html=sample)
                    return {"player_id": player_id, "platform": platform, "price": None, "cached": False, "fetched_at": datetime.utcnow().isoformat(), "note": "captcha_detected"}

                price = await _extract_price_from_html(html, platform)
                obj = {"price": price, "fetched_at": datetime.utcnow().isoformat()}
                await redis.set(cache_k, json.dumps(obj), ex=ttl)
                return {"player_id": player_id, "platform": platform, "price": price, "cached": False, "fetched_at": obj["fetched_at"]}
            except httpx.HTTPStatusError as e:
                status = getattr(e.response, "status_code", None)
                if status in (403, 429):
                    sample = (getattr(e.response, "text", "")[:1200] if getattr(e.response, "text", None) else None)
                    await _create_alert(player_id, platform, reason=f"http_{status}_protection", sample_html=sample)
                    return {"player_id": player_id, "platform": platform, "price": None, "cached": False, "fetched_at": datetime.utcnow().isoformat(), "note": f"http_{status}"}
                raise
            except Exception as e:
                # save a short negative-cache record so we don't retry immediately
                try:
                    await redis.set(_negative_block_key(player_id, platform), "1", ex=5)
                except Exception:
                    pass
                raise RuntimeError(f"Failed to fetch/parse futbin data: {e}") from e


async def clear_negative_block(player_id: str, platform: str):
    """
    Admin helper: remove negative block so next request will try fetch again.
    """
    redis = await get_redis()
    await redis.delete(_negative_block_key(player_id, platform))
