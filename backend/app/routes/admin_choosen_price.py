from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.admin_choosen_price import PriceUpdate, PriceOut
from app.crud import admin_choosen_price as price_crud

router = APIRouter(prefix="/prices", tags=["Prices"])

from app.schemas.admin_choosen_price import PriceOut

@router.get("/latest", response_model=PriceOut)
def get_latest(db: Session = Depends(get_db)):
    result = price_crud.get_latest_price(db)
    if result is None:
        return PriceOut(buy_price=0.0, sell_price=0.0)
    return result

@router.post("/", response_model=PriceOut)
def set_price(price_update: PriceUpdate, db: Session = Depends(get_db)):
    return price_crud.update_price(db, price_update)
