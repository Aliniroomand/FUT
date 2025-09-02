# app/models/price_cache.py
from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class PriceCache(Base):
    __tablename__ = "price_cache"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, nullable=False, index=True)
    platform = Column(String, nullable=False)
    card_type = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    currency = Column(String, default="coins")
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
