from app.routes import admin_choosen_price,transfer_card_rule_setting
from fastapi import FastAPI
from app.routes import player, transfer_method, card,card_range , admin_choosen_price,transfer_card_rule
from app.routes import transfer_range_setting
from app.database import engine, Base
from app.models.player import Player
from app.models.card import Card
from app.models.card_range import CardRange


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(player.router)
app.include_router(admin_choosen_price.router)
app.include_router(transfer_method.router)
app.include_router(card.router)
app.include_router(card_range.router)
app.include_router(transfer_card_rule.router)
app.include_router(transfer_card_rule_setting.router)
app.include_router(transfer_range_setting.router)



# این رو برای دیپلوی حتما پاک کن !!!!!!!!!!!

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # اجازه به همه دامنه‌ها (در توسعه مشکلی نیست)
    allow_credentials=True,
    allow_methods=["*"],  # همه متدها مثل GET, POST, PUT, DELETE
    allow_headers=["*"],  # همه هدرها مجاز هستن
)
# این رو برای دیپلوی حتما پاک کن !!!!!!!!!!!
