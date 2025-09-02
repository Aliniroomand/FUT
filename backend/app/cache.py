"""Redis connection helpers.

Provides an async get_redis() helper that returns a singleton
redis.asyncio.Redis client. Safe to call concurrently from multiple
coroutines thanks to an asyncio.Lock.
"""
import os
import asyncio
import redis.asyncio as aioredis  # requires redis>=4.x

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
# module-level singleton
_redis_client: aioredis.Redis | None = None
_redis_lock = asyncio.Lock()


async def get_redis() -> aioredis.Redis:
    """
    Return a singleton async Redis client (redis.asyncio.Redis).
    Safe to call concurrently.
    """
    global _redis_client
    if _redis_client is None:
        async with _redis_lock:
            if _redis_client is None:
                # from_url returns a Redis instance (not a coroutine)
                _redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)
    return _redis_client


async def close_redis():
    global _redis_client
    if _redis_client is not None:
        try:
            await _redis_client.close()
        except Exception:
            pass
        _redis_client = None
