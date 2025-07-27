from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.card_range_assignment import CardRangeAssignmentCreate
from crud import card_range_assignment
from database import get_db

router = APIRouter(prefix="/admin/transfer-ranges", tags=["Admin - Transfer Ranges"])

@router.post("/")
def create_assignment(data: CardRangeAssignmentCreate, db: Session = Depends(get_db)):
    return card_range_assignment.create_range_assignment(db, data)

@router.get("/{method_id}")
def list_assignments(method_id: int, db: Session = Depends(get_db)):
    return card_range_assignment.get_ranges_by_method(db, method_id)
