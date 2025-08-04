from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TransactionBase(BaseModel):
    user_id: int
    card_id: Optional[int] = None
    transfer_method_id: Optional[int] = None
    amount: float
    transaction_type: str
    timestamp: Optional[datetime] = None
    is_successful: Optional[int] = 0
    is_settled: Optional[int] = 0
    buy_price: Optional[float] = None
    sell_price: Optional[float] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    debt_or_credit: Optional[float] = None
    debt_or_credit_type: Optional[str] = None
    transfer_multiplier: Optional[float] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionOut(TransactionBase):
    id: int

    class Config:
        from_attributes = True