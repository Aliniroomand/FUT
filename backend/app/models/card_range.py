
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.transfer_method import TransferMethod 

class CardRange(Base):
    __tablename__ = "card_ranges"

    id = Column(Integer, primary_key=True, index=True)
    min_value = Column(Float, nullable=False)  # از Float استفاده می‌کنیم چون قیمت‌ها اعشاری هستند
    max_value = Column(Float, nullable=False)
    description = Column(String)
    

    transfer_method_id = Column(Integer, ForeignKey("transfer_methods.id"), nullable=False)

    transfer_method = relationship("TransferMethod", back_populates="card_ranges")

    
    # کارت‌های مرتبط
    primary_card_id = Column(Integer, ForeignKey("playercards.id"))
    fallback_card_id = Column(Integer, ForeignKey("playercards.id"), nullable=True)
    
    # روابط
    primary_card = relationship(
        "PlayerCard", 
        foreign_keys=[primary_card_id],
        back_populates="primary_ranges"
    )
    
    fallback_card = relationship(
        "PlayerCard", 
        foreign_keys=[fallback_card_id],
        back_populates="fallback_ranges"
    )