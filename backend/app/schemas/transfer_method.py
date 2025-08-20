from pydantic import BaseModel
from typing import Optional

class TransferMethodBase(BaseModel):
    description: Optional[str] = None
    is_active: bool = True
    logic: Optional[str] = None
    name: str
    description: Optional[str] = None
    is_active: bool = True
    logic: Optional[str] = None
    transfer_multiplier: Optional[float] = 1.0

class TransferMethodCreate(TransferMethodBase):
    pass

class TransferMethodUpdate(TransferMethodBase):
    pass

class TransferMethodOut(TransferMethodBase):

    class Config:
        from_attributes = True
    id: int

    class Config:
        from_attributes = True