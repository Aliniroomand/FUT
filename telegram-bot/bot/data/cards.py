# شبیه‌سازی دیتابیس کارت‌ها

def get_player_card_meta(amount: int):
    """فیک برمی‌گردونه کارت اصلی و فرعی"""
    return {
        "primary": f"کارت اصلی برای {amount}",
        "secondary": f"کارت فرعی برای {amount}"
    }

def list_card_ranges():
    """فیک رنج کارت‌ها"""
    return {
        "primary": 1000,
        "secondary": 5000
    }
