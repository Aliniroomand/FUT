from pydantic import BaseModel
from typing import List, Optional

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

    price_ps: Optional[int]
    price_xbox: Optional[int]
    price_pc: Optional[int]
    last_update: Optional[str]

    price_range_id: Optional[int]  # آیدی بازه قیمتی


class CardCreate(CardBase):
    pass

class Card(CardBase):
    id: int
    player_id: int

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
