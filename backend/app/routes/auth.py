from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import (
    UserResponse, UserCreate, UserLogin, ResetPasswordRequest
)
from app.models.user import User
from app.utils.security import hash_password, verify_password
import secrets
from app.utils.email_sender import send_reset_email
from app.utils.jwt import create_access_token, create_refresh_token, verify_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])


def mask_phone(phone: str) -> str:
    if not phone or len(phone) < 5:
        return "**********"
    return phone[:3] + "*" * (len(phone) - 5) + phone[-2:]



# ثبت‌نام کامل با ایمیل، شماره و رمز
@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    phone_exists = db.query(User).filter_by(phone_number=data.phone_number).first()
    email_exists = db.query(User).filter_by(email=data.email).first()
    if phone_exists:
        raise HTTPException(400, detail="این شماره موبایل قبلا ثبت شده است")
    if email_exists:
        raise HTTPException(400, detail="این ایمیل قبلا ثبت شده است")
    user = User(
        phone_number=data.phone_number,
        email=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token = create_access_token({"user_id": user.id, "is_admin": bool(user.is_admin)})
    refresh_token = create_refresh_token({"user_id": user.id, "is_admin": bool(user.is_admin)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "id": user.id,
        "phone_number": user.phone_number,
        "email": user.email,
        "is_admin": bool(user.is_admin),
        "require_password_change": False
    }
    
    
@router.post("/complete-registration", response_model=UserResponse)
def complete_registration(data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()
    if not user:
        raise HTTPException(400, "یافت نشد")
    if user.password_hash:
        raise HTTPException(400, "در حال حاضر پسورد ثبت شده است")
    user.password_hash = hash_password(data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse(
        id=user.id,
        phone_number=user.phone_number,
        email=user.email,
        is_admin=bool(user.is_admin),
        require_password_change=False
    )


@router.post("/login")
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="اکانت با چنین مشخصاتی وجود ندارد")

    access_token = create_access_token({"user_id": user.id, "is_admin": bool(user.is_admin)})
    refresh_token = create_refresh_token({"user_id": user.id, "is_admin": bool(user.is_admin)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "id": user.id,
        "phone_number": user.phone_number,
        "email": user.email,
        "is_admin": bool(user.is_admin),
        "require_password_change": False,
    }
# endpoint for refreshing access token
from fastapi import Body

@router.post("/refresh-token")
def refresh_token(refresh_token: str = Body(...)):
    payload = verify_refresh_token(refresh_token)
    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    # issue new access token
    access_token = create_access_token({"user_id": payload["user_id"], "is_admin": payload.get("is_admin", False)})
    return {"access_token": access_token}


@router.post("/forgot-password")
def forgot_password(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="این ایمیل وجود ندارد یا اشتباه است")

    reset_token = secrets.token_hex(16)
    db_user.reset_token = reset_token
    db.add(db_user)
    db.commit()

    try:
        send_reset_email(user.email, reset_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail="خطا : ایمیل ارسال نشد")

    return {"message": "لینک بازیابی رمز عبور به ایمیل شما ارسال شد"}


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.reset_token == data.token).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="توکن بازنشانی نامعتبر یا منقضی شده است")

    db_user.password_hash = hash_password(data.new_password)
    db_user.reset_token = None
    db.add(db_user)
    db.commit()
    return {"message": "رمز با موفقیت تغییر یافت"}
