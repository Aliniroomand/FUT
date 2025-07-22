from sqlalchemy.orm import Session

def create_auto_ranges_and_rules(db: Session, n: int, cards: list[int], platform: str):
    from app.models.card_range import CardRange
    from app.models.transfer_card_rule import TransferCardRule

    steps = [(0, n//3), (n//3 + 1, 2 * n // 3), (2 * n // 3 + 1, n)]
    descriptions = ["Low", "Medium", "High"]

    created_ranges = []

    for i, (min_val, max_val) in enumerate(steps):
        card_range = CardRange(
            min_value=min_val,
            max_value=max_val,
            description=descriptions[i]
        )
        db.add(card_range)
        db.commit()
        db.refresh(card_range)

        rule = TransferCardRule(
            card_range_id=card_range.id,
            primary_card_id=cards[i],
            platform=platform
        )
        db.add(rule)
        db.commit()

        created_ranges.append((card_range, rule))

    return created_ranges


def select_transfer_card_by_amount(db: Session, amount: int, platform: str):
    from backend.app.models.card_range_assignment import TransferSettings
    from app.models.card_range import CardRange
    from app.models.transfer_card_rule import TransferCardRule

    setting = db.query(TransferSettings).first()
    if not setting or amount > setting.threshold_amount:
        return {"contact_admin": True}

    # پیدا کردن بازه مناسب
    card_range = (
        db.query(CardRange)
        .filter(CardRange.min_value <= amount, CardRange.max_value >= amount)
        .first()
    )
    if not card_range:
        return {"contact_admin": True}

    # پیدا کردن کارت مناسب
    rule = (
        db.query(TransferCardRule)
        .filter_by(card_range_id=card_range.id, platform=platform)
        .first()
    )
    if not rule:
        return {"contact_admin": True}

    return {
        "contact_admin": False,
        "card_id": rule.primary_card_id or rule.fallback_card_id
    }
