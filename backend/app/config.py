"""Lightweight settings loader using environment variables.

This module intentionally avoids importing pydantic to prevent import-time
errors in environments where pydantic v2's BaseSettings is not available
via the `pydantic-settings` package. The class below provides the same
configuration surface the app expects via simple env var lookups.
"""
from __future__ import annotations
import os
from typing import Optional


def _bool_env(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.lower() in ("1", "true", "yes", "on")


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./fut.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Futbin / scraping related settings
    # Cache TTL (in seconds) for Futbin price freshness
    FUTBIN_CACHE_TTL: int = int(os.getenv("FUTBIN_CACHE_TTL", "3"))

    # When a captcha/protection event occurs, block retries for this many seconds
    FUTBIN_NEGATIVE_CACHE_SECONDS: int = int(os.getenv("FUTBIN_NEGATIVE_CACHE_SECONDS", "60"))

    # How long to dedupe alerts (prevent duplicate alerts within this window)
    FUTBIN_ALERT_DEDUPE_SECONDS: int = int(os.getenv("FUTBIN_ALERT_DEDUPE_SECONDS", "120"))

    # Maximum concurrent requests to Futbin from this process
    MAX_FUTBIN_CONCURRENCY: int = int(os.getenv("MAX_FUTBIN_CONCURRENCY", "2"))

    # User-Agent used for scraping Futbin (override in env if needed)
    FUTBIN_USER_AGENT: str = os.getenv(
        "FUTBIN_USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    )

    # Optional: internal route to post an alert if CRUD import fails
    INTERNAL_ALERT_POST_URL: str = os.getenv("INTERNAL_ALERT_POST_URL", "")

    EA_API_URL: str = os.getenv("EA_API_URL", "")
    # Controls whether the background transfer worker is started on app startup.
    START_WORKER: bool = _bool_env("START_WORKER", False)
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")

    # Optional: use a Redis-based distributed lock instead of process-local semaphore.
    # Set to "1" or "true" in env to enable distributed locking across multiple workers.
    USE_DISTRIBUTED_LOCK: bool = _bool_env("USE_DISTRIBUTED_LOCK", False)


settings = Settings()

# Module-level convenience constants for backwards compatibility
DATABASE_URL = settings.DATABASE_URL
REDIS_URL = settings.REDIS_URL
FUTBIN_CACHE_TTL = settings.FUTBIN_CACHE_TTL
FUTBIN_NEGATIVE_CACHE_SECONDS = settings.FUTBIN_NEGATIVE_CACHE_SECONDS
FUTBIN_ALERT_DEDUPE_SECONDS = settings.FUTBIN_ALERT_DEDUPE_SECONDS
MAX_FUTBIN_CONCURRENCY = settings.MAX_FUTBIN_CONCURRENCY
FUTBIN_USER_AGENT = settings.FUTBIN_USER_AGENT
INTERNAL_ALERT_POST_URL = settings.INTERNAL_ALERT_POST_URL
USE_DISTRIBUTED_LOCK = settings.USE_DISTRIBUTED_LOCK
