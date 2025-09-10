# backend/app/utils/rate_limiter.py
import os
import time
from typing import Callable, Optional, Set, Tuple
from uuid import uuid4

from fastapi import HTTPException, Request
from redis.asyncio import Redis

# ------------------------------
# Redis client (config via env)
# ------------------------------
# پشتیبانی از REDIS_URL یا مشخصات جدا
REDIS_URL = os.getenv("REDIS_URL")
if REDIS_URL:
    redis = Redis.from_url(REDIS_URL, decode_responses=True)
else:
    REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))
    redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

# ------------------------------
# Core sliding-window check
# ------------------------------
async def is_allowed(key: str, limit: int, window_seconds: int) -> bool:
    """
    Sliding window با ZSET:
      - هر درخواست: score=timestamp_ms؛ member یکتا برای جلوگیری از collision
      - پاکسازی رکوردهای قدیمی‌تر از window
      - اگر count >= limit => block
    """
    now_ms = int(time.time() * 1000)
    window_start_ms = now_ms - window_seconds * 1000

    pipe = redis.pipeline()
    # حذف رویدادهای قدیمی
    pipe.zremrangebyscore(key, 0, window_start_ms)
    # شمارش فعلی
    pipe.zcard(key)
    res = await pipe.execute()
    current_count = int(res[1])

    if current_count >= limit:
        return False

    # ثبت درخواست فعلی و TTL
    member = f"{now_ms}-{uuid4()}"
    pipe = redis.pipeline()
    pipe.zadd(key, {member: now_ms})
    # TTL را حداقل به طول پنجره نگه داریم (ثانیه)
    pipe.expire(key, window_seconds)
    await pipe.execute()
    return True

# ------------------------------
# Identifier helpers
# ------------------------------
def _default_identifier(request: Request) -> str:
    """
    ترتیب تشخیص هویت برای rate limiting:
      1) X-API-Key
      2) X-User-Id (برای ربات/کلاینت‌ داخلی)
      3) Authorization (token hash یا خام)
      4) fallback: client IP
    """
    headers = request.headers
    api_key = headers.get("x-api-key")
    if api_key:
        return f"api:{api_key}"

    user_id = headers.get("x-user-id")
    if user_id:
        return f"user:{user_id}"

    auth = headers.get("authorization")
    if auth:
        return f"auth:{auth}"

    host = request.client.host if request.client else "unknown"
    return f"ip:{host}"

# ------------------------------
# Dependency factory
# ------------------------------
def rate_limiter(
    limit: int,
    window_seconds: int,
    namespace: str = "rl",
    identify: Optional[Callable[[Request], str]] = None,
    whitelist: Optional[Set[str]] = None,
):
    """
    استفاده:
      rl_dep = rate_limiter(limit=5, window_seconds=1, namespace="player.fetch")
      @router.get(..., dependencies=[Depends(rl_dep)])
    """
    identify = identify or _default_identifier
    whitelist = whitelist or set()

    async def _dep(request: Request):
        ident = identify(request)
        if ident in whitelist:
            return

        key = f"{namespace}:{ident}"
        allowed = await is_allowed(key, limit=limit, window_seconds=window_seconds)
        if not allowed:
            # حداقل هدرهای مفید برای کلاینت‌ها
            raise HTTPException(
                status_code=429,
                detail="Too Many Requests",
                headers={
                    # ساده: به اندازه‌ی طول پنجره پیشنهاد صبر بده
                    "Retry-After": str(max(1, int(window_seconds))),
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Window": str(window_seconds),
                },
            )

    return _dep


