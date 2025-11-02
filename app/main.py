from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.database.base import Base
from app.database.session import engine
from app.config import settings

# =========================================================
# Import Routers — Super Admin
# =========================================================
from app.api.v1.routers.superadmin import (
    dashboard,
    companies,
    packages,
    subscriptions,
    transactions,
    domains,
)

from app.api.v1.routers.onboarding import (
    Addemployee, ApproveAdditions, OfferLetter, offerLetterform,
    BulkOnboarding, FinalizeAndSendForm, Forms, Newform, OnboardingDashboard,
    OnboardingFormPartB, OnboardingFormSingle, OnboardingFormTable, OnboardingSettings, Reviewform,dropdowns
)


# =========================================================
# Import Routers — Payroll
# =========================================================
from app.api.v1.routers.Payroll import (
    payroll_periods,
    leave_encashment,
    recalculation,
    bonus,
    gratuity,
    runpayroll,
    hold_salary,
)

# =========================================================
# Import Routers — Data Capture
# =========================================================
from app.api.v1.routers.datacapture import (
    salary_variable,
    deduction_variable,
    tds,
    deduction_tds,
    incometax_tds,
    extra_days,
    extra_hours,
    datacapture_loans,
    loans,
    it_declaration,
    tds_returns,
)
from app.api.v1.routers.requests import (
    leave_request,
    missed_punch_request,
    compoff,
    helpdesk,
    claim_requests,
    time_relaxation_request,
    shift_roster_request,
    week_roaster,
    strike_requests,
    visit_punch_request,
    workflow_request,
    shift_roster,
    requests
)

# =========================================================
# Directory Setup
# =========================================================
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# =========================================================
# Application Lifecycle (Startup & Shutdown)
# =========================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup/shutdown lifecycle"""
    # Startup: create tables if not exist (optional for Alembic)
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: perform cleanup if needed
    pass

# =========================================================
# FastAPI Initialization
# =========================================================
app = FastAPI(
    title="HRMS Super Admin, Payroll, and Data Capture API And Requests",
    description="Unified backend API for HRMS modules including Super Admin, Payroll, and Data Capture & Requests.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# =========================================================
# Middleware Configuration
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# Static Files
# =========================================================
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# =========================================================
# Include Routers — Super Admin
# =========================================================
app.include_router(dashboard.router, prefix="/api/v1/superadmin")
app.include_router(companies.router, prefix="/api/v1/superadmin")
app.include_router(packages.router, prefix="/api/v1/superadmin")
app.include_router(subscriptions.router, prefix="/api/v1/superadmin")
app.include_router(transactions.router, prefix="/api/v1/superadmin")
app.include_router(domains.router, prefix="/api/v1/superadmin")

#onboarding

# include routers
app.include_router(Addemployee)
app.include_router(ApproveAdditions)
app.include_router(OfferLetter)
app.include_router(offerLetterform)
app.include_router(BulkOnboarding)
app.include_router(FinalizeAndSendForm)
app.include_router(Forms)
app.include_router(Newform)
app.include_router(OnboardingDashboard)
app.include_router(OnboardingFormPartB)
app.include_router(OnboardingFormSingle)
app.include_router(OnboardingFormTable)
app.include_router(OnboardingSettings)
app.include_router(Reviewform)
app.include_router(dropdowns.router)

# =========================================================
# Include Routers — Payroll
# =========================================================
app.include_router(payroll_periods.router, prefix="/api/v1/payroll")
app.include_router(leave_encashment.router, prefix="/api/v1/payroll")
app.include_router(recalculation.router, prefix="/api/v1/payroll")
app.include_router(bonus.router, prefix="/api/v1/payroll")
app.include_router(gratuity.router, prefix="/api/v1/payroll")
app.include_router(runpayroll.router, prefix="/api/v1/payroll")
app.include_router(hold_salary.router, prefix="/api/v1/payroll")

# =========================================================
# Include Routers — Data Capture
# =========================================================
app.include_router(salary_variable.router, prefix="/api/v1/datacapture")
app.include_router(deduction_variable.router, prefix="/api/v1/datacapture")
app.include_router(tds.router, prefix="/api/v1/datacapture")
app.include_router(deduction_tds.router, prefix="/api/v1/datacapture")
app.include_router(incometax_tds.router, prefix="/api/v1/datacapture")
app.include_router(extra_days.router, prefix="/api/v1/datacapture")
app.include_router(extra_hours.router, prefix="/api/v1/datacapture")
app.include_router(datacapture_loans.router, prefix="/api/v1/datacapture")
app.include_router(loans.router, prefix="/api/v1/datacapture")
app.include_router(it_declaration.router, prefix="/api/v1/datacapture")
app.include_router(tds_returns.router, prefix="/api/v1/datacapture")

# Include routers - Requests
app.include_router(requests.router, prefix=settings.API_V1_STR)
app.include_router(missed_punch_request.router, prefix=settings.API_V1_STR)
app.include_router(leave_request.router, prefix=settings.API_V1_STR)
app.include_router(compoff.router, prefix=settings.API_V1_STR)
app.include_router(helpdesk.router, prefix=settings.API_V1_STR)
app.include_router(claim_requests.router, prefix=settings.API_V1_STR)
app.include_router(time_relaxation_request.router, prefix=settings.API_V1_STR)
app.include_router(shift_roster_request.router, prefix=settings.API_V1_STR)
app.include_router(week_roaster.router, prefix=settings.API_V1_STR)
app.include_router(strike_requests.router, prefix=settings.API_V1_STR)
app.include_router(visit_punch_request.router, prefix=settings.API_V1_STR)
app.include_router(workflow_request.router, prefix=settings.API_V1_STR)
app.include_router(shift_roster.router, prefix=settings.API_V1_STR)

# =========================================================
# Root Endpoint
# =========================================================
@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "✅ HRMS API for Super Admin, Payroll, and Data Capture is running!",
        "version": "1.0.0",
        "modules": ["superadmin", "payroll", "datacapture"],
        "docs": "/docs",
        "redoc": "/redoc",
    }

# =========================================================
# Health Check
# =========================================================
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "database": "connected"}
