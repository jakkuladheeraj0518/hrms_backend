"""
Dashboard API routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from dependencies.database import get_db
from services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/overviews")
async def get_dashboard_overview(db: Session = Depends(get_db)):
    """Get overview dashboard data including stats, attendance trends, and widgets"""
    service = DashboardService(db)
    return await service.get_overview_data()


@router.get("/attendance")
async def get_attendance_dashboard(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    department: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("Recently Added"),
    db: Session = Depends(get_db)
):
    """Get attendance dashboard data with filtering options"""
    service = DashboardService(db)
    return await service.get_attendance_data(
        start_date=start_date,
        end_date=end_date,
        department=department,
        status=status,
        sort_by=sort_by
    )


@router.get("/flightrisk")
async def get_flight_risk_dashboard(
    viewing: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get flight risk dashboard data"""
    service = DashboardService(db)
    return await service.get_flight_risk_data(viewing=viewing)


@router.get("/leadsdashboard")
async def get_leads_dashboard(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """Get leads dashboard data"""
    service = DashboardService(db)
    return await service.get_leads_data(
        start_date=start_date,
        end_date=end_date
    )