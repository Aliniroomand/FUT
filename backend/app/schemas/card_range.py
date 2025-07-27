from pydantic import BaseModel
from typing import Optional
from .player_card import PlayerCard

class CardRangeBase(BaseModel):
    min_value: float
    max_value: float
    description: Optional[str] = None
    primary_card_id: int
    fallback_card_id: Optional[int] = None

class CardRangeCreate(CardRangeBase):
    pass

class CardRangeUpdate(BaseModel):  # اضافه کردن کلاس CardRangeUpdate
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    description: Optional[str] = None
    primary_card_id: Optional[int] = None
    fallback_card_id: Optional[int] = None

class CardRange(CardRangeBase):
    id: int
    primary_card: Optional[PlayerCard] = None
    fallback_card: Optional[PlayerCard] = None

    class Config:
        from_attributes = True  # تغییر از orm_mode به from_attributes برای Pydantic V2