from pydantic import BaseModel

class PriceBase(BaseModel):
    buy_price: float
    sell_price: float

class PriceCreate(PriceBase):
    pass

class PriceOut(PriceBase):
    id: int

    class Config:
        orm_mode = True
