from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from sqlalchemy.sql import func

class EAAccountStatus(enum.Enum):
    active = "active"
    paused = "paused"
    banned = "banned"

class EAAccount(Base):
    __tablename__ = "ea_accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    platform = Column(String, nullable=False)
    daily_limit = Column(Integer, nullable=True)
    transferred_today = Column(Integer, default=0, nullable=False)
    last_transfer_time = Column(DateTime, nullable=True)
    status = Column(Enum(EAAccountStatus), default=EAAccountStatus.active, nullable=False)
    paused_until = Column(DateTime, nullable=True)
    is_user_account = Column(Boolean, default=False, nullable=False)
    session_token = Column(String, nullable=True)
    last_captcha_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    transactions = relationship("Transaction", back_populates="ea_account")
    alerts = relationship("Alert", back_populates="ea_account")
