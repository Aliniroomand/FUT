
from pydantic import BaseModel
from typing import List

class TransferSettingCreate(BaseModel):
    threshold_amount: int
    primary_card_ids: List[int]  # مثلاً 3 کارت برای Low/Medium/High
    platform: str

class TransferSettingOut(BaseModel):
    threshold_amount: int
