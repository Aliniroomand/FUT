from fastapi import APIRouter, Query, Depends
from app.services.futbin_player_price import fetch_player_price
from app.utils.rate_limiter import rate_limit

router = APIRouter(prefix="/futbin", tags=["futbin"])

# فقط تابع rate_limit را بدون () بدهید
@router.get("/price")
async def get_price(
    player_id: int = Query(...),
    slug: str = Query(...),
    platform: str = Query("pc"),
    limiter=Depends(rate_limit) 
):
    result = await fetch_player_price(player_id, slug, platform)
    return {
        "player_id": player_id,
        "platform": platform,
        "price": result.get("price"),
        "raw": result.get("raw"),
        "cached": result.get("cached", False),
        "fetched_at": result.get("fetched_at"),
        "note": result.get("note"),
    }
