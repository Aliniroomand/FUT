from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EAAccountCreate(BaseModel):
	name: str
	email: EmailStr
	platform: str
	daily_limit: Optional[int] = None
	is_user_account: Optional[bool] = False

class EAAccountOut(BaseModel):
	id: int
	name: str
	email: EmailStr
	platform: str
	daily_limit: Optional[int]
	transferred_today: int
	last_transfer_time: Optional[datetime]
	status: str
	paused_until: Optional[datetime]
	is_user_account: bool
	session_token: Optional[str]
	last_captcha_at: Optional[datetime]
	created_at: datetime
	updated_at: Optional[datetime]

	class Config:
		from_attributes = True
