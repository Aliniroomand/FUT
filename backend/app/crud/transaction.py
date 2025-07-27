from sqlalchemy.orm import Session
from app.models.transactions import Transaction
from app.schemas.transactions import TransactionCreate
from sqlalchemy import func

def create(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(
        card_id=transaction.card_id,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        user_id=transaction.user_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_all(db: Session, skip: int = 0, limit: int = 100, 
            card_id: int = None, transaction_type: str = None):
    query = db.query(Transaction)
    
    if card_id is not None:
        query = query.filter(Transaction.card_id == card_id)
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    
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