from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str
    http_proxy: str | None = None
    https_proxy: str | None = None
    backend_url: str
    admin_chat_id: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
