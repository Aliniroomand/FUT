from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"))
    price_range_id = Column(Integer, ForeignKey("card_ranges.id", ondelete="SET NULL"), nullable=True)

    player = relationship("Player", back_populates="cards")
    price_range = relationship("CardRange")
    price = relationship("Price", uselist=False, back_populates="card", cascade="all, delete")
