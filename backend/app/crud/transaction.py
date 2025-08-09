from sqlalchemy.orm import Session
from app.models.transactions import Transaction
from app.schemas.transactions import TransactionCreate
from sqlalchemy import func
from datetime import datetime
from fastapi import HTTPException
from app.models.transactions import Transaction

def create(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(
        user_id=transaction.user_id,
        card_id=transaction.card_id,
        transfer_method_id=transaction.transfer_method_id,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        is_successful=transaction.is_successful,
        is_settled=transaction.is_settled,
        buy_price=transaction.buy_price,
        sell_price=transaction.sell_price,
        customer_phone=transaction.customer_phone,
        customer_email=transaction.customer_email,
        debt_or_credit=transaction.debt_or_credit,
        debt_or_credit_type=transaction.debt_or_credit_type,
        transfer_multiplier=transaction.transfer_multiplier,
        timestamp=transaction.timestamp
)

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    card_id: int = None,
    transaction_type: str = None,
    customer_phone: str = None,
    customer_email: str = None,
    is_settled: int = None,
    is_successful: int = None,
    debt_or_credit_type: str = None,
    min_amount: float = None,
    max_amount: float = None,
    start_date: str = None,
    end_date: str = None,
    sort_by: str = None,
    sort_order: str = "desc"
):
    query = db.query(Transaction)

    if card_id is not None:
        query = query.filter(Transaction.card_id == card_id)
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    if customer_phone:
        query = query.filter(Transaction.customer_phone == customer_phone)
    if customer_email:
        query = query.filter(Transaction.customer_email == customer_email)
    if is_settled is not None:
        query = query.filter(Transaction.is_settled == is_settled)
    if is_successful is not None:
        query = query.filter(Transaction.is_successful == is_successful)
    if debt_or_credit_type:
        query = query.filter(Transaction.debt_or_credit_type == debt_or_credit_type)
    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
            base_query = base_query.filter(Transaction.timestamp >= start_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS")

    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date)
            base_query = base_query.filter(Transaction.timestamp <= end_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS")
    # مرتب‌سازی
    if sort_by:
        sort_col = getattr(Transaction, sort_by, None)
        if sort_col is not None:
            if sort_order == "asc":
                query = query.order_by(sort_col.asc())
            else:
                query = query.order_by(sort_col.desc())
    else:
        query = query.order_by(Transaction.timestamp.desc())

    return query.offset(skip).limit(limit).all()

def get(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

def get_for_card(db: Session, card_id: int):
    return db.query(Transaction).filter(Transaction.card_id == card_id).all()

def get_stats_for_card(db: Session, card_id: int):
    stats = db.query(
        func.count(Transaction.id).label("total_transactions"),
        func.sum(Transaction.amount).label("total_amount"),
        func.avg(Transaction.amount).label("average_price"),
        func.max(Transaction.amount).label("max_price"),
        func.min(Transaction.amount).label("min_price")
    ).filter(Transaction.card_id == card_id).first()
    
    return {
        "total_transactions": stats.total_transactions or 0,
        "total_amount": stats.total_amount or 0,
        "average_price": stats.average_price or 0,
        "max_price": stats.max_price or 0,
        "min_price": stats.min_price or 0
    }