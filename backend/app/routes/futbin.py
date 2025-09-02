# app/routes/futbin.py
from fastapi import APIRouter, Query, HTTPException, Depends
from app.services.futbin_client import get_player_price
from app.utils.deps import get_db  # اگر نیاز به DB باشه
from typing import Optional

router = APIRouter(prefix="/futbin", tags=["Futbin"])

@router.get("/price")
async def get_price(player_id: str = Query(...), platform: str = Query("pc"), ttl: int = Query(3)):
    try:
        res = await get_player_price(player_id=player_id, platform=platform, ttl=ttl)
        return res
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))