# app/routers/onboarding/OnboardingDashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.session import get_db
from app.models.onboarding import OnboardingEmployee as Employees, OnboardingCandidate, OnboardingForm, OfferLetter
from datetime import datetime

router = APIRouter(
    prefix="/onboarding/dashboard",
    tags=["Onboarding Dashboard"]
)

@router.get("/")
def get_onboarding_dashboard(db: Session = Depends(get_db)):
    # Total employees
    total_employees = db.query(Employees).count()

    # Pending approvals for onboarding candidates
    pending_approvals = db.query(OnboardingCandidate).filter(
        OnboardingCandidate.form_status == "Pending"
    ).count()

    # Total onboarding forms
    total_forms = db.query(OnboardingForm).count()

    # Offer letters generated
    offer_letters = db.query(OfferLetter).count()

    # Start date = 12 months ago
    today = datetime.today()
    start_date = datetime(today.year - 1, today.month, 1)

    # Monthly joinings for last 12 months (PostgreSQL uses to_char)
    joinings = db.query(
        func.to_char(Employees.joining_date, 'Mon YYYY').label("month"),
        func.count(Employees.id).label("count")
    ).filter(
        Employees.joining_date >= start_date
    ).group_by("month").order_by("month").all()

    # Format chart data
    chart_data = [{"month": month, "value": count} for month, count in joinings]

    return {
        "total_employees": total_employees,
        "pending_approvals": pending_approvals,
        "total_forms": total_forms,
        "offer_letters": offer_letters,
        "monthly_joinings": chart_data
    }
