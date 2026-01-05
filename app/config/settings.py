from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict

class Settings(BaseSettings):
    ENV: str = Field("dev", pattern="^(dev|prod)$")
    APP_NAME: str = "WEQ API"
    ALLOWED_ORIGINS: list[str] = ["http://localhost"]

    # JWT settings for authentication
    # Support key rotation via JWT_KEYS and an ACTIVE_KEY_ID.
    JWT_KEYS: dict = {"key-1": "change-me"}
    ACTIVE_KEY_ID: str = "key-1"
    JWT_ALGORITHM: str = "HS256"
    JWT_AUDIENCE: str = "weq-api"
    JWT_ISSUER: str = "weq-auth-service"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # default to 30 minutes for access tokens

    model_config = ConfigDict(env_file=".env")


settings = Settings()
print(f"Settings loaded: ENV={settings.ENV}, APP_NAME={settings.APP_NAME}")