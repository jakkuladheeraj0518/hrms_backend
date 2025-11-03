# app/models/attendance.py
from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Float, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database.base import Base

# Single file contains all 8 models to match your migrations

class AttendanceEmployee(Base):
    __tablename__ = "attendanceemployee"
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, nullable=False, index=True)
    employee_name = Column(String(100), nullable=False)
    designation = Column(String(100))
    department = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

    # relationships (optional helpers)
    modals = relationship("AttendanceModal", back_populates="employee", cascade="all, delete-orphan")
    daily = relationship("DailyAttendance", back_populates="employee", cascade="all, delete-orphan")
    punches = relationship("DailyPunch", back_populates="employee", cascade="all, delete-orphan")
    leave_corrections = relationship("LeaveCorrection", back_populates="employee", cascade="all, delete-orphan")
    manual_attendances = relationship("ManualAttendance", back_populates="employee", cascade="all, delete-orphan")
    monthly = relationship("MonthlyAttendance", back_populates="employee", cascade="all, delete-orphan")


class AttendanceModal(Base):
    __tablename__ = "attendancemodal"
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), ForeignKey("attendanceemployee.employee_code"))
    date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)
    remarks = Column(String(255))

    employee = relationship("AttendanceEmployee", back_populates="modals")


class CalendarTable(Base):
    __tablename__ = "calendartable"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False)
    day_name = Column(String(20))
    is_holiday = Column(Boolean, default=False)
    description = Column(String(200))


class DailyAttendance(Base):
    __tablename__ = "dailyattendance"
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), ForeignKey("attendanceemployee.employee_code"))
    date = Column(Date, nullable=False)
    check_in = Column(Time)
    check_out = Column(Time)
    status = Column(String(20))
    total_hours = Column(Float)

    employee = relationship("AttendanceEmployee", back_populates="daily")


class DailyPunch(Base):
    __tablename__ = "dailypunch"
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), ForeignKey("attendanceemployee.employee_code"))
    punch_time = Column(DateTime, nullable=False)
    punch_type = Column(String(20))  # selfie/manual/remote
    remarks = Column(String(255))

    employee = relationship("AttendanceEmployee", back_populates="punches")


class LeaveCorrection(Base):
    __tablename__ = "leavecorrection"
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), ForeignKey("attendanceemployee.employee_code"))
    date = Column(Date, nullable=False)
    leave_type = Column(String(50))
    reason = Column(String(255))
    status = Column(String(20), default="Pending")

    employee = relationship("AttendanceEmployee", back_populates="leave_corrections")


class ManualAttendance(Base):
    __tablename__ = "manualattendance"
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), ForeignKey("attendanceemployee.employee_code"))
    date = Column(Date, nullable=False)
    in_time = Column(Time)
    out_time = Column(Time)
    approved_by = Column(String(100))
    remarks = Column(String(255))

    employee = relationship("AttendanceEmployee", back_populates="manual_attendances")


class MonthlyAttendance(Base):
    __tablename__ = "monthlyattendance"
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), ForeignKey("attendanceemployee.employee_code"))
    month = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    total_present_days = Column(Integer)
    total_absent_days = Column(Integer)
    total_leaves = Column(Integer)
    updated_at = Column(DateTime, server_default=func.now())

    employee = relationship("AttendanceEmployee", back_populates="monthly")
