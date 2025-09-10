from pydantic_settings import BaseSettings
import warnings

class Settings(BaseSettings):
    bot_token: str
    http_proxy: str | None = None
    https_proxy: str | None = None
    backend_url: str
    frontend_url: str
    admin_chat_link: str
    admin_username: str
    admin_chat_id: str
    redis_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# ----------------------
# بارگذاری settings
# ----------------------
settings = Settings()

# ----------------------
# بررسی HTTPS
# ----------------------
if not settings.backend_url.startswith("https://"):
    warnings.warn(
        f"Backend URL is not HTTPS ({settings.backend_url})! "
        "Use HTTPS in production."
    )
