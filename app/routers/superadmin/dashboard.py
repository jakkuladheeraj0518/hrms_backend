from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
import calendar

from app.database import get_db
from app.models.superadmin import Company, Transaction, Subscription, Package
from app.schemas.superadmin import (
    DashboardResponse,
    DashboardStatsResponse,
    RevenueDataPoint,
    PlanDistribution,
    RecentTransaction,
    RecentCompany,
    ExpiredPlan
)

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
def get_dashboard_data(db: Session = Depends(get_db)):
    """Get all dashboard data including stats, charts, and recent activities"""

    # === Date Ranges ===
    today = datetime.now()
    first_day_current_month = today.replace(day=1)
    first_day_last_month = (first_day_current_month - timedelta(days=1)).replace(day=1)
    last_day_last_month = first_day_current_month - timedelta(days=1)

    # === Totals ===
    total_companies = db.query(Company).count()
    active_companies = db.query(Company).filter(Company.status == "Active").count()
    total_subscribers = db.query(Subscription).filter(Subscription.status == "Paid").count()
    total_earnings = db.query(func.sum(Transaction.amount)).filter(Transaction.status == "Paid").scalar() or 0.0

    # === Current & Previous Month Data ===
    # Companies
    current_month_companies = db.query(Company).filter(
        Company.created_date >= first_day_current_month
    ).count()
    previous_month_companies = db.query(Company).filter(
        Company.created_date >= first_day_last_month,
        Company.created_date <= last_day_last_month
    ).count()

    # Active Companies
    current_month_active = db.query(Company).filter(
        Company.status == "Active",
        Company.created_date >= first_day_current_month
    ).count()
    previous_month_active = db.query(Company).filter(
        Company.status == "Active",
        Company.created_date >= first_day_last_month,
        Company.created_date <= last_day_last_month
    ).count()

    # Subscribers (FIXED: using created_date)
    current_month_subscribers = db.query(Subscription).filter(
        Subscription.status == "Paid",
        Subscription.created_date >= first_day_current_month
    ).count()
    previous_month_subscribers = db.query(Subscription).filter(
        Subscription.status == "Paid",
        Subscription.created_date >= first_day_last_month,
        Subscription.created_date <= last_day_last_month
    ).count()

    # Earnings
    current_month_earnings = db.query(func.sum(Transaction.amount)).filter(
        Transaction.status == "Paid",
        Transaction.date >= first_day_current_month
    ).scalar() or 0.0
    previous_month_earnings = db.query(func.sum(Transaction.amount)).filter(
        Transaction.status == "Paid",
        Transaction.date >= first_day_last_month,
        Transaction.date <= last_day_last_month
    ).scalar() or 0.0

    # === Growth Calculation ===
    def calc_growth(current, previous):
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return round(((current - previous) / previous) * 100, 2)

    company_growth = calc_growth(current_month_companies, previous_month_companies)
    active_growth = calc_growth(current_month_active, previous_month_active)
    subscriber_growth = calc_growth(current_month_subscribers, previous_month_subscribers)
    earnings_growth = calc_growth(current_month_earnings, previous_month_earnings)

    # === Dashboard Stats ===
    stats = DashboardStatsResponse(
        total_companies=total_companies,
        active_companies=active_companies,
        total_subscribers=total_subscribers,
        total_earnings=round(total_earnings, 2),
        company_growth=company_growth,
        active_growth=active_growth,
        subscriber_growth=subscriber_growth,
        earnings_growth=earnings_growth
    )

    # === Revenue Data (Month by Month) ===
    revenue_data = []
    current_year = datetime.now().year
    for month_num in range(1, 13):
        month_name = calendar.month_abbr[month_num]
        income = db.query(func.sum(Transaction.amount)) \
            .filter(
                extract('year', Transaction.date) == current_year,
                extract('month', Transaction.date) == month_num,
                Transaction.status == "Paid"
            ).scalar() or 0.0

        expenses = income * 0.3 if income > 0 else 0.0

        revenue_data.append(RevenueDataPoint(
            month=month_name,
            income=round(income, 2),
            expenses=round(expenses, 2)
        ))

    # === Plan Distribution ===
    plan_counts = db.query(
        Package.name,
        func.count(Subscription.id)
    ).join(Subscription, Package.id == Subscription.package_id) \
        .group_by(Package.name).all()

    total_plans = sum([count for _, count in plan_counts])
    plan_distribution = []

    if total_plans > 0:
        for plan_name, count in plan_counts:
            percentage = (count / total_plans) * 100
            plan_distribution.append(PlanDistribution(
                name=plan_name,
                value=count,
                percentage=round(percentage, 2)
            ))
    else:
        plan_distribution = [
            PlanDistribution(name="Basic", value=60, percentage=60.0),
            PlanDistribution(name="Premium", value=20, percentage=20.0),
            PlanDistribution(name="Enterprise", value=20, percentage=20.0)
        ]

    # === Recent Transactions ===
    recent_trans = db.query(Transaction).join(Company) \
        .order_by(Transaction.date.desc()) \
        .limit(5).all()

    recent_transactions = [
        RecentTransaction(
            id=t.invoice_id,
            company=db.query(Company).filter(Company.id == t.company_id).first().name,
            date=t.date.strftime("%d %b %Y"),
            amount=f"+₹{t.amount:.0f}",
            plan=t.plan or "N/A",
            logo=db.query(Company).filter(Company.id == t.company_id).first().logo or "/default-logo.png"
        )
        for t in recent_trans
    ]

    # === Recently Registered Companies ===
    recent_companies = db.query(Company) \
        .order_by(Company.created_date.desc()) \
        .limit(5).all()

    recently_registered = [
        RecentCompany(
            company=c.name,
            plan=f"{c.plan_name} ({c.plan_type})" if c.plan_name else "N/A",
            users="150 Users",  # Mocked
            domain=c.account_url or "N/A",
            logo=c.logo or "/default-logo.png"
        )
        for c in recent_companies
    ]

    # === Expired Plans ===
    today_date = today.date()
    expired = db.query(Company) \
        .filter(Company.expiring_on < today_date) \
        .order_by(Company.expiring_on.desc()) \
        .limit(5).all()

    expired_plans = [
        ExpiredPlan(
            company=c.name,
            expired=c.expiring_on.strftime("%d %b %Y") if c.expiring_on else "N/A",
            plan=f"{c.plan_name} ({c.plan_type})" if c.plan_name else "N/A",
            logo=c.logo or "/default-logo.png"
        )
        for c in expired
    ]

    # === Final Dashboard Response ===
    return DashboardResponse(
        stats=stats,
        revenue_data=revenue_data,
        plan_distribution=plan_distribution,
        recent_transactions=recent_transactions,
        recently_registered=recently_registered,
        expired_plans=expired_plans
    )


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get only dashboard statistics"""
    total_companies = db.query(Company).count()
    active_companies = db.query(Company).filter(Company.status == "Active").count()
    total_subscribers = db.query(Subscription).filter(Subscription.status == "Paid").count()
    total_earnings = db.query(func.sum(Transaction.amount)).filter(Transaction.status == "Paid").scalar() or 0.0

    return {
        "total_companies": total_companies,
        "active_companies": active_companies,
        "total_subscribers": total_subscribers,
        "total_earnings": round(total_earnings, 2)
    }
