from pydantic import BaseModel
from typing import List, Optional

class PriceBase(BaseModel):
    buy_price: float
    sell_price: float

class PriceCreate(PriceBase):
    pass

class Price(PriceBase):
    id: int
    card_id: int

    class Config:
        orm_mode = True

class CardBase(BaseModel):
    version: Optional[str]
    rating: Optional[int]
    position: Optional[str]
    image_url: Optional[str]

    weak_foot: Optional[int]
    skill_moves: Optional[int]
    work_rate: Optional[str]
    foot: Optional[str]
    height: Optional[str]
    weight: Optional[str]
    birth_date: Optional[str]

    pace: Optional[int]
    shooting: Optional[int]
    passing: Optional[int]
    dribbling: Optional[int]
    defending: Optional[int]
    physicality: Optional[int]

    price_range_id: int  # حتماً لازم باشه

class CardCreate(CardBase):
    price: Optional[PriceCreate] = None

class Card(CardBase):
    id: int
    player_id: int
    price: Optional[Price]

    class Config:
        orm_mode = True

class PlayerBase(BaseModel):
    name: str
    club: Optional[str]
    nation: Optional[str]
    league: Optional[str]

class PlayerCreate(PlayerBase):
    cards: List[CardCreate] = []

class Player(PlayerBase):
    id: int
    cards: List[Card] = []

    class Config:
        orm_mode = True
