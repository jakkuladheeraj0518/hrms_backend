from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.database.base import Base
from app.database.session import engine
from app.config import settings
from app.api.v1.routers.superadmin import (
    dashboard,
    companies,
    packages,
    subscriptions,
    transactions,
    domains
)

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup if needed
    pass

app = FastAPI(
    title="Super Admin Dashboard API",
    description="Complete Backend API for Super Admin Dashboard Management System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include all routers
app.include_router(dashboard.router)
app.include_router(companies.router)
app.include_router(packages.router)
app.include_router(subscriptions.router)
app.include_router(transactions.router)
app.include_router(domains.router)

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Super Admin Dashboard API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected"
    }
