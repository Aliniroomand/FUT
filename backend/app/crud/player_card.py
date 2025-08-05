from sqlalchemy.orm import Session
from app.models.player_card import PlayerCard
from app.schemas.player_card import PlayerCardCreate, PlayerCardUpdate
from app.models.transactions import Transaction


def create_player_card(db: Session, player_card: PlayerCardCreate):
    db_player_card = PlayerCard(
        name=player_card.name,
        club=player_card.club,
        position=player_card.position,
        version=player_card.version,
        rating=player_card.rating,
        chemistry=player_card.chemistry,
        min_bid_price=player_card.min_bid_price,
        max_bid_price=player_card.max_bid_price,
        min_buy_now_price=player_card.min_buy_now_price,
        max_buy_now_price=player_card.max_buy_now_price,
        games_played=player_card.games_played,
        contract_number=player_card.contract_number,
        owner_number=player_card.owner_number
    )
    db.add(db_player_card)
    db.commit()
    db.refresh(db_player_card)
    return db_player_card


def get_player_card(db: Session, player_card_id: int):
    return db.query(PlayerCard).filter(PlayerCard.id == player_card_id).first()

def get_player_cards(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    club: str = None,
    rating: str = None
):
    query = db.query(PlayerCard)
    
    if name:
        query = query.filter(PlayerCard.name.ilike(f"%{name}%"))
    if club:
        query = query.filter(PlayerCard.club.ilike(f"%{club}%"))
    if rating:
        query = query.filter(PlayerCard.rating == rating)
    
    return query.offset(skip).limit(limit).all()

def update_player_card(db: Session, player_card_id: int, player_card: PlayerCardUpdate):
    db_player_card = db.query(PlayerCard).filter(PlayerCard.id == player_card_id).first()
    if not db_player_card:
        return None
    
    update_data = player_card.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_player_card, key, value)
    
    db.commit()
    db.refresh(db_player_card)
    return db_player_card

def delete_player_card(db: Session, player_card_id: int):
    db_player_card = db.query(PlayerCard).filter(PlayerCard.id == player_card_id).first()
    if not db_player_card:
        return False
    
    db.delete(db_player_card)
    db.commit()
    return True

def get_card_transactions(db: Session, card_id: int):
    return db.query(Transaction).filter(Transaction.card_id == card_id).all()

def sell_player_card(
    db: Session,
    card_id: int,
    min_bid_price: int,
    max_bid_price: int,
    min_buy_now_price: int,
    max_buy_now_price: int,
):
    card = get_player_card(db, card_id)
    if not card:
        raise ValueError("Player card not found")
    
    # آپدیت قیمت‌ها
    card.min_bid_price = min_bid_price
    card.max_bid_price = max_bid_price
    card.min_buy_now_price = min_buy_now_price
    card.max_buy_now_price = max_buy_now_price

    db.commit()
    db.refresh(card)
    
    return {
        "status": "listed_for_sale",
        "card_id": card_id,
        "min_bid_price": min_bid_price,
        "max_bid_price": max_bid_price,
        "min_buy_now_price": min_buy_now_price,
        "max_buy_now_price": max_buy_now_price,
    }


def buy_player_card(
    db: Session,
    card_id: int,
    buyer_id: int,
    min_bid_price: int,
    max_bid_price: int,
    min_buy_now_price: int,
    max_buy_now_price: int,
):
    card = get_player_card(db, card_id)
    if not card:
        raise ValueError("Player card not found")

    # ثبت قیمت‌های خرید واقعی
    card.min_bid_price = min_bid_price
    card.max_bid_price = max_bid_price
    card.min_buy_now_price = min_buy_now_price
    card.max_buy_now_price = max_buy_now_price



    db.commit()
    db.refresh(card)

    return {
        "status": "purchased",
        "buyer_id": buyer_id,
        "card_id": card_id,
        "min_bid_price": min_bid_price,
        "max_bid_price": max_bid_price,
        "min_buy_now_price": min_buy_now_price,
        "max_buy_now_price": max_buy_now_price,
    }