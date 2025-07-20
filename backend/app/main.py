from fastapi import FastAPI
from app.routes import player, price, transfer_method
from app.database import engine, Base

# ایجاد جداول دیتابیس
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API is running"}

# اضافه کردن مسیرهای API
app.include_router(player.router)
app.include_router(price.router)
app.include_router(transfer_method.router)

