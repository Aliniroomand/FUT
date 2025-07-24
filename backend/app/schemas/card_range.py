from pydantic import BaseModel
from typing import Optional

class CardRangeBase(BaseModel):
    min_value: int
    max_value: int
    description: Optional[str] = None
    player_card_id: int  # Changed from player_id to match relationships
    transfer_method_id: int  # Add this missing field

class CardRangeCreate(CardRangeBase):
    pass

class CardRangeUpdate(BaseModel):
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    description: Optional[str] = None

class CardRangeOut(CardRangeBase):
    id: int

    class Config:
        from_attributes = True