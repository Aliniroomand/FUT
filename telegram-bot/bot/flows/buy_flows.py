from enum import Enum, auto
from dataclasses import dataclass

class BuyState(Enum):
    START = auto()
    ASK_METHOD = auto()
    AWAIT_METHOD_SELECTION = auto()
    ASK_AMOUNT = auto()
    AWAIT_CONFIRM = auto()
    PENDING = auto()
    SUCCESS = auto()
    CANCELED = auto()

@dataclass
class BuyFlow:
    state: BuyState = BuyState.START
