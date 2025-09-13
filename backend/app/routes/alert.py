# app/routes/alert.py
from fastapi import APIRouter, Depends, HTTPException, Response
from app.crud import alerts as crud_alerts
from app.database import get_db
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
from fastapi import status

router = APIRouter(prefix="/alerts", tags=["Alerts"])

class AlertCreate(BaseModel):
    type: Optional[str] = "ERROR"
    title: Optional[str] = None
    message: Optional[str] = None
    player_id: Optional[str] = None
    platform: Optional[str] = None
    sample_html: Optional[str] = None
    futbin_url: Optional[str] = None
    account_id: Optional[int] = None
    meta: Optional[dict] = None

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_alert_endpoint(payload: AlertCreate):
    d = payload.dict()
    if not d.get("message") and d.get("title"):
        d["message"] = d["title"]
    created = await crud_alerts.create_alert(d)
    return {"ok": True, "created": created}

@router.get("/live")
async def get_unresolved_alerts_endpoint():
    alerts = await crud_alerts.get_unresolved_alerts()
    return alerts

@router.get("/resolved")
async def get_resolved_alerts_endpoint():
    alerts = await crud_alerts.get_resolved_alerts()
    return alerts
    
@router.get("/{alert_id}")
async def get_alert(alert_id: int):
    a = await crud_alerts.get_alert_full(alert_id)
    if not a:
        raise HTTPException(status_code=404, detail="alert not found")
    # برگرداندن sample_html را امن نگه‌دار (اگر نیاز است auth ادمین چک شود)
    return a

@router.post("/{alert_id}/resolve")
async def resolve_alert_endpoint(alert_id: int):
    # 1) resolve in DB
    res = await crud_alerts.resolve_alert(alert_id)
    if not res.get("ok"):
        raise HTTPException(status_code=404, detail="alert not found")
    # 2) instruct futbin client to clear negative cache / unblock (we'll implement an exported function)
    from app.services.futbin_client import clear_futbin_block_for_alert
    try:
        await clear_futbin_block_for_alert(alert_id)
    except Exception as e:
        # لاگ کن ولی اجازه بده resolve صورت بگیره
        pass
    return {"ok": True}
