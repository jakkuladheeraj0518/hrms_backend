from fastapi import APIRouter
from typing import List
from app.schemas import report_schema as rs
from datetime import date

router = APIRouter(prefix="/reports/attendance", tags=["Attendance Reports"])


@router.get("/attendance_register", response_model=List[rs.AttendanceRegisterResponse])
def list_attendance_register():
    return [{"id": 1, "location": "LOC1", "from_date": date.today(), "to_date": date.today()}]


@router.get("/leave_register", response_model=List[rs.LeaveRegisterResponse])
def list_leave_register():
    return [{"id": 1, "employee_name": "John", "employee_code": "E001"}]


@router.get("/time_register", response_model=List[rs.TimeRegisterResponse])
def list_time_register():
    return [{"id": 1, "employee": "John", "shift_hrs": "09:00-18:00"}]


@router.get("/strike_register", response_model=List[rs.StrikeRegisterResponse])
def list_strike_register():
    return [{"id": 1, "location": "LOC1", "strike_count": 1, "deduction_amount": 100.0}]


@router.get("/travel_register", response_model=List[rs.TravelRegisterResponse])
def list_travel_register():
    return [{"id": 1, "employee_name": "John", "distance": 12.5}]


@router.get("/time_punches", response_model=List[rs.TimePunchResponse])
def list_time_punches():
    return [{"id": 1, "employee_name": "John"}]


@router.get("/remote_punch", response_model=List[rs.RemotePunchResponse])
def list_remote_punch():
    return [{"id": 1, "employee_name": "John"}]


@router.get("/manual_updates", response_model=List[rs.ManualUpdateResponse])
def list_manual_updates():
    return [{"id": 1, "employee_name": "John", "remarks": "Manual update sample"}]
