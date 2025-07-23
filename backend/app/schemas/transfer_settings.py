from pydantic import BaseModel

class TransferSettingsBase(BaseModel):
    threshold_amount: int

class TransferSettingsCreate(TransferSettingsBase):
    pass

class TransferSettingsOut(TransferSettingsBase):
    id: int

    class Config:
        orm_mode = True