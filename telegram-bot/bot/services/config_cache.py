"""Config caching helpers for seldom-changing data.

Provides both async and sync variants for callers.
Uses `bot.services.cache` as storage backend (Redis or in-memory fallback).
"""
from __future__ import annotations

import asyncio
import inspect
import logging
from typing import Any, Callable, Dict, List, Optional

from bot.services import cache

logger = logging.getLogger(__name__)

# cache key versions - bump if shape changes
_TRANSFER_METHODS_KEY = "cfg:transfer_methods:v1"
_CARD_RANGES_KEY = "cfg:card_ranges:v1"
_TRANSACTION_STATUS_KEY = "cfg:transaction_status:v1"
_PLAYER_CARD_META_KEY_FMT = "cfg:player_card_meta:v1:{player_id}"


async def _call_fetch_async(fetch_func: Callable, *args, **kwargs) -> Any:
    if inspect.iscoroutinefunction(fetch_func):
        return await fetch_func(*args, **kwargs)
    # run sync function in thread to avoid blocking event loop
    return await asyncio.to_thread(fetch_func, *args, **kwargs)


def _call_fetch_sync(fetch_func: Callable, *args, **kwargs) -> Any:
    if inspect.iscoroutinefunction(fetch_func):
        # try to run coroutine in a fresh event loop
        try:
            return asyncio.run(fetch_func(*args, **kwargs))
        except RuntimeError as exc:
            # likely there is already a running event loop
            logger.error("Cannot run coroutine fetch_func in sync context: %s", exc)
            raise
    return fetch_func(*args, **kwargs)


# Generic async/sync getters
async def get_transfer_methods(fetch_func: Callable[[], List[Dict[str, Any]]], ttl: int = 600) -> List[Dict[str, Any]]:
    """Async getter for transfer methods."""
    cached = cache.get(_TRANSFER_METHODS_KEY)
    if cached is not None:
        return cached
    data = await _call_fetch_async(fetch_func)
    try:
        cache.set(_TRANSFER_METHODS_KEY, data, ttl)
    except Exception as exc:
        logger.warning("Failed to set cache for transfer_methods: %s", exc)
    return data


def get_transfer_methods_sync(fetch_func: Callable[[], List[Dict[str, Any]]], ttl: int = 600) -> List[Dict[str, Any]]:
    """Sync getter for transfer methods."""
    cached = cache.get(_TRANSFER_METHODS_KEY)
    if cached is not None:
        return cached
    data = _call_fetch_sync(fetch_func)
    try:
        cache.set(_TRANSFER_METHODS_KEY, data, ttl)
    except Exception as exc:
        logger.warning("Failed to set cache for transfer_methods: %s", exc)
    return data


async def get_card_ranges(fetch_func: Callable[[], List[Dict[str, Any]]], ttl: int = 600) -> List[Dict[str, Any]]:
    cached = cache.get(_CARD_RANGES_KEY)
    if cached is not None:
        return cached
    data = await _call_fetch_async(fetch_func)
    try:
        cache.set(_CARD_RANGES_KEY, data, ttl)
    except Exception as exc:
        logger.warning("Failed to set cache for card_ranges: %s", exc)
    return data


def get_card_ranges_sync(fetch_func: Callable[[], List[Dict[str, Any]]], ttl: int = 600) -> List[Dict[str, Any]]:
    cached = cache.get(_CARD_RANGES_KEY)
    if cached is not None:
        return cached
    data = _call_fetch_sync(fetch_func)
    try:
        cache.set(_CARD_RANGES_KEY, data, ttl)
    except Exception as exc:
        logger.warning("Failed to set cache for card_ranges: %s", exc)
    return data


async def get_transaction_status(fetch_func: Callable[[], Dict[str, Any]], ttl: int = 10) -> Dict[str, Any]:
    # Try fast path: return cached if present
    cached = cache.get(_TRANSACTION_STATUS_KEY)
    if cached is not None:
        return cached

    # No cached value: fetch from backend but tolerate failures by
    # returning stale value if fetch fails (caller will log/notify).
    try:
        data = await _call_fetch_async(fetch_func)
    except Exception as exc:
        logger.warning("transaction_status fetch failed and no cache present: %s", exc)
        # No cached value to fall back to — propagate error to caller
        raise

    try:
        cache.set(_TRANSACTION_STATUS_KEY, data, ttl)
    except Exception as exc:
        logger.warning("Failed to set cache for transaction_status: %s", exc)
    return data


def get_transaction_status_sync(fetch_func: Callable[[], Dict[str, Any]], ttl: int = 10) -> Dict[str, Any]:
    cached = cache.get(_TRANSACTION_STATUS_KEY)
    if cached is not None:
        return cached

    try:
        data = _call_fetch_sync(fetch_func)
    except Exception as exc:
        logger.warning("transaction_status fetch failed and no cache present: %s", exc)
        raise

    try:
        cache.set(_TRANSACTION_STATUS_KEY, data, ttl)
    except Exception as exc:
        logger.warning("Failed to set cache for transaction_status: %s", exc)
    return data


async def get_player_card_meta(fetch_func: Callable[[int], Dict[str, Any]], player_id: int, ttl: int = 600) -> Dict[str, Any]:
    key = _PLAYER_CARD_META_KEY_FMT.format(player_id=player_id)
    cached = cache.get(key)
    if cached is not None:
        return cached
    data = await _call_fetch_async(fetch_func, player_id)
    try:
        cache.set(key, data, ttl)
    except Exception as exc:
        logger.warning("Failed to set cache for player_card_meta(%s): %s", player_id, exc)
    return data


def get_player_card_meta_sync(fetch_func: Callable[[int], Dict[str, Any]], player_id: int, ttl: int = 600) -> Dict[str, Any]:
    key = _PLAYER_CARD_META_KEY_FMT.format(player_id=player_id)
    cached = cache.get(key)
    if cached is not None:
        return cached
    data = _call_fetch_sync(fetch_func, player_id)
    try:
        cache.set(key, data, ttl)
    except Exception as exc:
        logger.warning("Failed to set cache for player_card_meta(%s): %s", player_id, exc)
    return data


# Invalidate helpers

def invalidate_transfer_methods() -> None:
    cache.delete(_TRANSFER_METHODS_KEY)


def invalidate_card_ranges() -> None:
    cache.delete(_CARD_RANGES_KEY)


def invalidate_player_card_meta(player_id: int) -> None:
    key = _PLAYER_CARD_META_KEY_FMT.format(player_id=player_id)
    cache.delete(key)
