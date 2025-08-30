import time
from typing import Any


class TTLCache:
    def __init__(self, default_ttl: int = 3600):
        self._store: dict[str, tuple[float, Any]] = {}
        self.default_ttl = default_ttl

    def set(self, key: str, value: Any, ttl: int | None = None):
        expire = time.time() + (ttl if ttl is not None else self.default_ttl)
        self._store[key] = (expire, value)

    def get(self, key: str):
        item = self._store.get(key)
        if not item:
            return None
        expire, value = item
        if time.time() > expire:
            del self._store[key]
            return None
        return value

    def delete(self, key: str):
        if key in self._store:
            del self._store[key]


cache = TTLCache()
