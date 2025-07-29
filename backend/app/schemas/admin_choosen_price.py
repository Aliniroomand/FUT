from pydantic import BaseModel
from typing import Optional


class PriceBase(BaseModel):
    buy_price: float
    sell_price: float

class PriceCreate(PriceBase):
    pass

class PriceOut(BaseModel):
    buy_price: float
    sell_price: float

class PriceUpdate(BaseModel):
    buy_price: Optional[float] = None
    sell_price: Optional[float] = None

model_config = {
    "from_attributes": True
}
