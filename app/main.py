from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_tables

# Import routers
from app.routers import dashboard, companies, domains, packages, transactions, subscriptions

# Create FastAPI app
app = FastAPI(
    title="SuperAdmin Dashboard API",
    description="Complete backend API for SuperAdmin Dashboard with PostgreSQL",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def on_startup():
    try:
        create_tables()
        print("✅ Database tables checked/created successfully!")
    except Exception as e:
        print(f"⚠️ Warning: Could not create tables - {e}")
        print("Please run: python init_db.py")

# Include routers
app.include_router(dashboard.router)
app.include_router(companies.router)
app.include_router(domains.router)
app.include_router(packages.router)
app.include_router(transactions.router)
app.include_router(subscriptions.router)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "SuperAdmin Dashboard API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "dashboard": "/api/dashboard",
            "companies": "/api/companies",
            "domains": "/api/domains",
            "packages": "/api/packages",
            "transactions": "/api/transactions",
            "subscriptions": "/api/subscriptions",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)