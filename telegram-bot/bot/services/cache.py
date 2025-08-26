"""Caching foundation with Redis fallback.

Behavior:
- If REDIS_URL env var is set and redis-py is importable, use Redis client.
- Else use a simple in-memory dict with TTL and thread-safety.

Exposes:
- get(key) -> Any|None
- set(key, value, ttl_sec) -> None
- delete(key) -> None
- ttl(key) -> int|-1
- cached(ttl_sec): decorator

Notes:
- Values stored in Redis are JSON serialized.
- Uses APP_CACHE_PREFIX env var (default "bot:cache:") as key prefix.
- On any Redis error operations fall back to in-memory store.
"""
from __future__ import annotations

import os
import json
import time
import threading
import functools
import inspect
import logging
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)

REDIS_URL = os.environ.get("REDIS_URL")
APP_CACHE_PREFIX = os.environ.get("APP_CACHE_PREFIX", "bot:cache:")

_redis_client = None
_use_redis = False

# In-memory store: key -> (value, expire_at)
_memory_store: dict[str, tuple[Any, Optional[float]]] = {}
_memory_lock = threading.Lock()

# Try to initialize redis client if url provided and redis package available
if REDIS_URL:
    try:
        import redis

        _redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        # Quick ping to verify connectivity
        try:
            _redis_client.ping()
            _use_redis = True
        except Exception as exc:  # pragma: no cover - runtime environment specific
            logger.warning("redis ping failed, falling back to in-memory cache: %s", exc)
            _redis_client = None
            _use_redis = False
    except Exception as exc:  # includes ImportError
        logger.warning("redis not available or failed to init, using in-memory cache: %s", exc)
        _redis_client = None
        _use_redis = False


def _prefixed(key: str) -> str:
    return f"{APP_CACHE_PREFIX}{key}"


def _now() -> float:
    return time.time()


def _memory_get(key: str) -> Any | None:
    with _memory_lock:
        entry = _memory_store.get(key)
        if not entry:
            return None
        value, expire_at = entry
        if expire_at is not None and _now() > expire_at:
            # expired
            _memory_store.pop(key, None)
            return None
        return value


def _memory_set(key: str, value: Any, ttl_sec: Optional[int]) -> None:
    expire_at = None if ttl_sec is None or ttl_sec <= 0 else _now() + ttl_sec
    with _memory_lock:
        _memory_store[key] = (value, expire_at)


def _memory_delete(key: str) -> None:
    with _memory_lock:
        _memory_store.pop(key, None)


def _memory_ttl(key: str) -> int:
    with _memory_lock:
        entry = _memory_store.get(key)
        if not entry:
            return -1
        _, expire_at = entry
        if expire_at is None:
            return -1
        remaining = int(expire_at - _now())
        return remaining if remaining > 0 else -1


# Public API

def get(key: str) -> Any | None:
    pkey = _prefixed(key)
    if _use_redis and _redis_client is not None:
        try:
            raw = _redis_client.get(pkey)
            if raw is None:
                return None
            try:
                return json.loads(raw)
            except Exception:
                # fallback: return raw string
                return raw
        except Exception as exc:
            logger.warning("redis get failed, falling back to memory: %s", exc)
            # fallthrough to memory fallback
    return _memory_get(pkey)


def set(key: str, value: Any, ttl_sec: int | None = None) -> None:
    pkey = _prefixed(key)
    if _use_redis and _redis_client is not None:
        try:
            raw = json.dumps(value, default=str)
            if ttl_sec and ttl_sec > 0:
                _redis_client.setex(pkey, int(ttl_sec), raw)
            else:
                _redis_client.set(pkey, raw)
            return
        except Exception as exc:
            logger.warning("redis set failed, falling back to memory: %s", exc)
    _memory_set(pkey, value, ttl_sec)


def delete(key: str) -> None:
    pkey = _prefixed(key)
    if _use_redis and _redis_client is not None:
        try:
            _redis_client.delete(pkey)
            return
        except Exception as exc:
            logger.warning("redis delete failed, falling back to memory: %s", exc)
    _memory_delete(pkey)


def ttl(key: str) -> int:
    pkey = _prefixed(key)
    if _use_redis and _redis_client is not None:
        try:
            remaining = _redis_client.ttl(pkey)
            # redis returns -2 if key doesn't exist, -1 if exists without timeout
            if remaining is None:
                return -1
            return int(remaining)
        except Exception as exc:
            logger.warning("redis ttl failed, falling back to memory: %s", exc)
    return _memory_ttl(pkey)


def _make_cache_key(func: Callable, args: tuple, kwargs: dict) -> str:
    name = f"{func.__module__}.{func.__qualname__}"
    try:
        payload = {"args": args, "kwargs": kwargs}
        key_body = json.dumps(payload, default=str, sort_keys=True)
    except Exception:
        # fallback to repr
        key_body = repr((args, kwargs))
    return f"{name}:{key_body}"


def cached(ttl_sec: int) -> Callable:
    """Decorator to cache function result keyed by function name + args.

    Works for sync and async functions.
    """

    def decorator(func: Callable) -> Callable:
        is_coro = inspect.iscoroutinefunction(func)

        if is_coro:
            async def async_wrapper(*args, **kwargs):
                key = _make_cache_key(func, args, kwargs)
                existing = get(key)
                if existing is not None:
                    return existing
                result = await func(*args, **kwargs)
                try:
                    set(key, result, ttl_sec)
                except Exception as exc:
                    logger.warning("cache set failed: %s", exc)
                return result

            return functools.update_wrapper(async_wrapper, func)

        else:
            def sync_wrapper(*args, **kwargs):
                key = _make_cache_key(func, args, kwargs)
                existing = get(key)
                if existing is not None:
                    return existing
                result = func(*args, **kwargs)
                try:
                    set(key, result, ttl_sec)
                except Exception as exc:
                    logger.warning("cache set failed: %s", exc)
                return result

            return functools.update_wrapper(sync_wrapper, func)

    return decorator
