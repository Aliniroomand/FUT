# app/crud/alerts.py
import asyncio
from typing import Any, Dict, Optional
from app.database import SessionLocal
from app.models.alert import Alert, AlertType
from datetime import datetime, timedelta, timezone
import json

def _sync_create_alert(payload: Dict[str, Any]) -> Dict[str, Any]:
    db = SessionLocal()
    try:
        account_id = payload.get("account_id") or 0
        type_val = payload.get("type", "ERROR")
        try:
            alert_type = AlertType[type_val] if isinstance(type_val, str) and type_val in AlertType.__members__ else AlertType.ERROR
        except Exception:
            alert_type = AlertType.ERROR

        a = Alert(
            account_id = account_id,
            type = alert_type,
            message = payload.get("message", payload.get("title", "No message provided")),
            futbin_url = payload.get("futbin_url"),
            sample_html = payload.get("sample_html"),
            meta = json.dumps(payload.get("meta", {})) if payload.get("meta") else None
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        return {"id": a.id, "ok": True}
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

async def create_alert(payload: Dict[str, Any]) -> Dict[str, Any]:
    return await asyncio.to_thread(_sync_create_alert, payload)

# helpers:
async def get_alert_full(alert_id: int) -> Optional[Dict[str, Any]]:
    def _sync(aid):
        db = SessionLocal()
        try:
            a = db.query(Alert).filter_by(id=aid).first()
            if not a:
                return None
            return {
                "id": a.id,
                "account_id": a.account_id,
                "type": a.type.name if a.type else None,
                "message": a.message,
                "futbin_url": a.futbin_url,
                "sample_html": a.sample_html,
                "meta": a.meta,
                "resolved": a.resolved,
                "created_at": a.created_at.isoformat(),
                "resolved_at": a.resolved_at.isoformat() if a.resolved_at else None,
            }
        finally:
            db.close()
    return await asyncio.to_thread(_sync, alert_id)

async def resolve_alert(alert_id: int) -> Dict[str, Any]:
    def _sync_res(aid):
        db = SessionLocal()
        try:
            a = db.query(Alert).filter_by(id=aid).first()
            if not a:
                return {"ok": False}
            a.resolved = True
            a.resolved_at = datetime.now(timezone.utc)
            db.commit()
            return {"ok": True}
        finally:
            db.close()
    return await asyncio.to_thread(_sync_res, alert_id)

# app/crud/alerts.py

async def get_unresolved_alerts(hours: int = 24):
    """فقط alert هایی که resolve نشده‌اند"""
    def _sync():
        db = SessionLocal()
        try:
            since = datetime.now(timezone.utc) - timedelta(hours=hours)
            q = (
                db.query(Alert)
                .filter(Alert.created_at >= since, Alert.resolved == False)
                .order_by(Alert.created_at.desc())
                .all()
            )
            return [
                {
                    "id": a.id,
                    "account_id": a.account_id,
                    "type": a.type.name if a.type else None,
                    "message": a.message,
                    "futbin_url": a.futbin_url,
                    "sample_html": a.sample_html,
                    "meta": a.meta,
                    "resolved": a.resolved,
                    "created_at": a.created_at.isoformat(),
                }
                for a in q
            ]
        finally:
            db.close()
    return await asyncio.to_thread(_sync)


async def get_resolved_alerts(hours: int = 24):
    """فقط alert هایی که resolve شده‌اند (برای نمایش آرشیو)"""
    def _sync():
        db = SessionLocal()
        try:
            since = datetime.now(timezone.utc) - timedelta(hours=hours)
            q = (
                db.query(Alert)
                .filter(Alert.created_at >= since, Alert.resolved == True)
                .order_by(Alert.created_at.desc())
                .all()
            )
            return [
                {
                    "id": a.id,
                    "account_id": a.account_id,
                    "type": a.type.name if a.type else None,
                    "message": a.message,
                    "futbin_url": a.futbin_url,
                    "sample_html": a.sample_html,
                    "meta": a.meta,
                    "resolved": a.resolved,
                    "created_at": a.created_at.isoformat(),
                    "resolved_at": a.resolved_at.isoformat() if a.resolved_at else None,
                }
                for a in q
            ]
        finally:
            db.close()
    return await asyncio.to_thread(_sync)