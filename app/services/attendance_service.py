# app/services/attendance_service.py
from sqlalchemy.orm import Session
from datetime import datetime, date, time as dtime
from typing import Optional, List
from dateutil import parser

from app.models.attendance import DailyAttendance, MonthlyAttendance, DailyPunch
from app.repositories.attendance_repo import AttendanceRepo

def calculate_hours(check_in: Optional[dtime], check_out: Optional[dtime]) -> Optional[float]:
    if check_in and check_out:
        dt_in = datetime.combine(date.today(), check_in)
        dt_out = datetime.combine(date.today(), check_out)
        diff = dt_out - dt_in
        return round(diff.total_seconds() / 3600.0, 2)
    return None

def update_or_create_daily(db: Session, employee_code: str, date_val: date, check_in=None, check_out=None, status=None):
    existing = AttendanceRepo.get_daily_by_employee_date(db, employee_code, date_val)
    if existing:
        if check_in is not None:
            existing.check_in = check_in
        if check_out is not None:
            existing.check_out = check_out
        if status is not None:
            existing.status = status
        existing.total_hours = calculate_hours(existing.check_in, existing.check_out)
        db.add(existing)
        db.flush()
        return existing
    else:
        new = DailyAttendance(
            employee_code=employee_code,
            date=date_val,
            check_in=check_in,
            check_out=check_out,
            status=status,
            total_hours=calculate_hours(check_in, check_out),
        )
        db.add(new)
        db.flush()
        return new

def create_punch(db: Session, employee_code: str, punch_time: datetime, punch_type: str = None, remarks: str = None):
    punch = DailyPunch(employee_code=employee_code, punch_time=punch_time, punch_type=punch_type, remarks=remarks)
    db.add(punch)
    db.flush()
    # also try to update dailyattendance check_in/check_out if same day
    day = punch_time.date()
    daily = AttendanceRepo.get_daily_by_employee_date(db, employee_code, day)
    if not daily:
        # create a daily record with check_in as this punch (simple heuristic)
        from app.models.attendance import DailyAttendance
        daily = DailyAttendance(employee_code=employee_code, date=day, check_in=punch_time.time(), check_out=None, status="P")
        db.add(daily)
    else:
        # if check_in empty and this is earlier, set as check_in; if later than existing check_in we might ignore
        if not daily.check_in or punch_time.time() < daily.check_in:
            daily.check_in = punch_time.time()
        if not daily.check_out or punch_time.time() > daily.check_out:
            daily.check_out = punch_time.time()
        daily.total_hours = calculate_hours(daily.check_in, daily.check_out)
        db.add(daily)
    db.flush()
    return punch

def recalc_monthly_for_employee_month(db: Session, employee_code: str, month: int, year: int):
    # Calculate counts from dailyattendance
    from sqlalchemy import extract
    q = db.query(DailyAttendance).filter(
        DailyAttendance.employee_code == employee_code,
        extract('month', DailyAttendance.date) == month,
        extract('year', DailyAttendance.date) == year
    )
    total = q.count()
    present = q.filter(DailyAttendance.status == 'P').count()
    absent = q.filter(DailyAttendance.status == 'A').count()
    leaves = q.filter(DailyAttendance.status == 'CL').count()
    month_name = datetime(year, month, 1).strftime("%B")
    existing = db.query(MonthlyAttendance).filter(
        MonthlyAttendance.employee_code == employee_code,
        MonthlyAttendance.month == month_name,
        MonthlyAttendance.year == year
    ).first()
    if existing:
        existing.total_present_days = present
        existing.total_absent_days = absent
        existing.total_leaves = leaves
        db.add(existing)
        db.flush()
        return existing
    else:
        new = MonthlyAttendance(employee_code=employee_code,
                                month=month_name, year=year,
                                total_present_days=present,
                                total_absent_days=absent,
                                total_leaves=leaves)
        db.add(new)
        db.flush()
        return new
