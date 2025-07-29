from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class AdminChoosenPrice(Base):
    __tablename__ = "admin_prices"

    id = Column(Float, primary_key=True, default=1)
    buy_price = Column(Float, nullable=False, default=0.0)
    sell_price = Column(Float, nullable=False, default=0.0)
