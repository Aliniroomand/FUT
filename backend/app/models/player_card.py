from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class PlayerCard(Base):
    __tablename__ = "playercards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    club = Column(String)
    position = Column(String)
    version = Column(String, nullable=False)
    rating = Column(String, nullable=False)
    chemistry = Column(Integer, default=0)
    bid_price = Column(String)
    buy_now_price = Column(String)
    games_played = Column(Integer, default=0)
    contract_number = Column(Integer, default=0)
    owner_number = Column(Integer, default=0)
    
    # Relationships with CardRange

    as_primary_ranges = relationship(
        "CardRange",
        foreign_keys="CardRange.primary_card_id",
        back_populates="primary_card"
    )

    as_fallback_ranges = relationship(
        "CardRange",
        foreign_keys="CardRange.fallback_card_id",
        back_populates="fallback_card",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

