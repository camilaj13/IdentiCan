from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    APP_NAME: str = "IdentiCan"
    DEBUG: bool = False
    SECRET_KEY: str = "CHANGE_THIS_SECRET_KEY"

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/identican"

    # JWT
    JWT_SECRET: str = "CHANGE_THIS_JWT_SECRET"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_DAYS: int = 7

    # Storage (Cloudflare R2)
    R2_ENDPOINT: str = ""
    R2_ACCESS_KEY: str = ""
    R2_SECRET_KEY: str = ""
    R2_BUCKET_NAME: str = "identican-images"

    # Features
    PREMIUM_ENABLED: bool = False
    VERIFICATION_LIMIT_FREE: int = 3

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:19006"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
