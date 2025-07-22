# app/routes/transfer_settings.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.card_range_assignment import CardRangeAssignment
from app.services.transfer_card_range_logic import create_auto_ranges_and_rules
from app.schemas.transfer_range_setting import TransferSettingCreate, TransferSettingOut

router = APIRouter(prefix="/transfer-settings", tags=["Transfer Settings"])

@router.post("/", response_model=TransferSettingOut)
def set_threshold_and_generate_ranges(
    payload: TransferSettingCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(CardRangeAssignment).first()
    if existing:
        existing.threshold_amount = payload.threshold_amount
        db.commit()
    else:
        setting = CardRangeAssignment(threshold_amount=payload.threshold_amount)
        db.add(setting)
        db.commit()
        db.refresh(setting)

    # ساخت بازه‌ها و قوانین خودکار
    if len(payload.primary_card_ids) != 3:
        raise HTTPException(status_code=400, detail="Exactly 3 card IDs required.")

    create_auto_ranges_and_rules(
        db=db,
        n=payload.threshold_amount,
        cards=payload.primary_card_ids,
        platform=payload.platform
    )

    return {"threshold_amount": payload.threshold_amount}
