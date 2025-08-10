# app/routes/profile.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import UserProfile, User
from app.schemas.profile import ProfileResponse, ProfileUpdate, FullProfileResponse
from app.utils.deps import get_current_user

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

# دریافت اطلاعات کامل پروفایل بر اساس شناسه کاربری
@router.get("/full/{user_id}", response_model=FullProfileResponse)
def get_full_profile_by_id(
    user_id: int = Path(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # فقط ادمین یا خود کاربر می‌توانند به این اطلاعات دسترسی داشته باشند
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    return FullProfileResponse(
        id=user.id,
        phone_number=user.phone_number,
        email=user.email,
        is_admin=bool(user.is_admin),
        first_name=profile.first_name if profile else None,
        last_name=profile.last_name if profile else None,
        card_number=profile.card_number if profile else None,
        bank_account_number=profile.bank_account_number if profile else None,
        bank_account_name=profile.bank_account_name if profile else None,
        telegram_id=user.telegram_id
    )
