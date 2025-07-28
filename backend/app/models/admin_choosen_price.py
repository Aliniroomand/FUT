from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class AdminChoosenPrice(Base):
    __tablename__ = "admin_prices"

    id = Column(Integer, primary_key=True, index=True)
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
