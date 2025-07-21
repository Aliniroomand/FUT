from sqlalchemy import Column, Integer
from app.database import Base

class TransferSettings(Base):
    __tablename__ = "transfer_settings"
    id = Column(Integer, primary_key=True, index=True)
    threshold_amount = Column(Integer, nullable=False)  # همون n
