from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ==========================
    # DATABASE SETTINGS
    # ==========================
    DATABASE_URL: str = "postgresql://postgres:dheeraj123@localhost:5432/superadmin_db"

    # ==========================
    # APP / PROJECT
    # ==========================
    PROJECT_NAME: str = "HRMS Onboarding"

    # ==========================
    # SECURITY SETTINGS
    # ==========================
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_V1_STR: str = "/api/v1"

    # ==========================
    # CORS SETTINGS
    # ==========================
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # ==========================
    # FILE UPLOAD SETTINGS
    # ==========================
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 4 * 1024 * 1024  # 4 MB

    # Optional / external integrations
    FRONTEND_URL: Optional[str] = None

    # Optional email config
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    EMAIL_USER: Optional[str] = None
    EMAIL_PASS: Optional[str] = None

    # Optional Twilio config
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None

    # pydantic-settings / pydantic v2 config
    # Allow ignoring extra env variables so local/dev-only keys don't break startup
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


# Instantiate settings globally
settings = Settings()
