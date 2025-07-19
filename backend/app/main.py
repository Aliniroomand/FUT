from fastapi import FastAPI
from app.routes import player  # 👈 ایمپورت کردن روت مربوط به بازیکن
from app.database import engine, Base

# ایجاد جداول دیتابیس
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API is running"}

# اضافه کردن مسیرهای API
app.include_router(player.router, prefix="/players", tags=["Players"])
