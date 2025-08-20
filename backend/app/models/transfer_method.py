# models/transfer_method.py

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class TransferMethod(Base):
    __tablename__ = "transfer_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Integer, default=0)
    logic = Column(String)
    transfer_multiplier = Column(Float, default=1.0)

    card_ranges = relationship("CardRange", back_populates="transfer_method", cascade="all, delete") 
