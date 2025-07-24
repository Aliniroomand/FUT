from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.player_card import PlayerCardCreate, PlayerCardUpdate, PlayerCardOut
from app.schemas.transactions import TransactionOut 
from app.crud import player_card as crud

router = APIRouter(prefix="/player-cards", tags=["Player Cards"])

@router.post("/", response_model=PlayerCardOut)
def create_player_card(card: PlayerCardCreate, db: Session = Depends(get_db)):
    return crud.create(db, card)

@router.get("/", response_model=list[PlayerCardOut])
def list_player_cards(
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    club: str = None,
    rating_min: int = None,
    db: Session = Depends(get_db)
):
    return crud.get_all(db, skip=skip, limit=limit, name=name, club=club, rating_min=rating_min)

@router.get("/{card_id}", response_model=PlayerCardOut)
def get_player_card(card_id: int, db: Session = Depends(get_db)):
    card = crud.get(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="PlayerCard not found")
    return card

@router.put("/{card_id}", response_model=PlayerCardOut)
def update_player_card(card_id: int, card: PlayerCardUpdate, db: Session = Depends(get_db)):
    updated_card = crud.update(db, card_id, card)
    if not updated_card:
        raise HTTPException(status_code=404, detail="PlayerCard not found")
    return updated_card

@router.delete("/{card_id}")
def delete_player_card(card_id: int, db: Session = Depends(get_db)):
    success = crud.delete(db, card_id)
    if not success:
        raise HTTPException(status_code=404, detail="PlayerCard not found")
    return {"detail": "Deleted"}

@router.get("/{card_id}/transactions", response_model=list[TransactionOut])
def get_card_transactions(card_id: int, db: Session = Depends(get_db)):
    return crud.get_transactions_for_card(db, card_id)

@router.post("/{card_id}/sell")
def sell_player_card(card_id: int, price: float, db: Session = Depends(get_db)):
    return crud.sell_card(db, card_id, price)

@router.post("/{card_id}/buy")
def buy_player_card(card_id: int, buyer_id: int, price: float, db: Session = Depends(get_db)):
    return crud.buy_card(db, card_id, buyer_id, price)