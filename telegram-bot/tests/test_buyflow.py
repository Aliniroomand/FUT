import pytest
from bot.flows.buy_flows import BuyFlow, BuyState
from decimal import Decimal

def test_serialization():
    flow = BuyFlow(state=BuyState.ASK_AMOUNT, amount=Decimal('150000'), method_id=1)
    
    data = flow.to_dict()
    # باید state به string تبدیل شده باشه
    assert data["state"] == "ASK_AMOUNT"
    # amount درست ذخیره شده
    assert str(data["amount"]) == "150000"

    # دوباره از dict بسازیم
    flow2 = BuyFlow.from_dict(data)
    assert flow2.state == BuyState.ASK_AMOUNT
    assert flow2.amount == Decimal('150000')
    assert flow2.method_id == 1
