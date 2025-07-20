from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    club = Column(String)
    nation = Column(String)
    league = Column(String)

    cards = relationship("Card", back_populates="player", cascade="all, delete")
