from sqlalchemy import Column, Integer, Float
from app.database import Base

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
