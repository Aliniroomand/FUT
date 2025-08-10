from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    phone_number: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    phone_number: str
    email: str
    is_admin: bool = False
    require_password_change: Optional[bool] = False
    
    
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


    class Config:
        from_attributes = True

class FullUserResponse(BaseModel):
    id: int
    phone_number: str
    email: EmailStr
    is_admin: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    card_number: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_account_name: Optional[str] = None
    telegram_id: Optional[str] = None

    class Config:
        from_attributes = True
