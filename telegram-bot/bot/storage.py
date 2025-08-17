# Simple in-memory token storage for demo purposes
user_tokens: dict[int, str] = {}


def is_logged_in(user_id: int) -> bool:
    return user_id in user_tokens


def save_token(user_id: int, token: str) -> None:
    user_tokens[user_id] = token


def get_token(user_id: int) -> str | None:
    return user_tokens.get(user_id)
