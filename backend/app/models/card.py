from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    version = Column(String)        # Gold, TOTW, TOTS...
    rating = Column(Integer)
    position = Column(String)
    image_url = Column(String)

    # Info
    weak_foot = Column(Integer)
    skill_moves = Column(Integer)
    work_rate = Column(String)
    foot = Column(String)
    height = Column(String)
    weight = Column(String)
    birth_date = Column(String)

    # Stats
    pace = Column(Integer)
    shooting = Column(Integer)
    passing = Column(Integer)
    dribbling = Column(Integer)
    defending = Column(Integer)
    physicality = Column(Integer)

    # Prices
    price_ps = Column(Integer)
    price_xbox = Column(Integer)
    price_pc = Column(Integer)
    last_update = Column(String)

    # رابطه با بازیکن
    player = relationship("Player", back_populates="cards")
