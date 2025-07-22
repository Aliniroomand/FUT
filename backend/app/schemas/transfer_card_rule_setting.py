from pydantic import BaseModel

class TransferSettingCreate(BaseModel):
    threshold_amount: int

class TransferSettingOut(BaseModel):
    id: int
    threshold_amount: int

    class Config:
        orm_mode = True
