# models/quick_sell_card.py
from sqlalchemy import Column, Integer, ForeignKey, String, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class QuickSellCardAssignment(Base):
    __tablename__ = "quick_sell_card_assignments"
    __table_args__ = (
        UniqueConstraint("card_range_id", name="uq_card_range"),  # هر بازه فقط یک کارت داشته باشه
    )

    id = Column(Integer, primary_key=True, index=True)
    card_range_id = Column(Integer, ForeignKey("card_ranges.id", ondelete="CASCADE"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="SET NULL"))
    platform = Column(Enum("ps", "xbox", "pc", name="platform_enum"), nullable=False)

    card_range = relationship("CardRange")
    card = relationship("Card")
