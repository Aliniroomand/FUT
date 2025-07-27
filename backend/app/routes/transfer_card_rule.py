from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.transfer_card_rule import TransferCardRuleCreate, TransferCardRuleOut
from app.crud import transfer_card_rule as crud

router = APIRouter(prefix="/transfer-card-rules", tags=["Transfer Card Rules"])

@router.get("/", response_model=list[TransferCardRuleOut])
def list_rules(db: Session = Depends(get_db)):
    return crud.get_all(db)

@router.post("/", response_model=TransferCardRuleOut)
def create_rule(rule: TransferCardRuleCreate, db: Session = Depends(get_db)):
    return crud.create(db, rule)

@router.put("/{rule_id}", response_model=TransferCardRuleOut)
def update_rule(rule_id: int, rule: TransferCardRuleCreate, db: Session = Depends(get_db)):
    updated = crud.update(db, rule_id, rule)
    if updated is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return updated

@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    success = crud.delete(db, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"detail": "Deleted"}
