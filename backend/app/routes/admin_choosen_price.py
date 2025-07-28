from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.admin_choosen_price import PriceCreate, PriceOut
from app.crud import admin_choosen_price as price_crud

router = APIRouter(prefix="/prices", tags=["Prices"])

@router.get("/latest", response_model=PriceOut)
def get_latest(db: Session = Depends(get_db)):
    result = price_crud.get_latest_price(db)
    if result is None:
        raise HTTPException(status_code=404, detail="No price found")
    return result

@router.post("/", response_model=PriceOut)
def set_price(price: PriceCreate, db: Session = Depends(get_db)):
    return price_crud.create_price(db, price)
