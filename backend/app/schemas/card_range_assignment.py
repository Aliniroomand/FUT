from pydantic import BaseModel
from typing import Optional

class CardRangeAssignmentBase(BaseModel):
    method_id: int
    start_price: float
    end_price: float
    primary_card_id: Optional[int] = None
    fallback_card_id: Optional[int] = None

class CardRangeAssignmentCreate(CardRangeAssignmentBase):
    pass

class CardRangeAssignmentOut(CardRangeAssignmentBase):
    id: int

    class Config:
        from_attributes = True