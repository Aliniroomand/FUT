from dataclasses import dataclass, asdict
from datetime import datetime
from decimal import Decimal
from typing import Optional
from enum import Enum, auto

class BuyState(Enum):
    START = auto()
    ASK_METHOD = auto()
    AWAIT_METHOD_SELECTION = auto()
    ASK_AMOUNT = auto()
    AWAIT_CONFIRM = auto()
    PENDING = auto()
    SUCCESS = auto()
    CANCELED = auto()
    AWAIT_PROFILE_INPUT = auto()
    AWAIT_PROFILE_CONFIRM = auto()

@dataclass
class BuyFlow:
    state: BuyState = BuyState.START
    amount: Optional[Decimal] = None
    method_id: Optional[int] = None
    method_name: Optional[str] = None
    transfer_multiplier: float = 1.0
    matched_ranges: Optional[list] = None
    choice_map: Optional[dict] = None
    tx_id: Optional[int] = None
    created_at: Optional[str] = None

    # تبدیل dataclass به دیکشنری برای ذخیره
    def to_dict(self):
        d = asdict(self)
        if self.created_at is None:
            d["created_at"] = datetime.utcnow().isoformat()
        # enum را به نام رشته‌ای تبدیل می‌کنیم تا راحت ذخیره شود
        d["state"] = self.state.name
        return d

    # ساخت از دیکشنری
    @classmethod
    def from_dict(cls, raw: dict):
        # enum را از رشته برگردانیم
        if "state" in raw and isinstance(raw["state"], str):
            raw["state"] = BuyState[raw["state"]]
        return cls(**raw)
