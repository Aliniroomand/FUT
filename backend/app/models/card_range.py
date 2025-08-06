# models/card_range.py

from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CardRange(Base):
    __tablename__ = "card_ranges"

    id = Column(Integer, primary_key=True, index=True)
    min_value = Column(Float, nullable=False)
    max_value = Column(Float, nullable=False)
    description = Column(String)

    primary_card_id = Column(Integer, ForeignKey("playercards.id"))
    fallback_card_id = Column(Integer, ForeignKey("playercards.id", ondelete="CASCADE"), nullable=True)

    transfer_method_id = Column(Integer, ForeignKey("transfer_methods.id"), nullable=False) 

    primary_card = relationship("PlayerCard", foreign_keys=[primary_card_id], back_populates="as_primary_ranges")
    fallback_card = relationship("PlayerCard", foreign_keys=[fallback_card_id], back_populates="as_fallback_ranges")

    transfer_method = relationship("TransferMethod", back_populates="card_ranges")  
