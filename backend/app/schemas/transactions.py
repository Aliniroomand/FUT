from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    card_id: int
    transaction_type: str  # 'buy' or 'sell'
    amount: float
    user_id: int
    timestamp: Optional[datetime] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionOut(TransactionBase):
    id: int

    class Config:
        from_attributes = True