from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from app.database import Base

class CoinPrice(Base):
    __tablename__ = "coin_prices"

    id = Column(Integer, primary_key=True, index=True)
    buy_price_ps = Column(Float)
    sell_price_ps = Column(Float)
    buy_price_xbox = Column(Float)
    sell_price_xbox = Column(Float)
    buy_price_pc = Column(Float)
    sell_price_pc = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
