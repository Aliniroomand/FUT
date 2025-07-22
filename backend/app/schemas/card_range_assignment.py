# schemas/card_range_assignment.py
from pydantic import BaseModel
from typing import Optional

class CardRangeAssignmentCreate(BaseModel):
    method_id: int
    start_price: float
    end_price: float
    primary_card_id: int
    fallback_card_id: Optional[int] = None
