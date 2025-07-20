from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class TransferMethod(Base):
    __tablename__ = "transfer_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
