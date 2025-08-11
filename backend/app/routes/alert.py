from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.alert import Alert, AlertType
from app.models.transactions import Transaction
from app.models.ea_account import EAAccount
from app.utils.deps import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/alerts", tags=["Alerts"])

# هشدارهای لحظه‌ای (CAPTCHA، RATE_LIMIT، ERROR)
@router.get("/live")
def get_live_alerts(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
	now = datetime.utcnow()
	since = now - timedelta(hours=24)
	alerts = db.query(Alert).filter(
		Alert.resolved == False,
		Alert.created_at >= since
	).order_by(Alert.created_at.desc()).all()
	return alerts

# تراکنش‌های در حال انجام (pending یا pending_captcha)
@router.get("/pending-transactions")
def get_pending_transactions(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
	txs = db.query(Transaction).filter(
		Transaction.status.in_(["pending", "pending_captcha"])
	).order_by(Transaction.created_at.desc()).all()
	return txs

# حل هشدار (مثلاً CAPTCHA)
@router.post("/resolve/{alert_id}")
def resolve_alert(alert_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
	alert = db.query(Alert).filter_by(id=alert_id).first()
	if not alert:
		raise HTTPException(status_code=404, detail="هشدار پیدا نشد")
	alert.resolved = True
	alert.resolved_at = datetime.utcnow()
	# فعال‌سازی مجدد اکانت
	account = db.query(EAAccount).filter_by(id=alert.account_id).first()
	if account:
		account.status = "active"
		account.paused_until = None
	db.commit()
	return {"message": "هشدار با موفقیت حل شد و اکانت فعال شد"}
