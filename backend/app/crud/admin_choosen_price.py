from sqlalchemy.orm import Session
from app.models.admin_choosen_price import AdminChoosenPrice
from app.schemas.admin_choosen_price import PriceCreate

def get_latest_price(db: Session):
    return db.query(AdminChoosenPrice).order_by(AdminChoosenPrice.id.desc()).first()

def create_price(db: Session, price: PriceCreate):
    db_price = AdminChoosenPrice(**price.model_dump())
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price
