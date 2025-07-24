from sqlalchemy.orm import Session
from app.models.player_card import PlayerCard
from app.schemas.player_card import PlayerCardCreate, PlayerCardUpdate
from app.models.transactions import Transaction

def create(db: Session, card: PlayerCardCreate):
    db_card = PlayerCard(
        name=card.name,
        club=card.club,
        nation=card.nation,
        league=card.league,
        position=card.position,
        version=card.version,
        rating=card.rating,
        chemistry=card.chemistry,
        is_special=card.is_special,
        bid_price=card.bid_price,
        buy_now_price=card.buy_now_price,
        last_sale_price=card.last_sale_price,
        tax=card.tax,
        price_range_min=card.price_range_min,
        price_range_max=card.price_range_max,
        games_played=card.games_played,
        goals=card.goals,
        assists=card.assists,
        owner_count=card.owner_count
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def get_all(db: Session, skip: int = 0, limit: int = 100, 
            name: str = None, club: str = None, rating_min: int = None):
    query = db.query(PlayerCard)
    
    if name:
        query = query.filter(PlayerCard.name.ilike(f"%{name}%"))
    if club:
        query = query.filter(PlayerCard.club.ilike(f"%{club}%"))
    if rating_min is not None:
        query = query.filter(PlayerCard.rating >= rating_min)
    
    return query.offset(skip).limit(limit).all()

def get(db: Session, card_id: int):
    return db.query(PlayerCard).filter(PlayerCard.id == card_id).first()

def update(db: Session, card_id: int, card: PlayerCardUpdate):
    db_card = db.query(PlayerCard).filter(PlayerCard.id == card_id).first()
    if not db_card:
        return None
    
    update_data = card.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_card, key, value)
    
    db.commit()
    db.refresh(db_card)
    return db_card

def delete(db: Session, card_id: int):
    db_card = db.query(PlayerCard).filter(PlayerCard.id == card_id).first()
    if not db_card:
        return False
    db.delete(db_card)
    db.commit()
    return True

def get_transactions_for_card(db: Session, card_id: int):
    return db.query(Transaction).filter(Transaction.card_id == card_id).all()

def sell_card(db: Session, card_id: int, price: float):
    # Implement selling logic
    card = get(db, card_id)
    if not card:
        raise ValueError("Card not found")
    
    # Update card status and create transaction
    # ...
    return {"status": "sold", "price": price}

def buy_card(db: Session, card_id: int, buyer_id: int, price: float):
    # Implement buying logic
    card = get(db, card_id)
    if not card:
        raise ValueError("Card not found")
    
    # Update card status and create transaction
    # ...
    return {"status": "bought", "buyer_id": buyer_id, "price": price}