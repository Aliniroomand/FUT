from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.price import PriceCreate, PriceOut
from app.crud import price as price_crud

router = APIRouter(prefix="/prices", tags=["Prices"])

@router.get("/latest", response_model=PriceOut)
def get_latest(db: Session = Depends(get_db)):
    return price_crud.get_latest_price(db)

@router.post("/", response_model=PriceOut)
def set_price(price: PriceCreate, db: Session = Depends(get_db)):
    return price_crud.create_price(db, price)
