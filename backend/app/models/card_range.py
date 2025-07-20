from sqlalchemy import Column, Integer, String
from app.database import Base

class CardRange(Base):
    __tablename__ = "card_ranges"  # اسم دقیق جدول باید همین باشد

    id = Column(Integer, primary_key=True, index=True)
    min_value = Column(Integer, nullable=False)
    max_value = Column(Integer, nullable=False)
    description = Column(String)
