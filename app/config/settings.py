from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict

class Settings(BaseSettings):
    ENV: str = Field("dev", pattern="^(dev|prod)$")
    APP_NAME: str = "WEQ API"
    ALLOWED_ORIGINS: list[str] = ["http://localhost"]

    model_config = ConfigDict(env_file=".env")


settings = Settings()
print(f"Settings loaded: ENV={settings.ENV}, APP_NAME={settings.APP_NAME}")