from fastapi import APIRouter, Query, Depends
from app.services.futbin_client import get_player_price
from app.utils.rate_limiter import rate_limiter
from typing import Optional


router = APIRouter(prefix="/futbin", tags=["futbin"])

rl_futbin_price = rate_limiter(limit=5, window_seconds=1, namespace="futbin.price")

@router.get("/price")
async def get_price(
    player_id: int = Query(...),
    platform: str = Query("ps/xbox"),
    slug: Optional[str] = Query(None, description="exact futbin slug from admin, e.g. 'allan-saint-maximin'"),
    name: Optional[str] = Query(None, description="player name (used to generate slug if slug not provided)")
):
    result = await get_player_price(str(player_id), platform, slug=slug, name=name)
    return {
        "player_id": player_id,
        "platform": platform,
        "price": result.get("price"),
        "cached": result.get("cached", False),
        "fetched_at": result.get("fetched_at"),
        "note": result.get("note"),
    }
