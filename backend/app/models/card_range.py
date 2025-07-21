from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CardRange(Base):
    __tablename__ = "card_ranges"

    id = Column(Integer, primary_key=True, index=True)
    min_value = Column(Integer, nullable=False)
    max_value = Column(Integer, nullable=False)
    description = Column(String)

    player_id = Column(Integer, ForeignKey("players.id"), nullable=True)  
    player = relationship("Player", back_populates="card_ranges") 
