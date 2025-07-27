from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.transfer_method import TransferMethodCreate, TransferMethodUpdate, TransferMethodOut
from app.schemas.card_range import CardRange  # Import اضافه شده
from app.crud import transfer_method as crud

router = APIRouter(prefix="/transfer-methods", tags=["Transfer Methods"])

@router.get("/", response_model=List[TransferMethodOut])
def list_methods(db: Session = Depends(get_db)):
    return crud.get_all(db)

@router.post("/", response_model=TransferMethodOut)
def create_method(method: TransferMethodCreate, db: Session = Depends(get_db)):
    return crud.create(db, method)

@router.get("/{method_id}", response_model=TransferMethodOut)
def get_method(method_id: int, db: Session = Depends(get_db)):
    method = crud.get(db, method_id)
    if not method:
        raise HTTPException(status_code=404, detail="Method not found")
    return method

@router.put("/{method_id}", response_model=TransferMethodOut)
def update_method(method_id: int, method: TransferMethodUpdate, db: Session = Depends(get_db)):
    updated = crud.update(db, method_id, method)
    if not updated:
        raise HTTPException(status_code=404, detail="Method not found")
    return updated

@router.delete("/{method_id}", status_code=204)
def delete_method(method_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete(db, method_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Method not found")
    return

@router.get("/{method_id}/ranges", response_model=List[CardRange])
def get_ranges_for_method(method_id: int, db: Session = Depends(get_db)):
    return crud.get_ranges_for_method(db, method_id)