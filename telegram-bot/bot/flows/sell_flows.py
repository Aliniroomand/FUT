# bot/flows/sell_flow.py
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Optional

class SellState(Enum):
    START = auto()
    CHECK_STATUS = auto()
    CHOOSE_METHOD = auto()
    ASK_AMOUNT = auto()
    AWAIT_CONFIRM = auto()
    SHOW_OPTIONS = auto()
    AWAIT_LIST_DECISION = auto()
    AWAIT_PURCHASE_CONFIRM = auto()
    DONE = auto()
    CANCELED = auto()
    TIMEOUT = auto()

@dataclass
class SellFlow:
    state: SellState = SellState.START
    method_id: Optional[int] = None
    methods: list[dict] = field(default_factory=list)
    amount: Optional[int] = None

    matched_range: dict = field(default_factory=dict)
    primary: dict = field(default_factory=dict)
    secondary: dict = field(default_factory=dict)
    buy1: Optional[int] = None
    buy2: Optional[int] = None
    img1: Optional[str] = None
    img2: Optional[str] = None
    transfer_multiplier: float = 1.0
    transferable1: Optional[float] = None
    transferable2: Optional[float] = None

    # کارهای زمان‌بندی‌شده (برای تایم‌اوت ۱ دقیقه‌ای)
    jobs: dict[str, Any] = field(default_factory=dict)

    extra: dict = field(default_factory=dict)

    def reset(self):
        self.__dict__.update(SellFlow().__dict__)
