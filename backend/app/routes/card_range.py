from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.card_range import CardRangeCreate, CardRangeUpdate, CardRangeOut
from app.crud import card_range as crud_card_range

router = APIRouter(prefix="/card-ranges", tags=["Card Ranges"])

@router.get("/", response_model=list[CardRangeOut])
def list_card_ranges(db: Session = Depends(get_db)):
    return crud_card_range.get_all(db)

@router.post("/", response_model=CardRangeOut)
def create_card_range(card_range: CardRangeCreate, db: Session = Depends(get_db)):
    return crud_card_range.create(db, card_range)

@router.get("/{id}", response_model=CardRangeOut)
def get_card_range(id: int, db: Session = Depends(get_db)):
    card_range = crud_card_range.get(db, id)
    if not card_range:
        raise HTTPException(status_code=404, detail="CardRange not found")
    return card_range

@router.put("/{id}", response_model=CardRangeOut)
def update_card_range(id: int, card_range: CardRangeUpdate, db: Session = Depends(get_db)):
    updated = crud_card_range.update(db, id, card_range)
    if updated is None:
        raise HTTPException(status_code=404, detail="CardRange not found")
    return updated

@router.delete("/{id}")
def delete_card_range(id: int, db: Session = Depends(get_db)):
    success = crud_card_range.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="CardRange not found")
    return {"detail": "Deleted successfully"}

@router.get("/card/{card_id}", response_model=list[CardRangeOut])
def get_ranges_for_card(card_id: int, db: Session = Depends(get_db)):
    return crud_card_range.get_ranges_by_card(db, card_id)