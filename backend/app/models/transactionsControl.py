from sqlalchemy import Column, Boolean, Integer
from app.database import Base

class TransactionStatus(Base):
    __tablename__ = "transaction_status"

    id = Column(Integer, primary_key=True, index=True)
    buying_disabled = Column(Boolean, default=False)   # False = enabled
    selling_disabled = Column(Boolean, default=False)  # False = enabled
