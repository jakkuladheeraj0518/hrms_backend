from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:dheeraj123@localhost:5432/superadmin_db"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 4 * 1024 * 1024  # 4MB
    
    class Config:
        env_file = ".env"

settings = Settings()
