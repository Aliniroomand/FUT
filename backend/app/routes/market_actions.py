# app/routes/market_actions.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import ea_account as ea_crud
from app.models.transfer_task import TransferTask, TransferStatus
from app.database import SessionLocal
from datetime import datetime
import json

router = APIRouter(prefix="/market", tags=["Market"])

class BuyRequest(BaseModel):
    player_id: str
    ea_account_id: int
    max_price: int

@router.post("/buy")
def enqueue_buy(req: BuyRequest, db: Session = Depends(get_db)):
    # validate account
    account = db.query(ea_crud.EAAccount).filter_by(id=req.ea_account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="EA account not found")
    # create TransferTask
    task = TransferTask(
        ea_account_id=req.ea_account_id,
        player_id=req.player_id,
        max_price=req.max_price,
        status=TransferStatus.pending
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    # Here we assume background worker will pick up pending tasks.
    return {"message": "Enqueued", "task_id": task.id}
