from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.player import Player, PlayerCreate
from app.crud import player as crud_player

router = APIRouter(prefix="/players", tags=["Players"])

@router.post("/", response_model=Player)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    return crud_player.create_player(db, player)

@router.get("/", response_model=list[Player])
def list_players(db: Session = Depends(get_db)):
    return crud_player.get_all_players(db)

@router.get("/{player_id}", response_model=Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    return crud_player.get_player_by_id(db, player_id)
