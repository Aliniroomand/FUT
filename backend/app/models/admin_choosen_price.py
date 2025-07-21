from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class AdminChoosenPrice(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"))
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)

    card = relationship("Card", back_populates="price")
