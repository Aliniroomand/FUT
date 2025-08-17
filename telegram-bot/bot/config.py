from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    bot_token: str
    backend_url: str
    admin_chat_id: int
    http_proxy: str | None = None
    https_proxy: str | None = None

    @classmethod
    def from_env(cls) -> 'Settings':
        bot_token = os.getenv('BOT_TOKEN')
        backend_url = os.getenv('BACKEND_URL', '').rstrip('/')
        admin_chat_id = os.getenv('ADMIN_CHAT_ID')

        if not bot_token or not admin_chat_id:
            raise RuntimeError("BOT_TOKEN and ADMIN_CHAT_ID must be set in the environment variables.")

        return cls(
            bot_token=bot_token,
            backend_url=backend_url,
            admin_chat_id=int(admin_chat_id),
            http_proxy=os.getenv('HTTP_PROXY'),
            https_proxy=os.getenv('HTTPS_PROXY')
        )

settings = Settings.from_env()