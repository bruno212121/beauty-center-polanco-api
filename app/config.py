from pydantic_settings import BaseSettings, SettingsConfigDict
from decimal import Decimal

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "postgresql://user:password@localhost:5432/beauty_center"
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 horas

    COMMISSION_SERVICE_PERCENT: Decimal = Decimal("30.00")
    COMMISSION_PRODUCT_PERCENT: Decimal = Decimal("10.00")


settings = Settings()
