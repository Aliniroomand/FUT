from sqlalchemy import Column, Integer, String, Boolean, Text  # Text برای منطق بهتر از String هست
from app.database import Base
from sqlalchemy.orm import relationship


class TransferMethod(Base):
    __tablename__ = "transfer_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    logic = Column(Text, nullable=True)  
    ranges = relationship("CardRangeAssignment", back_populates="method", cascade="all, delete")

