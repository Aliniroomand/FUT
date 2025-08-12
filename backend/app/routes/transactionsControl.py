from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import transactionsControl as crud

router = APIRouter()

@router.get("/transaction-status")
def get_transaction_status(db: Session = Depends(get_db)):
    return crud.get_status(db)

@router.patch("/transaction-status")
def update_transaction_status(
    buying_disabled: bool = None,
    selling_disabled: bool = None,
    db: Session = Depends(get_db)
):
    return crud.update_status(db, buying_disabled, selling_disabled)
