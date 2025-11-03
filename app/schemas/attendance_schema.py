from typing import Optional, List
from datetime import date, time, datetime
from pydantic import BaseModel, Field

# ✅ Pydantic v2 compatibility
class BaseConfig:
    model_config = {"from_attributes": True}


# -------------------------------------------------
# Employee
# -------------------------------------------------
class AttendanceEmployeeBase(BaseModel):
    employee_code: str
    employee_name: str
    designation: Optional[str] = None
    department: Optional[str] = None

    model_config = {"from_attributes": True}


class AttendanceEmployeeCreate(AttendanceEmployeeBase):
    pass


class AttendanceEmployeeUpdate(BaseModel):
    employee_name: Optional[str]
    designation: Optional[str]
    department: Optional[str]

    model_config = {"from_attributes": True}


class AttendanceEmployeeOut(AttendanceEmployeeBase):
    id: int
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}


# -------------------------------------------------
# AttendanceModal
# -------------------------------------------------
class AttendanceModalBase(BaseModel):
    employee_code: str
    date: date
    status: str
    remarks: Optional[str] = None

    model_config = {"from_attributes": True}


class AttendanceModalCreate(AttendanceModalBase):
    pass


class AttendanceModalOut(AttendanceModalBase):
    id: int

    model_config = {"from_attributes": True}


# -------------------------------------------------
# CalendarTable
# -------------------------------------------------
class CalendarTableBase(BaseModel):
    date: date
    day_name: Optional[str] = None
    is_holiday: Optional[bool] = False
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class CalendarTableCreate(CalendarTableBase):
    pass


class CalendarTableOut(CalendarTableBase):
    id: int

    model_config = {"from_attributes": True}


# -------------------------------------------------
# DailyAttendance
# -------------------------------------------------
class DailyAttendanceBase(BaseModel):
    employee_code: str
    date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: Optional[str] = None
    total_hours: Optional[float] = None

    model_config = {"from_attributes": True}


class DailyAttendanceCreate(DailyAttendanceBase):
    pass


class DailyAttendanceUpdate(BaseModel):
    check_in: Optional[time]
    check_out: Optional[time]
    status: Optional[str]

    model_config = {"from_attributes": True}


class DailyAttendanceOut(DailyAttendanceBase):
    id: int

    model_config = {"from_attributes": True}


# -------------------------------------------------
# ✅ DailyPunch (Improved Swagger Output)
# -------------------------------------------------
class DailyPunchBase(BaseModel):
    employee_code: str
    punch_time: datetime
    punch_type: Optional[str] = Field(default=None, description="Type of punch (Selfie/Remote/Manual)")
    remarks: Optional[str] = Field(default=None, description="Optional remarks for punch")

    model_config = {"from_attributes": True}


class DailyPunchCreate(DailyPunchBase):
    pass


class DailyPunchOut(DailyPunchBase):
    id: int
    formatted_punch_time: Optional[str] = Field(
        default=None,
        description="Punch time formatted as YYYY-MM-DD HH:MM:SS"
    )

    model_config = {"from_attributes": True}


# -------------------------------------------------
# LeaveCorrection
# -------------------------------------------------
class LeaveCorrectionBase(BaseModel):
    employee_code: str
    date: date
    leave_type: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = "Pending"

    model_config = {"from_attributes": True}


class LeaveCorrectionCreate(LeaveCorrectionBase):
    pass


class LeaveCorrectionOut(LeaveCorrectionBase):
    id: int

    model_config = {"from_attributes": True}


# -------------------------------------------------
# ManualAttendance
# -------------------------------------------------
class ManualAttendanceBase(BaseModel):
    employee_code: str
    date: date
    in_time: Optional[time] = None
    out_time: Optional[time] = None
    approved_by: Optional[str] = None
    remarks: Optional[str] = None

    model_config = {"from_attributes": True}


class ManualAttendanceCreate(ManualAttendanceBase):
    pass


class ManualAttendanceOut(ManualAttendanceBase):
    id: int

    model_config = {"from_attributes": True}


# -------------------------------------------------
# MonthlyAttendance
# -------------------------------------------------
class MonthlyAttendanceBase(BaseModel):
    employee_code: str
    month: str
    year: int
    total_present_days: Optional[int] = 0
    total_absent_days: Optional[int] = 0
    total_leaves: Optional[int] = 0

    model_config = {"from_attributes": True}


class MonthlyAttendanceCreate(MonthlyAttendanceBase):
    pass


class MonthlyAttendanceOut(MonthlyAttendanceBase):
    id: int
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
