# app/routes/profile.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import UserProfile, User
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.utils.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/profile", tags=["Profile"])

# دریافت پروفایل کاربر
@router.get("/me", response_model=ProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),  # دریافت کاربر از توکن
    db: Session = Depends(get_db)
):
    profile = db.query(UserProfile).filter_by(user_id=current_user.id).first()
    if not profile:
        # اگر پروفایل هنوز ایجاد نشده، یک پروفایل جدید بساز
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    # اضافه کردن is_admin به پاسخ
    return {
        **profile.__dict__,
        "is_admin": bool(current_user.is_admin)
    }

# به‌روزرسانی پروفایل کاربر
@router.put("/me", response_model=ProfileResponse)
def update_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),  # دریافت کاربر از توکن
    db: Session = Depends(get_db)
):
    profile = db.query(UserProfile).filter_by(user_id=current_user.id).first()
    if not profile:
        raise HTTPException(404, "Profile not found")
    # فقط فیلدهایی که تغییر داده شده‌اند به‌روز می‌شوند
    for field, value in data.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile
