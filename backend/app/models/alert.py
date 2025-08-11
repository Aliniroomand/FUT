from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func
import enum

class AlertType(enum.Enum):
    CAPTCHA = "CAPTCHA"
    RATE_LIMIT = "RATE_LIMIT"
    ERROR = "ERROR"

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("ea_accounts.id"), nullable=False)
    type = Column(Enum(AlertType), nullable=False)
    message = Column(String, nullable=False)
    resolved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    ea_account = relationship("EAAccount", back_populates="alerts")
