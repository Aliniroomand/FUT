# app/models/transaction.py
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey ,String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("playercards.id"), nullable=True)  # کارت انتقالی
    transfer_method_id = Column(Integer, ForeignKey("transfer_methods.id"), nullable=True)
    amount = Column(Float, nullable=False)  # مبلغ کل انتقال
    transaction_type = Column(String, nullable=False)  # خرید/فروش/انتقال
    timestamp = Column(DateTime, default=datetime.now())
    is_successful = Column(Integer, default=0)  # 1: موفق، 0: ناموفق
    is_settled = Column(Integer, default=0)  # 1: تسویه شده، 0: تسویه نشده
    buy_price = Column(Float, nullable=True)  # قیمت خرید سکه توسط ادمین در لحظه تراکنش
    sell_price = Column(Float, nullable=True)  # قیمت فروش سکه توسط ادمین در لحظه تراکنش
    customer_phone = Column(String, nullable=True)  # شماره مشتری برای جستجو
    customer_email = Column(String, nullable=True)  # ایمیل مشتری برای جستجو
    debt_or_credit = Column(Float, nullable=True)  # مبلغ بدهی یا طلبکاری
    debt_or_credit_type = Column(String, nullable=True)  # 'debt' یا 'credit'
    transfer_multiplier = Column(Float, nullable=True)  # ضریب انتقال از transfer_method

    # روابط
    user = relationship("User")
    card = relationship("PlayerCard")
    transfer_method = relationship("TransferMethod")
    