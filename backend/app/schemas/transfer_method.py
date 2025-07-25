from pydantic import BaseModel
from typing import Optional

class TransferMethodBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    logic: Optional[str] = None

class TransferMethodCreate(TransferMethodBase):
    pass

class TransferMethodUpdate(TransferMethodBase):
    pass

class TransferMethodOut(TransferMethodBase):
    id: int

    class Config:
        orm_mode = True
