# app/utils/rate_limiter.py
import time
from fastapi import HTTPException, Request, Depends
from collections import defaultdict

store = defaultdict(list)

def rate_limit(calls: int = 5, per_seconds: int = 60):
    async def limiter(request: Request):
        client_host = request.client.host if request.client else "unknown"
        now = time.time()
        window = now - per_seconds

        # فقط درخواست‌های داخل بازه‌ی زمانی رو نگه دار
        requests = [t for t in store[client_host] if t > window]
        requests.append(now)
        store[client_host] = requests

        if len(requests) > calls:
            raise HTTPException(status_code=429, detail="Too many requests")

    return limiter
