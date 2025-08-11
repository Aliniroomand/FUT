from app.models.alert import Alert, AlertType
from sqlalchemy.exc import SQLAlchemyError

def atomic_create_transaction(db: Session, user_id: int, amount: int, transaction_type: str, **kwargs):
	try:
		# انتخاب اکانت مناسب
		account = get_available_account_for_user(db, user_id, amount)
		effective_daily_limit = account.daily_limit if account.daily_limit is not None else GLOBAL_DAILY_LIMIT

		# ایجاد تراکنش pending
		transaction = Transaction(
			user_id=user_id,
			account_id=account.id,
			amount=amount,
			transaction_type=transaction_type,
			status="pending",
			created_at=datetime.utcnow(),
			**kwargs
		)
		db.add(transaction)
		db.flush()  # برای گرفتن id

		# فراخوانی ea_client (شبیه‌سازی شده)
		# اینجا باید منطق واقعی خرید/فروش را فراخوانی کنید
		# فرض: نتیجه موفقیت‌آمیز
		ea_result = {"success": True, "captcha": False, "error": None}

		now = datetime.utcnow()
		if ea_result["success"]:
			transaction.status = "success"
			transaction.completed_at = now
			account.transferred_today += amount
			account.last_transfer_time = now

			# اگر سقف روزانه رسید
			if account.transferred_today >= effective_daily_limit:
				account.status = EAAccountStatus.paused
				account.paused_until = now + timedelta(hours=24)
				# ایجاد alert نوع RATE_LIMIT
				alert = Alert(
					account_id=account.id,
					type=AlertType.RATE_LIMIT,
					message=f"سقف روزانه اکانت رسید.",
					created_at=now
				)
				db.add(alert)

		elif ea_result["captcha"]:
			transaction.status = "pending_captcha"
			account.status = EAAccountStatus.paused
			account.paused_until = now + timedelta(hours=24)
			account.last_captcha_at = now
			alert = Alert(
				account_id=account.id,
				type=AlertType.CAPTCHA,
				message="نیاز به حل کپچا.",
				created_at=now
			)
			db.add(alert)
			# ارسال event وب‌سوکت (در صورت نیاز)

		elif ea_result["error"]:
			transaction.status = "failed"
			transaction.completed_at = now
			alert = Alert(
				account_id=account.id,
				type=AlertType.ERROR,
				message=ea_result["error"],
				created_at=now
			)
			db.add(alert)

		db.commit()
		db.refresh(transaction)
		return transaction
	except SQLAlchemyError as e:
		db.rollback()
		raise HTTPException(status_code=500, detail={"error": "db_error", "message": str(e)})
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from app.models.ea_account import EAAccount, EAAccountStatus
from app.models.transactions import Transaction
from fastapi import HTTPException

GLOBAL_DAILY_LIMIT = 1000000  # مقدار پیش‌فرض، قابل تنظیم

def get_available_account_for_user(db: Session, user_id: int, amount: int):
	now = datetime.now(datetime.timezone.utc)()
	since = now - timedelta(hours=24)

	# فعال‌سازی lazy برای اکانت‌هایی که paused_until گذشته است
	db.query(EAAccount).filter(
		EAAccount.status == EAAccountStatus.paused,
		EAAccount.paused_until <= now
	).update({EAAccount.status: EAAccountStatus.active, EAAccount.paused_until: None})
	db.commit()

	# بارگذاری اکانت‌های فعال
	accounts = db.query(EAAccount).filter(
		EAAccount.status == EAAccountStatus.active,
		or_(EAAccount.paused_until == None, EAAccount.paused_until <= now)
	).all()

	candidates = []
	for acc in accounts:
		effective_daily_limit = acc.daily_limit if acc.daily_limit is not None else GLOBAL_DAILY_LIMIT
		if acc.transferred_today >= effective_daily_limit:
			continue
		if acc.last_transfer_time and acc.last_transfer_time >= since:
			continue
		# فقط یک تراکنش در ۲۴ ساعت برای هر کاربر
		exists = db.query(Transaction).filter(
			Transaction.account_id == acc.id,
			Transaction.user_id == user_id,
			Transaction.created_at >= since
		).first()
		if exists:
			continue
		candidates.append(acc)

	# ترتیب بر اساس transferred_today (کمترین استفاده)
	candidates.sort(key=lambda x: x.transferred_today)

	if not candidates:
		raise HTTPException(status_code=409, detail={"error": "no_available_account", "message": "هیچ اکانتی که شرایط را داشته باشد در دسترس نیست"})

	# انتخاب اولین کاندیدا
	selected = candidates[0]
	# TODO: اعمال قفل کوتاه‌مدت روی رکورد (در صورت نیاز)
	return selected
