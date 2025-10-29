from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from app.config import settings

# ==========================
# DATABASE ENGINE
# ==========================
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # checks connection before using it
    pool_size=10,
    max_overflow=20,
)

# ==========================
# SESSION LOCAL
# ==========================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ==========================
# DATABASE DEPENDENCY
# ==========================
def get_db() -> Generator:
    """Yields a SQLAlchemy session for dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
