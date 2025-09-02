# app/models/transfer_task.py
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, func, JSON
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TransferStatus(enum.Enum):
    pending = "pending"
    attempting = "attempting"
    success = "success"
    failed = "failed"

class TransferTask(Base):
    __tablename__ = "transfer_tasks"

    id = Column(Integer, primary_key=True, index=True)
    ea_account_id = Column(Integer, ForeignKey("ea_accounts.id"), nullable=False)
    player_id = Column(String, nullable=False)
    max_price = Column(Integer, nullable=False)
    status = Column(Enum(TransferStatus), default=TransferStatus.pending, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    last_error = Column(String, nullable=True)
    meta = Column(JSON, nullable=True)  # flexible field for extra info
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # relationship optional
    # ea_account = relationship("EAAccount", back_populates="transactions")
