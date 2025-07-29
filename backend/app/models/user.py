from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=True)
    telegram_id = Column(String, unique=True, nullable=True)
    reset_token = Column(String, nullable=True)

    profile = relationship("UserProfile", back_populates="user", uselist=False)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    first_name = Column(String)
    last_name = Column(String)
    card_number = Column(String)
    bank_account_number = Column(String)
    bank_account_name = Column(String)

    user = relationship("User", back_populates="profile")
