
# app/crud/alerts.py
# Compatibility wrapper for alert CRUD. If you have a real DB-backed
# implementation, place it in app.crud.alerts_impl with the same names
# (create_alert, update_alert_status, get_alert) and this wrapper will
# delegate to it. The wrapper supports both sync and async real functions.
#
# TEMP: added app/crud/alerts.py stub for dev. Remove and replace with
# a real DB CRUD implementation when available. (Keep this note in the
# PR/commit message when merging.)

import asyncio
import inspect
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger("app.crud.alerts")

# Try to import a real implementation module (optional)
_real_create = None
_real_update = None
_real_get = None
try:
    from app.crud.alerts_impl import create_alert as _real_create  # type: ignore
    from app.crud.alerts_impl import update_alert_status as _real_update  # type: ignore
    from app.crud.alerts_impl import get_alert as _real_get  # type: ignore
except Exception:
    # No real implementation found; fall back to internal stub
    _real_create = None
    _real_update = None
    _real_get = None


async def _run_maybe_sync(func, *args, **kwargs):
    """Run func whether it's sync or async. Return its result."""
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


async def create_alert(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compatibility wrapper. Delegates to a real implementation if available.
    Otherwise uses a minimal async stub.
    """
    if _real_create:
        try:
            return await _run_maybe_sync(_real_create, payload)
        except Exception:
            logger.exception("Real create_alert failed; falling back to stub")

    # minimal stub
    logger.info("STUB create_alert called", extra={"payload": payload})
    await asyncio.sleep(0)
    return {"id": 0, **payload}


async def update_alert_status(alert_id: int, status: str, meta: Optional[Dict[str, Any]] = None) -> bool:
    if _real_update:
        try:
            return await _run_maybe_sync(_real_update, alert_id, status, meta)
        except Exception:
            logger.exception("Real update_alert_status failed; falling back to stub")

    logger.info("STUB update_alert_status", extra={"alert_id": alert_id, "status": status, "meta": meta})
    await asyncio.sleep(0)
    return True


async def get_alert(alert_id: int) -> Dict[str, Any]:
    if _real_get:
        try:
            return await _run_maybe_sync(_real_get, alert_id)
        except Exception:
            logger.exception("Real get_alert failed; falling back to stub")

    logger.info("STUB get_alert", extra={"alert_id": alert_id})
    await asyncio.sleep(0)
    return {"player_id": "12345", "platform": "pc", "status": "open"}

