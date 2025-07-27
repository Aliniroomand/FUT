from fastapi import APIRouter

router = APIRouter()

@router.get("/cards/")
def get_cards():
    return {"message": "List of cards"}
