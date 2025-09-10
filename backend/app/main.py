from app.routes import admin_choosen_price
from fastapi import FastAPI  
from app.routes import player_card, transfer_method, transaction,card_range , admin_choosen_price,auth,profile,admin,alert, ea_account, transactionsControl ,futbin, market_actions, admin_alerts
from app.database import engine, Base
import app.models
from app.cache import get_redis, close_redis
from app.services.transfer_worker import start_worker, stop_worker
from app.config import settings


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

# include routers
app.include_router(futbin.router)
app.include_router(market_actions.router)
app.include_router(admin_alerts.router)








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

@app.on_event("startup")
async def startup_event():
    # init redis (connect)
    await get_redis()
    # start worker only when enabled in settings (useful to disable during tests)
    if getattr(settings, "START_WORKER", False):
        await start_worker(app)

@app.on_event("shutdown")
async def shutdown_event():
    # stop worker only if it was started
    if getattr(settings, "START_WORKER", False):
        await stop_worker(app)
    await close_redis()
    
    
