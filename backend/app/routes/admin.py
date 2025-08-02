from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.deps import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

# فقط ادمین‌ها مجازند
@router.post("/make-admin")
def make_admin(user_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    # بررسی اینکه درخواست‌دهنده خودش ادمین است
    admin_user = db.query(User).filter_by(id=current_user["user_id"]).first()
    if not admin_user or not admin_user.is_admin:
        raise HTTPException(status_code=403, detail="دسترسی فقط برای ادمین مجاز است")
    # پیدا کردن کاربر هدف
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")
    user.is_admin = 1
    db.add(user)
    db.commit()
    return {"message": "کاربر با موفقیت ادمین شد"}
