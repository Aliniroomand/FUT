from sqlalchemy import Column, Integer, String, Boolean, Text  
from app.database import Base
from sqlalchemy.orm import relationship


class TransferMethod(Base):
    __tablename__ = "transfer_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    logic = Column(Text, nullable=True)
    
    # تغییر رابطه: اکنون مستقیماً به CardRange مرتبط است
    card_ranges = relationship("CardRange", back_populates="transfer_method")
