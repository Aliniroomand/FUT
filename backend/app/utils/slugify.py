import re
import unicodedata


def slugify(name: str) -> str:
# basic ASCII slug for Futbin slug param
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9\s-]", "", s).strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return s