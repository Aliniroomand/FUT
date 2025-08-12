from app.routes import admin_choosen_price
from fastapi import FastAPI  
from app.routes import player_card, transfer_method, transaction,card_range , admin_choosen_price,auth,profile,admin
from app.database import engine, Base
import app.models
from app.routes import alert, ea_account, transactionsControl

Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}



app.include_router(admin_choosen_price.router)
app.include_router(card_range.router)
app.include_router(player_card.router)
app.include_router(transaction.router)
app.include_router(transfer_method.router)
app.include_router(transactionsControl.router)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(admin.router)
app.include_router(alert.router)
app.include_router(ea_account.router)









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
