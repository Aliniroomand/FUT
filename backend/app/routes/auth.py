from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserResponse , UserCreate ,UserLogin, UserResponse
from app.models.user import User
from app.utils.security import hash_password , verify_password
import secrets



router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(phone_number=user.phone_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    db_user = User(
        phone_number=user.phone_number,
        email=user.email,
        password_hash=hash_password(user.password) if user.password else None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=UserResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return db_user

    
# send token for recover passsword

@router.post("/forgot-password")
def forgot_password(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Email not registered")

    reset_token = secrets.token_hex(16)  # Create a secure token
    db_user.reset_token = reset_token
    db.add(db_user)
    db.commit()

    # Send reset_token to the user's email (implementing email service is required)
    # send_reset_email(user.email, reset_token)
    
    return {"message": "Password reset link has been sent to your email."}

# reset password
@router.post("/reset-password/{token}")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.reset_token == token).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    db_user.password_hash = hash_password(new_password)
    db_user.reset_token = None  # Clear the reset token after successful reset
    db.add(db_user)
    db.commit()

    return {"message": "Password has been successfully reset"}