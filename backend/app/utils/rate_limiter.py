# app/utils/rate_limiter.py
import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict

class SimpleRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 5, per_seconds: int = 60):
        super().__init__(app)
        self.calls = calls
        self.per_seconds = per_seconds
        self.store = defaultdict(list)  # in-memory; replace with Redis for prod

    async def dispatch(self, request: Request, call_next):
        client = request.client.host if request.client else "unknown"
        now = time.time()
        window = now - self.per_seconds
        requests = [t for t in self.store[client] if t > window]
        requests.append(now)
        self.store[client] = requests
        if len(requests) > self.calls:
            raise HTTPException(status_code=429, detail="Too many requests")
        response = await call_next(request)
        return response
