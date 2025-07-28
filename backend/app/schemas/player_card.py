from pydantic import BaseModel
from typing import Optional, List

class PlayerCardBase(BaseModel):
    name: str
    club: Optional[str] = None
    position: Optional[str] = None
    version: str
    rating: str
    chemistry: int = 0
    bid_price: Optional[str] = None
    buy_now_price: Optional[str] = None
    price_range_min: Optional[str] = None
    price_range_max: Optional[str] = None
    games_played: int = 0
    contract_number: int = 0
    owner_number: int = 0

class PlayerCardCreate(PlayerCardBase):
    pass

class PlayerCardUpdate(BaseModel):
    name: Optional[str] = None
    club: Optional[str] = None
    position: Optional[str] = None
    version: Optional[str] = None
    rating: Optional[str] = None
    chemistry: Optional[int] = None
    bid_price: Optional[str] = None
    buy_now_price: Optional[str] = None
    price_range_min: Optional[str] = None
    price_range_max: Optional[str] = None
    games_played: Optional[int] = None
    contract_number: Optional[int] = None
    owner_number: Optional[int] = None

class PlayerCard(PlayerCardBase):
    id: int

    class Config:
        from_attributes = True

# برای نمایش استفاده بازیکن در بازه‌ها
class CardRangeShort(BaseModel):
    id: int
    min_value: int
    max_value: int

class PlayerUsageResponse(BaseModel):
    is_used: bool
    ranges: List[CardRangeShort]
