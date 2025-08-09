from pydantic import BaseModel
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

