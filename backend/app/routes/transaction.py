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
from app.schemas.transactions import TransactionCreate, TransactionOut
from app.crud import transaction as crud
from app.models.transactions import Transaction as TransactionModel  # برای فیلتر در صورت نیاز

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def to_serializable(item: Any):
    """
    تبدیل آیتم به dict قابل بازگشت به کلاینت.
    - اگر item از نوع dict باشد مستقیم بازگردانده می‌شود.
    - اگر ORM instance باشد ابتدا سعی می‌کنیم با pydantic v2 آن را serialize کنیم،
      اگر نشد تلاش می‌کنیم pydantic v1 را استفاده کنیم،
      اگر باز هم نشد به‌صورت دستی ستون‌ها را استخراج می‌کنیم.
    """
    if isinstance(item, dict):
        return {k: to_serializable(v) for k, v in item.items()}
    elif isinstance(item, list):
        return [to_serializable(i) for i in item]
    elif hasattr(item, "__dict__"):
        return {k: to_serializable(v) for k, v in vars(item).items() if not k.startswith('_')}
    elif isinstance(item, datetime):
        return item.isoformat()
    elif isinstance(item, InstanceState):
        return None  # Skip SQLAlchemy internal state
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
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    لیست تراکنش‌ها با پشتیبانی از:
    - pagination (skip, limit)
    - فیلترها (card_id, transaction_type, customer_phone, ...)
    - sort_by, sort_order
    اگر کاربر ادمین نباشد فقط تراکنش‌های خودش را مشاهده می‌کند.
    """

    try:
        # اگر شما crud.get_all را با پارامتر user_id ارتقا نداده‌اید،
        # روش ایمن: برای admin از crud.get_all استفاده کن، برای کاربر عادی از یک base_query استفاده کن.
        if not getattr(current_user, "is_admin", False):
            # کاربر عادی — فیلتر در سطح query انجام می‌شود تا total درست باشد
            query = db.query(TransactionModel).filter(
                (TransactionModel.customer_phone == current_user.phone) |
                (TransactionModel.customer_email == current_user.email)
            )

        else:
            # ادمین — از crud.get_all استفاده می‌کنیم (که شامل fallback هم می‌شود)
            query = db.query(TransactionModel)

        if card_id is not None:
            query = query.filter(TransactionModel.card_id == card_id)
        if transaction_type:
            query = query.filter(TransactionModel.transaction_type == transaction_type)
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
            # قبول رشته ISO؛ برای یکپارچگی بهتر اجازه بده crud هم handle کنه، ولی اینجا امن parse می‌کنیم
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

        # مرتب‌سازی
        if sort_by and hasattr(TransactionModel, sort_by):
            sort_col = getattr(TransactionModel, sort_by)
            if sort_order == "asc":
                query = query.order_by(sort_col.asc())
            else:
                query = query.order_by(sort_col.desc())
        else:
            query = query.order_by(TransactionModel.timestamp.desc(), TransactionModel.id.desc())

        items = query.all()
        serialized = [to_serializable(i) for i in items]

        return JSONResponse(content={
            "items": serialized
        })

    except HTTPException:
        # از HTTPException های صریح عبور بده
        raise
    except Exception as e:
        # لاگ کامل traceback برای دیباگ
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


@router.post("/", response_model=TransactionOut)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    return crud.create(db, transaction)


@router.get("/stats/{card_id}")
def get_transaction_stats(card_id: int, db: Session = Depends(get_db)):
    return crud.get_stats_for_card(db, card_id)
