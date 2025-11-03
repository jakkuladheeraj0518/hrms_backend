from fastapi import APIRouter
from typing import List
from app.schemas import report_schema as rs

router = APIRouter(prefix="/reports/annual", tags=["Annual Reports"])


@router.get("/annual_salary_summary", response_model=List[rs.AnnualSalarySummaryResponse])
def list_annual_salary_summary():
    return [{"id": 1, "period": "2024-25", "employees": 100, "earned_salary": 5000000.0}]


@router.get("/annual_salary_statement", response_model=List[rs.AnnualSalaryStatementResponse])
def list_annual_salary_statement():
    return [{"id": 1, "employee_id": 1, "period": "2024-25", "net_earnings": 480000.0}]


@router.get("/annual_attendance", response_model=List[rs.AttendanceRegisterResponse])
def list_annual_attendance():
    return [{"id": 1, "period": "2024", "paid_days": 240}]


@router.get("/annual_leaves", response_model=List[rs.LeaveRegisterResponse])
def list_annual_leaves():
    return [{"id": 1, "employee_name": "John", "opening": 12}]
