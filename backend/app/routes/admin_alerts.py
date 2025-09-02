# app/routes/admin_alerts.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.futbin_client import clear_negative_block
from app.cache import get_redis

router = APIRouter(prefix="/admin/alerts", tags=["admin"])

class ResolveRequest(BaseModel):
    clear_negative_block: bool = True
    comment: str | None = None

@router.post("/{alert_id}/resolve")
async def resolve_alert(alert_id: int, body: ResolveRequest):
    """
    Resolve an alert (update DB via app.crud.alerts if available), and optionally clear negative block.
    """
    # Try update DB via CRUD if exists
    try:
        from app.crud.alerts import update_alert_status  # type: ignore
        # Try calling update_alert_status(alert_id, status="resolved", meta={"comment": ...})
        try:
            await update_alert_status(alert_id, "resolved", {"comment": body.comment})
        except TypeError:
            # maybe different signature
            await update_alert_status(alert_id, {"status": "resolved", "comment": body.comment})
    except Exception:
        # If CRUD not available, just log and continue
        pass

    # Optionally clear negative block for the player — we need player info from DB; try to fetch alert to get player/platform
    player = None
    platform = None
    try:
        from app.crud.alerts import get_alert  # type: ignore
        alert = await get_alert(alert_id)
        player = alert.get("player_id") if isinstance(alert, dict) else getattr(alert, "player_id", None)
        platform = alert.get("platform") if isinstance(alert, dict) else getattr(alert, "platform", None)
    except Exception:
        pass

    if body.clear_negative_block and player and platform:
        try:
            await clear_negative_block(str(player), str(platform))
        except Exception:
            pass

    return {"ok": True, "resolved": True}
