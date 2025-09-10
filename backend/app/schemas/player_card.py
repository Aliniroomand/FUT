from pydantic import BaseModel
from typing import Optional


class PlayerCardBase(BaseModel):
    name: str
    rating: str
    version: str


class PlayerCardCreate(PlayerCardBase):
# allow admin-provided id; DB autoincrement still works if omitted
    id: Optional[int] = None


class PlayerCardUpdate(BaseModel):
    name: Optional[str] = None
    rating: Optional[str] = None
    version: Optional[str] = None


class PlayerCard(PlayerCardBase):
    id: int
    
class Config:
    from_attributes = True


# Lightweight schema used by other modules
class PlayerCardShort(BaseModel):
    id: int
    name: str