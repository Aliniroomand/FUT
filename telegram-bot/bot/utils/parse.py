# bot/utils/parse.py
import re

_persian_digits = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
    "01234567890123456789"
)

def parse_amount_from_text(text: str) -> int | None:
    if not isinstance(text, str):
        return None
    t = text.strip().translate(_persian_digits)
    digits = re.findall(r"\d+", t)
    if not digits:
        return None
    try:
        return int("".join(digits))
    except Exception:
        return None
