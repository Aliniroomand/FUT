from sqlalchemy.orm import Session
from app.models.admin_choosen_price import AdminChoosenPrice
from app.schemas.admin_choosen_price import PriceUpdate

def get_latest_price(db: Session):
    return db.query(AdminChoosenPrice).first()

def update_price(db: Session, price_update: PriceUpdate):
    db_price = db.query(AdminChoosenPrice).first()
    if not db_price:
        db_price = AdminChoosenPrice(buy_price=0.0, sell_price=0.0)
        db.add(db_price)

    if price_update.buy_price is not None:
        db_price.buy_price = price_update.buy_price

    if price_update.sell_price is not None:
        db_price.sell_price = price_update.sell_price

    db.commit()
    db.refresh(db_price)
    return db_price
