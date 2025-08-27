"""
Simple per-user rate limiter for buy requests.
Limits: max 5 buy requests per 10 minutes.
Developer note: No backend endpoint, local only.
"""
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests=5, window_sec=600):
        self.max_requests = max_requests
        self.window_sec = window_sec
        self.user_timestamps = defaultdict(list)

    def is_allowed(self, user_id):
        now = time.time()
        timestamps = self.user_timestamps[user_id]
        # Remove old timestamps
        self.user_timestamps[user_id] = [t for t in timestamps if now - t < self.window_sec]
        if len(self.user_timestamps[user_id]) < self.max_requests:
            self.user_timestamps[user_id].append(now)
            return True
        return False

rate_limiter = RateLimiter()
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_calls: int, period: int):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()

    def allow(self) -> bool:
        now = time.time()
        while self.calls and now - self.calls[0] > self.period:
            self.calls.popleft()
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False

# simple per-user limiter holder
_user_limiters = {}

def check_user_limit(user_id: int, max_calls=5, period=60) -> bool:
    limiter = _user_limiters.get(user_id)
    if limiter is None:
        limiter = RateLimiter(max_calls, period)
        _user_limiters[user_id] = limiter
    return limiter.allow()
