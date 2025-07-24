from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class PlayerCard(Base):
    __tablename__ = "playercards"

    id = Column(Integer, primary_key=True, index=True)
    # اطلاعات بازیکن
    name = Column(String, nullable=False)
    club = Column(String)
    nation = Column(String)
    league = Column(String)
    position = Column(String)
    # اطلاعات کارت
    version = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    chemistry = Column(Integer, default=0)
    is_special = Column(Boolean, default=False)
    # اطلاعات قیمت و معاملات
    bid_price = Column(Float)
    buy_now_price = Column(Float)
    last_sale_price = Column(Float)
    tax = Column(Float, default=0.05)  # مالیات 5% پیش فرض
    price_range_min = Column(Float)
    price_range_max = Column(Float)
    
    # آمار بازیکن
    games_played = Column(Integer, default=0)
    goals = Column(Integer, default=0)
    owner_count = Column(Integer, default=1)
    
    # روابط
    primary_ranges = relationship(
        "CardRange", 
        foreign_keys="[CardRange.primary_card_id]",
        back_populates="primary_card"
    )
    fallback_ranges = relationship(
        "CardRange", 
        foreign_keys="[CardRange.fallback_card_id]",
        back_populates="fallback_card"
    )
    transactions = relationship("Transaction", back_populates="card")

    # محاسبه قیمت خالص بعد از کسر مالیات
    def net_price(self, price):
        return price * (1 - self.tax)
    
@property
def transfer_methods(self):
    methods = set()
    for r in self.primary_ranges:
        methods.add(r.transfer_method)
    for r in self.fallback_ranges:
        if r.transfer_method:
            methods.add(r.transfer_method)
    return list(methods)