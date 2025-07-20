from sqlalchemy.orm import Session
from app.models.player import Player
from app.models.card import Card
from app.schemas.player import PlayerCreate

def create_player(db: Session, player_data: PlayerCreate):
    db_player = Player(
        name=player_data.name,
        club=player_data.club,
        nation=player_data.nation,
        league=player_data.league,
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    for card in player_data.cards:
        # کارت رو ایجاد می‌کنیم بدون قیمت (Price) چون جداست
        db_card = Card(
            version=card.version,
            rating=card.rating,
            price_range_id=card.price_range_id,
            player_id=db_player.id
        )
        db.add(db_card)
        db.commit()
        db.refresh(db_card)

        # اگر قیمت (Price) هم همراه کارت داده شده بود، ایجاد می‌کنیم
        if hasattr(card, "price") and card.price:
            from app.models.price import Price
            db_price = Price(
                buy_price=card.price.buy_price,
                sell_price=card.price.sell_price,
                card_id=db_card.id
            )
            db.add(db_price)
            db.commit()

    return db_player

def get_all_players(db: Session):
    return db.query(Player).all()

def get_player_by_id(db: Session, player_id: int):
    return db.query(Player).filter(Player.id == player_id).first()
