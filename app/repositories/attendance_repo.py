# app/repositories/attendance_repo.py
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date

from app.models.attendance import (
    AttendanceEmployee,
    AttendanceModal,
    CalendarTable,
    DailyAttendance,
    DailyPunch,
    LeaveCorrection,
    ManualAttendance,
    MonthlyAttendance,
)

class AttendanceRepo:
    # Employee
    @staticmethod
    def create_employee(db: Session, obj: AttendanceEmployee):
        db.add(obj)
        db.flush()
        return obj

    @staticmethod
    def get_employee_by_code(db: Session, code: str) -> Optional[AttendanceEmployee]:
        return db.query(AttendanceEmployee).filter(AttendanceEmployee.employee_code == code).first()

    @staticmethod
    def list_employees(db: Session, skip: int = 0, limit: int = 100) -> List[AttendanceEmployee]:
        return db.query(AttendanceEmployee).offset(skip).limit(limit).all()

    # Generic helpers for other tables
    @staticmethod
    def get_daily_by_employee_date(db: Session, employee_code: str, date_val: date):
        return db.query(DailyAttendance).filter(DailyAttendance.employee_code==employee_code,
                                               DailyAttendance.date==date_val).first()

    @staticmethod
    def list_daily_by_date(db: Session, date_val: date):
        return db.query(DailyAttendance).filter(DailyAttendance.date == date_val).all()

    # You can add more direct query helpers here as needed.
