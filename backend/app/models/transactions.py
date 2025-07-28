# app/models/transaction.py
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey ,String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("playercards.id"))
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # خرید/فروش/انتقال
    timestamp = Column(DateTime, default=datetime.utcnow)
    