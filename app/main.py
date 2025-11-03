# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
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

# =========================================================
# Import Routers — Onboarding
# =========================================================
from app.api.v1.routers.onboarding import (
    Addemployee, ApproveAdditions, OfferLetter, offerLetterform,
    BulkOnboarding, FinalizeAndSendForm, Forms, Newform, OnboardingDashboard,
    OnboardingFormPartB, OnboardingFormSingle, OnboardingFormTable,
    OnboardingSettings, Reviewform, dropdowns, AttachOfferLetterform
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
# Import Routers — Data Capture & Requests
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
    router as requests_router
)

# =========================================================
# Import Routers — Attendance (from your project)
# =========================================================
from app.api.v1.routers.attendance import (
    attendanceemployee,
    attendancemodal,
    calendartable,
    dailyattendance,
    dailypunch,
    leavecorrection,
    manualattendance,
    monthlyattendance,
)

# =========================================================
# Directory Setup
# =========================================================
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# =========================================================
# Application Lifecycle
# =========================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup/shutdown lifecycle"""
    Base.metadata.create_all(bind=engine)
    yield
    pass

# =========================================================
# FastAPI Initialization
# =========================================================
app = FastAPI(
    title="HRMS Unified API",
    description=(
        "Unified backend API for HRMS modules including Super Admin, "
        "Payroll, Data Capture, Requests, and Attendance Management."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
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

# =========================================================
# Include Routers — Onboarding
# =========================================================
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
app.include_router(AttachOfferLetterform.router)

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

# =========================================================
# Include Routers — Requests
# =========================================================
app.include_router(requests_router, prefix=settings.API_V1_STR)
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
# Include Routers — Attendance (your project)
# =========================================================
app.include_router(attendanceemployee.router, prefix="/api/v1/attendance")
app.include_router(attendancemodal.router, prefix="/api/v1/attendance")
app.include_router(calendartable.router, prefix="/api/v1/attendance")
app.include_router(dailyattendance.router, prefix="/api/v1/attendance")
app.include_router(dailypunch.router, prefix="/api/v1/attendance")
app.include_router(leavecorrection.router, prefix="/api/v1/attendance")
app.include_router(manualattendance.router, prefix="/api/v1/attendance")
app.include_router(monthlyattendance.router, prefix="/api/v1/attendance")

# =========================================================
# Custom OpenAPI (from your main.py)
# =========================================================
custom_tags_metadata = [
    {"name": "attendanceemployee", "description": "Manage Employee Records"},
    {"name": "attendancemodal", "description": "Handle daily attendance modals"},
    {"name": "calendartable", "description": "Manage holidays and calendar dates"},
    {"name": "dailyattendance", "description": "Manage employee daily attendance"},
    {"name": "dailypunch", "description": "Record and view daily punches"},
    {"name": "leavecorrection", "description": "Manage employee leave corrections"},
    {"name": "manualattendance", "description": "Add or review manual attendance"},
    {"name": "monthlyattendance", "description": "Monthly summary of employee attendance"},
]

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["tags"] = custom_tags_metadata
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# =========================================================
# Root Endpoint
# =========================================================
@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "✅ HRMS Unified API is running!",
        "version": "1.0.0",
        "modules": ["superadmin", "payroll", "datacapture", "attendance"],
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
