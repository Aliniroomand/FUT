user_tokens = {}

def save_token(user_id: int, token: str):
    user_tokens[user_id] = token

def delete_token(user_id: int):
    user_tokens.pop(user_id, None)

def token_exists(user_id: int) -> bool:
    return user_id in user_tokens
