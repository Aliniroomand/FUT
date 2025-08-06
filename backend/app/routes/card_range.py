from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import CardRange,PlayerCard,TransferMethod
from app.schemas.card_range import (
    CardRange as CardRangeSchema,
    CardRangeCreate,
    CardRangeUpdate
)
from app.crud import card_range as crud

router = APIRouter(prefix="/card-ranges", tags=["Card Ranges"])

@router.post("/", response_model=CardRangeSchema)
def create_card_range(range_data: CardRangeCreate, db: Session = Depends(get_db)):
    """
    ایجاد یک بازه قیمتی جدید
    """
    # بررسی اینکه کارت اصلی وجود دارد
    primary_card = db.query(PlayerCard).filter(PlayerCard.id == range_data.primary_card_id).first()
    if not primary_card:
        raise HTTPException(status_code=400, detail="کارت اصلی یافت نشد")
    
    # بررسی کارت جایگزین اگر وجود دارد
    if range_data.fallback_card_id:
        fallback_card = db.query(PlayerCard).filter(PlayerCard.id == range_data.fallback_card_id).first()
        if not fallback_card:
            raise HTTPException(status_code=400, detail="کارت جایگزین یافت نشد")
    # بررسی اینکه شیوه انتقال وجود دارد
    transfer_method = db.query(TransferMethod).filter(TransferMethod.id == range_data.transfer_method_id).first()
    if not transfer_method:
        raise HTTPException(status_code=400, detail="شیوه انتقال یافت نشد")
    # بررسی صحت بازه قیمتی
    if range_data.min_value >= range_data.max_value:
        raise HTTPException(status_code=400, detail="حداقل مقدار باید کمتر از حداکثر مقدار باشد")
    
    return crud.create_card_range(db, range_data)

@router.get("/", response_model=list[CardRangeSchema])
def get_all_ranges(db: Session = Depends(get_db)):
    """
    دریافت لیست تمام بازه‌های قیمتی
    """
    return db.query(CardRange).options(
        joinedload(CardRange.primary_card),
        joinedload(CardRange.fallback_card)
    ).order_by(CardRange.min_value).all()

@router.get("/{range_id}", response_model=CardRangeSchema)
def get_range_by_id(range_id: int, db: Session = Depends(get_db)):
    """
    دریافت یک بازه قیمتی بر اساس ID
    """
    db_range = db.query(CardRange).options(
        joinedload(CardRange.primary_card),
        joinedload(CardRange.fallback_card)
    ).filter(CardRange.id == range_id).first()
    
    if not db_range:
        raise HTTPException(status_code=404, detail="بازه قیمتی یافت نشد")
    return db_range

@router.put("/{range_id}", response_model=CardRangeSchema)
def update_card_range(range_id: int, range_data: CardRangeUpdate, db: Session = Depends(get_db)):
    """
    به‌روزرسانی یک بازه قیمتی
    """
    db_range = db.query(CardRange).filter(CardRange.id == range_id).first()
    if not db_range:
        raise HTTPException(status_code=404, detail="بازه قیمتی یافت نشد")
    
    # بررسی کارت‌ها اگر در داده‌های به‌روزرسانی وجود دارند
    if range_data.primary_card_id is not None:
        primary_card = db.query(PlayerCard).filter(PlayerCard.id == range_data.primary_card_id).first()
        if not primary_card:
            raise HTTPException(status_code=400, detail="کارت اصلی یافت نشد")
    
    if range_data.fallback_card_id is not None:
        fallback_card = db.query(PlayerCard).filter(PlayerCard.id == range_data.fallback_card_id).first()
        if not fallback_card:
            raise HTTPException(status_code=400, detail="کارت جایگزین یافت نشد")
    
    # اعمال تغییرات
    update_data = range_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_range, key, value)
    
    db.commit()
    db.refresh(db_range)
    return db_range

@router.delete("/{range_id}")
def delete_card_range(range_id: int, db: Session = Depends(get_db)):
    """
    حذف یک بازه قیمتی
    """
    db_range = db.query(CardRange).filter(CardRange.id == range_id).first()
    if not db_range:
        raise HTTPException(status_code=404, detail="بازه قیمتی یافت نشد")
    
    db.delete(db_range)
    db.commit()
    return {"message": "بازه قیمتی با موفقیت حذف شد"}

    
@router.get("/{method_id}/ranges")
def get_ranges(method_id: int, db: Session = Depends(get_db)):
    return crud.get_ranges_for_method(db, method_id)


@router.get("/for-amount/{amount}", response_model=list[CardRangeSchema])
def get_ranges_for_amount(amount: float, db: Session = Depends(get_db)):
    """
    دریافت بازه‌های قیمتی مناسب برای مبلغ مشخص شده
    """
    if amount <= 0:
        raise HTTPException(status_code=400, detail="مبلغ باید بزرگتر از صفر باشد")
    
    ranges = db.query(CardRange).options(
        joinedload(CardRange.primary_card),
        joinedload(CardRange.fallback_card)
    ).filter(
        CardRange.min_value <= amount,
        CardRange.max_value >= amount
    ).order_by(CardRange.min_value).all()
    
    if not ranges:
        raise HTTPException(
            status_code=404,
            detail="هیچ بازه‌ای برای این مبلغ تعریف نشده است. لطفاً با ادمین تماس بگیرید"
        )
    
    return ranges