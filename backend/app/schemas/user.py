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
