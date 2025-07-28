from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./fut.db"  # یا مسیر دلخواه

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ تابع get_db برای Dependency Injection در FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
