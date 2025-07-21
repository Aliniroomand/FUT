from pydantic import BaseModel

class CardRangeBase(BaseModel):
    min_value: int
    max_value: int
    description: str | None = None
    player_id: int | None = None

class CardRangeCreate(CardRangeBase):
    pass

class CardRangeOut(CardRangeBase):
    id: int

    class Config:
        orm_mode = True
