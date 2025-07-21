from pydantic import BaseModel
from typing import Optional

class TransferCardRuleBase(BaseModel):
    card_range_id: int
    primary_card_id: int
    fallback_card_id: Optional[int] = None
    platform: str

class TransferCardRuleCreate(TransferCardRuleBase):
    pass

class TransferCardRuleOut(TransferCardRuleBase):
    id: int

    class Config:
        orm_mode = True
