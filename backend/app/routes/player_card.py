from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.player_card import PlayerCardUpdate, PlayerCard
from app.schemas.transactions import TransactionOut 
from app.crud import player_card as crud
from app.schemas import player_card as schemas
from app import models  

router = APIRouter(prefix="/player-cards", tags=["Player Cards"])

@router.post("/", response_model=schemas.PlayerCard)
def create_player_card(card: schemas.PlayerCardCreate, db: Session = Depends(get_db)):
    return crud.create_player_card(db, card)

@router.get("/", response_model=list[PlayerCard])
def list_player_cards(
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    club: str = None,
    rating: str = None,
    db: Session = Depends(get_db)
):
    return crud.get_player_cards(db, skip=skip, limit=limit, name=name, club=club, rating=rating)

@router.get("/{card_id}", response_model=PlayerCard)
def get_player_card(card_id: int, db: Session = Depends(get_db)):
    card = crud.get_player_card(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="PlayerCard not found")
    return card

@router.put("/{card_id}", response_model=PlayerCard)
def update_player_card(card_id: int, card: PlayerCardUpdate, db: Session = Depends(get_db)):
    updated_card = crud.update_player_card(db, card_id, card)
    if not updated_card:
        raise HTTPException(status_code=404, detail="PlayerCard not found")
    return updated_card

@router.delete("/{card_id}")
def delete_player_card(card_id: int, db: Session = Depends(get_db)):
    success = crud.delete_player_card(db, card_id)
    if not success:
        raise HTTPException(status_code=404, detail="PlayerCard not found")
    return {"detail": "Deleted"}

@router.get("/{card_id}/transactions", response_model=list[TransactionOut])
def get_card_transactions(card_id: int, db: Session = Depends(get_db)):
    return crud.get_card_transactions(db, card_id)

@router.post("/{card_id}/sell")
def sell_player_card(card_id: int, price: str, db: Session = Depends(get_db)):
    return crud.sell_player_card(db, card_id, price)

@router.post("/{card_id}/sell")
def sell_player_card(
    card_id: int,
    min_bid_price: int,
    max_bid_price: int,
    min_buy_now_price: int,
    max_buy_now_price: int,
    db: Session = Depends(get_db)
):
    return crud.sell_player_card(
        db,
        card_id,
        min_bid_price=min_bid_price,
        max_bid_price=max_bid_price,
        min_buy_now_price=min_buy_now_price,
        max_buy_now_price=max_buy_now_price,
    )


@router.post("/{card_id}/buy")
def buy_player_card(
    card_id: int,
    buyer_id: int,
    min_bid_price: int,
    max_bid_price: int,
    min_buy_now_price: int,
    max_buy_now_price: int,
    db: Session = Depends(get_db)
):
    return crud.buy_player_card(
        db,
        card_id,
        buyer_id=buyer_id,
        min_bid_price=min_bid_price,
        max_bid_price=max_bid_price,
        min_buy_now_price=min_buy_now_price,
        max_buy_now_price=max_buy_now_price,
    )

@router.delete("/by-primary-card/{player_id}", status_code=204)
def delete_ranges_with_primary_card(player_id: int, db: Session = Depends(get_db)):
    ranges = db.query(models.CardRange).filter(models.CardRange.primary_card_id == player_id).all()
    for r in ranges:
        db.delete(r)
    db.commit()
    return
