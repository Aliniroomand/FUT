# app/routes/transaction.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, Any
from fastapi.responses import JSONResponse
import traceback
import sys
from datetime import datetime
from sqlalchemy.orm.state import InstanceState

from app.database import get_db
from app.utils.deps import get_current_user
from app.schemas.transactions import TransactionCreate, TransactionOut, TransactionResponse
from app.crud import transaction as crud
from app.models.transactions import Transaction as TransactionModel
from app.models.ea_account import EAAccount, EAAccountStatus
from app.models.alert import Alert, AlertType

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def to_serializable(item: Any):
    if isinstance(item, dict):
        return {k: to_serializable(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [to_serializable(i) for i in item]
    elif hasattr(item, "__dict__"):
        return {k: to_serializable(v) for k, v in vars(item).items() if not k.startswith('_')}
    elif isinstance(item, datetime):
        return item.isoformat()
    elif isinstance(item, InstanceState):
        return None
    return item


@router.get("/", response_model=None)
def list_transactions(
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
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    لیست تراکنش‌ها با پشتیبانی از:
    - pagination (skip, limit)
    - فیلترها
    - مرتب‌سازی
    """
    try:
        if not getattr(current_user, "is_admin", False):
            query = db.query(TransactionModel).filter(
                (TransactionModel.customer_phone == current_user.phone) |
                (TransactionModel.customer_email == current_user.email)
            )
        else:
            query = db.query(TransactionModel)

        # ===== فیلترها =====
        if card_id is not None:
            query = query.filter(TransactionModel.card_id == card_id)
        if transaction_type:
            query = query.filter(TransactionModel.transaction_type == transaction_type)
        if customer_phone:
            query = query.filter(TransactionModel.customer_phone.contains(customer_phone))
        if customer_email:
            query = query.filter(TransactionModel.customer_email.contains(customer_email))
        if is_settled is not None:
            query = query.filter(TransactionModel.is_settled == is_settled)
        if is_successful is not None:
            query = query.filter(TransactionModel.is_successful == is_successful)
        if debt_or_credit_type:
            query = query.filter(TransactionModel.debt_or_credit_type == debt_or_credit_type)
        if min_amount is not None:
            query = query.filter(TransactionModel.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(TransactionModel.amount <= max_amount)
        if start_date:
            try:
                sd = datetime.fromisoformat(start_date)
                query = query.filter(TransactionModel.timestamp >= sd)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid start_date format. Use ISO format")
        if end_date:
            try:
                ed = datetime.fromisoformat(end_date)
                query = query.filter(TransactionModel.timestamp <= ed)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid end_date format. Use ISO format")

        # ===== مرتب‌سازی =====
        if sort_by and hasattr(TransactionModel, sort_by):
            sort_col = getattr(TransactionModel, sort_by)
            if sort_order == "asc":
                query = query.order_by(sort_col.asc())
            else:
                query = query.order_by(sort_col.desc())
        else:
            query = query.order_by(TransactionModel.timestamp.desc(), TransactionModel.id.desc())

        # ===== total =====
        total = query.count()

        # ===== pagination =====
        items = query.offset(skip).limit(limit).all()
        serialized = [to_serializable(i) for i in items]

        return JSONResponse(content={
            "items": serialized,
            "total": total
        })

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        raise HTTPException(status_code=500, detail="Internal server error while listing transactions")


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.get(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.get("/card/{card_id}", response_model=list[TransactionOut])
def get_transactions_for_card(card_id: int, db: Session = Depends(get_db)):
    return crud.get_for_card(db, card_id)


@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    ea_account = db.query(EAAccount).filter(EAAccount.id == transaction.account_id).first()
    if ea_account:
        if ea_account.status == EAAccountStatus.paused:
            alert = Alert(
                account_id=ea_account.id,
                type=AlertType.ERROR,
                message=f"تلاش برای تراکنش با اکانت {ea_account.name} که وضعیت آن paused است.",
                created_at=datetime.utcnow()
            )
            db.add(alert)
            db.commit()
            raise HTTPException(status_code=400, detail="این اکانت غیرفعال است و نمی‌توان تراکنش انجام داد.")

    created_transaction = crud.create(db, transaction)

    if ea_account:
        ea_account.transferred_today += transaction.amount
        ea_account.last_transfer_time = datetime.utcnow()
        if ea_account.daily_limit and ea_account.transferred_today >= ea_account.daily_limit:
            ea_account.status = EAAccountStatus.paused
        db.commit()

    next_account = (
        db.query(EAAccount)
        .filter(EAAccount.is_user_account == False, EAAccount.id != transaction.account_id)
        .order_by(EAAccount.id)
        .first()
    )

    return {"transaction": created_transaction, "next_account": next_account}


@router.get("/stats/{card_id}")
def get_transaction_stats(card_id: int, db: Session = Depends(get_db)):
    return crud.get_stats_for_card(db, card_id)
