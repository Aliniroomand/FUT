from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ea_account import EAAccount
from app.schemas.ea_account import EAAccountCreate, EAAccountOut
from app.crud.ea_account import create_ea_account, delete_ea_account
from app.utils.deps import get_current_user

router = APIRouter(prefix="/ea-accounts", tags=["EA Accounts"])


# لیست اکانت‌ها (برای پنل ادمین)
@router.get("/", response_model=list[EAAccountOut])
def list_accounts(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
	accounts = db.query(EAAccount).order_by(EAAccount.id.asc()).all()
	return accounts

# ایجاد اکانت جدید
@router.post("/", response_model=EAAccountOut)
def add_account(account: EAAccountCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
	db_account = create_ea_account(db, account)
	return db_account

# حذف اکانت
@router.delete("/{account_id}")
def remove_account(account_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
	success = delete_ea_account(db, account_id)
	if not success:
		raise HTTPException(status_code=404, detail="اکانت پیدا نشد")
	return {"message": "اکانت با موفقیت حذف شد"}

# ویرایش daily_limit هر اکانت (inline edit)
@router.patch("/{account_id}/daily-limit")
def update_daily_limit(account_id: int, daily_limit: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
	account = db.query(EAAccount).filter_by(id=account_id).first()
	if not account:
		raise HTTPException(status_code=404, detail="اکانت پیدا نشد")
	account.daily_limit = daily_limit
	db.commit()
	return {"message": "سقف روزانه با موفقیت بروزرسانی شد"}
