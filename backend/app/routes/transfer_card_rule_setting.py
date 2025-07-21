from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.TransferCard_range_setting import TransferSettings
from app.schemas.transfer_card_rule_setting import TransferSettingCreate, TransferSettingOut
from app.services.transfer_card_range_logic import create_auto_ranges_and_rules

router = APIRouter(prefix="/transfer-settings", tags=["Transfer Settings"])

@router.post("/", response_model=TransferSettingOut)
def set_threshold(setting: TransferSettingCreate, db: Session = Depends(get_db)):
    existing = db.query(TransferSettings).first()
    if existing:
        existing.threshold_amount = setting.threshold_amount
        db.commit()
        db.refresh(existing)
        return existing
    new_setting = TransferSettings(threshold_amount=setting.threshold_amount)
    db.add(new_setting)
    db.commit()
    db.refresh(new_setting)
    return new_setting

@router.get("/", response_model=TransferSettingOut)
def get_threshold(db: Session = Depends(get_db)):
    setting = db.query(TransferSettings).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Threshold not set")
    return setting

@router.post("/apply-ranges/")
def apply_ranges(
    threshold: int,
    card_ids: list[int],  # باید دقیقا ۳ تا باشه
    platform: str,
    db: Session = Depends(get_db),
):
    if len(card_ids) != 3:
        raise HTTPException(status_code=400, detail="Exactly 3 cards required")
    
    # 1. ذخیره مقدار threshold
    existing = db.query(TransferSettings).first()
    if existing:
        existing.threshold_amount = threshold
    else:
        setting = TransferSettings(threshold_amount=threshold)
        db.add(setting)
    db.commit()

    # 2. ایجاد بازه‌ها و قوانین
    return create_auto_ranges_and_rules(db, threshold, card_ids, platform)
