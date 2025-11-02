from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "HRMS Onboarding"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    CORS_ORIGINS: List[str] = ["*"]

    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    EMAIL_USER: Optional[str] = None
    EMAIL_PASS: Optional[str] = None

    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None

    # pydantic-settings configuration
    # Allow or ignore extra env vars so unrelated environment variables
    # (for example FRONTEND_URL in local dev) don't raise validation errors.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
