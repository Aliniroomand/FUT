from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.transactions import TransactionCreate, TransactionOut
from app.crud import transaction as crud

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/", response_model=list[TransactionOut])
def list_transactions(
    skip: int = 0,
    limit: int = 100,
    card_id: int = None,
    transaction_type: str = None,
    db: Session = Depends(get_db)
):
    return crud.get_all(db, skip=skip, limit=limit, card_id=card_id, transaction_type=transaction_type)

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