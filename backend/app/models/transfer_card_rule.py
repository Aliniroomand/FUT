# models/transfer_card_rule.py

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class TransferCardRule(Base):
    __tablename__ = "transfer_card_rules"

    id = Column(Integer, primary_key=True, index=True)

    card_range_id = Column(Integer, ForeignKey("card_ranges.id"), nullable=False)
    primary_card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    fallback_card_id = Column(Integer, ForeignKey("cards.id"), nullable=True)

    platform = Column(String, nullable=True) 

    card_range = relationship("CardRange", backref="transfer_rules")
    primary_card = relationship("Card", foreign_keys=[primary_card_id])
    fallback_card = relationship("Card", foreign_keys=[fallback_card_id])
