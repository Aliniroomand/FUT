from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.deps import get_current_user
from app.schemas.transactions import TransactionCreate, TransactionOut
from app.crud import transaction as crud

router = APIRouter(prefix="/transactions", tags=["Transactions"])


from fastapi import Query
from typing import Optional
from fastapi.responses import JSONResponse

@router.get("/", response_model=None)
def list_transactions(
    skip: int = 0,
    limit: int = 20,
    card_id: Optional[int] = None,
    transaction_type: Optional[str] = None,
    customer_phone: Optional[str] = None,
    customer_email: Optional[str] = None,
    is_settled: Optional[int] = None,
    is_successful: Optional[int] = None,
    debt_or_credit_type: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    sort_by: Optional[str] = Query(None, description="Sort by field name"),
    sort_order: Optional[str] = Query("desc", description="asc or desc"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # اگر ادمین نیست فقط تراکنش‌های خودش را ببیند
    if not getattr(current_user, "is_admin", False):
        # فقط تراکنش‌های مربوط به کاربر جاری
        user_id = current_user.id
        base_query = db.query(crud.Transaction).filter(crud.Transaction.user_id == user_id)
        if card_id is not None:
            base_query = base_query.filter(crud.Transaction.card_id == card_id)
        if transaction_type:
            base_query = base_query.filter(crud.Transaction.transaction_type == transaction_type)
        if is_settled is not None:
            base_query = base_query.filter(crud.Transaction.is_settled == is_settled)
        if is_successful is not None:
            base_query = base_query.filter(crud.Transaction.is_successful == is_successful)
        if debt_or_credit_type:
            base_query = base_query.filter(crud.Transaction.debt_or_credit_type == debt_or_credit_type)
        if min_amount is not None:
            base_query = base_query.filter(crud.Transaction.amount >= min_amount)
        if max_amount is not None:
            base_query = base_query.filter(crud.Transaction.amount <= max_amount)
        if start_date:
            base_query = base_query.filter(crud.Transaction.timestamp >= start_date)
        if end_date:
            base_query = base_query.filter(crud.Transaction.timestamp <= end_date)
        total = base_query.count()
        items = base_query.order_by(crud.Transaction.timestamp.desc()).offset(skip).limit(limit).all()
    else:
        # ادمین همه تراکنش‌ها را می‌بیند
        base_query = db.query(crud.Transaction)
        if card_id is not None:
            base_query = base_query.filter(crud.Transaction.card_id == card_id)
        if transaction_type:
            base_query = base_query.filter(crud.Transaction.transaction_type == transaction_type)
        if customer_phone:
            base_query = base_query.filter(crud.Transaction.customer_phone == customer_phone)
        if customer_email:
            base_query = base_query.filter(crud.Transaction.customer_email == customer_email)
        if is_settled is not None:
            base_query = base_query.filter(crud.Transaction.is_settled == is_settled)
        if is_successful is not None:
            base_query = base_query.filter(crud.Transaction.is_successful == is_successful)
        if debt_or_credit_type:
            base_query = base_query.filter(crud.Transaction.debt_or_credit_type == debt_or_credit_type)
        if min_amount is not None:
            base_query = base_query.filter(crud.Transaction.amount >= min_amount)
        if max_amount is not None:
            base_query = base_query.filter(crud.Transaction.amount <= max_amount)
        if start_date:
            base_query = base_query.filter(crud.Transaction.timestamp >= start_date)
        if end_date:
            base_query = base_query.filter(crud.Transaction.timestamp <= end_date)
        total = base_query.count()
        # مرتب‌سازی
        if sort_by:
            sort_col = getattr(crud.Transaction, sort_by, None)
            if sort_col is not None:
                if sort_order == "asc":
                    base_query = base_query.order_by(sort_col.asc())
                else:
                    base_query = base_query.order_by(sort_col.desc())
        else:
            base_query = base_query.order_by(crud.Transaction.timestamp.desc(),crud.Transaction.id.desc() )
        items = base_query.offset(skip).limit(limit).all()

    return JSONResponse(content={
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [TransactionOut.model_validate(i).model_dump() for i in items]
    })

@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.get(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.get("/card/{card_id}", response_model=list[TransactionOut])
def get_transactions_for_card(card_id: int, db: Session = Depends(get_db)):
    return crud.get_for_card(db, card_id)

@router.post("/", response_model=TransactionOut)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    return crud.create(db, transaction)

@router.get("/stats/{card_id}")
def get_transaction_stats(card_id: int, db: Session = Depends(get_db)):
    return crud.get_stats_for_card(db, card_id)