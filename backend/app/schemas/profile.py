from pydantic import BaseModel, EmailStr
from typing import Optional

class ProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_account_name: Optional[str] = None

class ProfileResponse(ProfileBase):
    user_id: int
    is_admin: bool = False

    class Config:
        from_attributes = True

class ProfileUpdate(ProfileBase):
    pass

class FullProfileResponse(BaseModel):
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

