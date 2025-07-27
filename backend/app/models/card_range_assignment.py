# models/card_range_assignment.py
from sqlalchemy import Column, Integer, Float, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class CardRangeAssignment(Base):
    __tablename__ = "card_range_assignments"

    id = Column(Integer, primary_key=True, index=True)
    method_id = Column(Integer, ForeignKey("transfer_methods.id"))  # شیوه انتقال
    start_price = Column(Float, nullable=False)  # شروع بازه
    end_price = Column(Float, nullable=False)    # پایان بازه
    primary_card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)  # کارت اصلی
    fallback_card_id = Column(Integer, ForeignKey("cards.id"), nullable=True)  # کارت جایگزین (اختیاری)

    method = relationship("TransferMethod", back_populates="ranges")
    primary_card = relationship("Card", foreign_keys=[primary_card_id])
    fallback_card = relationship("Card", foreign_keys=[fallback_card_id])
