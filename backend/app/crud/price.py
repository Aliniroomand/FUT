from sqlalchemy.orm import Session
from app.models.price import Price
from app.schemas.price import PriceCreate

def get_latest_price(db: Session):
    return db.query(Price).order_by(Price.id.desc()).first()

def create_price(db: Session, price: PriceCreate):
    db_price = Price(**price.model_dump())
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price
