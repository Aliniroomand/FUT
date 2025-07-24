from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PlayerCardBase(BaseModel):
    name: str
    club: Optional[str] = None
    nation: Optional[str] = None
    league: Optional[str] = None
    position: Optional[str] = None
    version: str
    rating: int
    chemistry: int = 0
    is_special: bool = False
    bid_price: Optional[float] = None
    buy_now_price: Optional[float] = None
    last_sale_price: Optional[float] = None
    tax: float = 0.05
    price_range_min: Optional[float] = None
    price_range_max: Optional[float] = None
    games_played: int = 0
    goals: int = 0
    assists: int = 0
    owner_count: int = 1

class PlayerCardCreate(PlayerCardBase):
    pass

class PlayerCardUpdate(BaseModel):
    name: Optional[str] = None
    club: Optional[str] = None
    nation: Optional[str] = None
    league: Optional[str] = None
    position: Optional[str] = None
    version: Optional[str] = None
    rating: Optional[int] = None
    chemistry: Optional[int] = None
    is_special: Optional[bool] = None
    bid_price: Optional[float] = None
    buy_now_price: Optional[float] = None
    last_sale_price: Optional[float] = None
    tax: Optional[float] = None
    price_range_min: Optional[float] = None
    price_range_max: Optional[float] = None
    games_played: Optional[int] = None
    goals: Optional[int] = None
    assists: Optional[int] = None
    owner_count: Optional[int] = None

class PlayerCardOut(PlayerCardBase):
    id: int
    
    class Config:
        from_attributes = True

# Additional schemas for nested relationships
class TransferMethodSimple(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class CardRangeSimple(BaseModel):
    id: int
    min_value: float
    max_value: float
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

class PlayerCardDetail(PlayerCardOut):
    primary_ranges: List[CardRangeSimple] = []
    fallback_ranges: List[CardRangeSimple] = []
    transfer_methods: List[TransferMethodSimple] = []

class TransactionSimple(BaseModel):
    id: int
    transaction_type: str
    amount: float
    timestamp: datetime
    
    class Config:
        from_attributes = True

class PlayerCardWithTransactions(PlayerCardDetail):
    transactions: List[TransactionSimple] = []