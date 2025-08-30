import asyncio
import httpx
from typing import Any

from bot.adapters.cache import cache
from bot.config import settings

BASE_URL = getattr(settings, 'backend_url', 'http://localhost:8000')


async def http_get(path: str, params: dict | None = None):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}{path}", params=params, timeout=10.0)
        r.raise_for_status()
        return r.json()


async def get_card_ranges():
    # expecting endpoint /card-ranges or /card-ranges/
    try:
        return await http_get("/card-ranges")
    except httpx.HTTPStatusError:
        return await http_get("/card-ranges/")


async def get_player_card(card_id: int):
    cache_key = f"player_card:{card_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    data = await http_get(f"/player-cards/{card_id}")
    cache.set(cache_key, data)
    return data
