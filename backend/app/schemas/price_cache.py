from pydantic import BaseModel
from datetime import datetime


class PriceCacheOut(BaseModel):
    id: int
    player_id: str
    platform: str
    price: int
    currency: str
    fetched_at: datetime
class Config:
    from_attributes = True