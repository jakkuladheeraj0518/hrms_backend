from sqlalchemy import Column, Integer, Float, String, Boolean, Date, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    department = Column(String(50), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=True)
    daily_salary = Column(Float, nullable=True)
    joining_date = Column(Date, nullable=True)
    exit_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)

    attendances = relationship("AttendanceRecord", back_populates="employee")
    leave_balances = relationship("LeaveBalance", back_populates="employee")
    leave_encashments = relationship("LeaveEncashment", back_populates="employee")
    salary_components = relationship("SalaryComponent", back_populates="employee")
    bonus_records = relationship("BonusRecord", back_populates="employee")
    gratuity_records = relationship("GratuityRecord", back_populates="employee")
    hold_salaries = relationship("HoldSalary", back_populates="employee")

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class CostCenter(Base):
    __tablename__ = "cost_centers"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class PayrollPeriod(Base):
    __tablename__ = "payroll_periods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days = Column(Integer, nullable=False)
    status = Column(String(20), default="Open")
    is_reporting_enabled = Column(Boolean, default=False)

class RecalculationLog(Base):
    __tablename__ = "recalculation_logs"
    id = Column(Integer, primary_key=True, index=True)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    all_employees = Column(Boolean, default=False)
    status = Column(String(20), default="started")
    progress = Column(Integer, default=0)
    records_processed = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class RecalculationRateLimit(Base):
    __tablename__ = "recalculation_rate_limits"
    id = Column(Integer, primary_key=True, index=True)
    all_employees = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, nullable=False)
    check_in = Column(DateTime, nullable=True)
    check_out = Column(DateTime, nullable=True)
    hours_worked = Column(Float, default=0.0)
    status = Column(String(50), default="Absent")
    is_manual = Column(Boolean, default=False)

    employee = relationship("Employee", back_populates="attendances")

class LeaveType(Base):
    __tablename__ = "leave_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)

class LeaveBalance(Base):
    __tablename__ = "leave_balances"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), nullable=False)
    balance_days = Column(Float, default=0.0)
    balance_as_on = Column(Date, nullable=False)

    employee = relationship("Employee", back_populates="leave_balances")
    leave_type = relationship("LeaveType")

class LeaveEncashment(Base):
    __tablename__ = "leave_encashments"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), nullable=False)
    payment_period = Column(Date, nullable=False)
    leave_balance = Column(Float)
    daily_salary = Column(Float)
    encashment_days = Column(Float)
    encashment_amount = Column(Float)
    processed = Column(Boolean, default=False)

    employee = relationship("Employee", back_populates="leave_encashments")
    leave_type = relationship("LeaveType")

class SalaryComponent(Base):
    __tablename__ = "salary_components"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    basic_salary = Column(Numeric(10, 2), default=0)
    hra = Column(Numeric(10, 2), default=0)
    special_allowance = Column(Numeric(10, 2), default=0)
    medical_allowance = Column(Numeric(10, 2), default=0)
    conveyance_allowance = Column(Numeric(10, 2), default=0)
    telephone_allowance = Column(Numeric(10, 2), default=0)
    month = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    effective_from = Column(Date, nullable=False)
    is_current = Column(Boolean, default=True)

    employee = relationship("Employee", back_populates="salary_components")

class BonusConfiguration(Base):
    __tablename__ = "bonus_configurations"
    id = Column(Integer, primary_key=True, index=True)
    bonus_rate = Column(Numeric(5, 2), default=8.33)
    eligibility_cutoff = Column(Numeric(10, 2), default=21000)
    min_wages = Column(Numeric(10, 2), default=7000)
    min_bonus = Column(Numeric(10, 2), default=100)
    max_bonus = Column(Numeric(10, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class BonusRecord(Base):
    __tablename__ = "bonus_records"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    payment_period = Column(String(20), nullable=False)
    base_salary = Column(Numeric(10, 2), nullable=False)
    bonus_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)

    employee = relationship("Employee", back_populates="bonus_records")

class BonusSummary(Base):
    __tablename__ = "bonus_summaries"
    id = Column(Integer, primary_key=True, index=True)
    payment_period = Column(String(20), nullable=False)
    location_id = Column(Integer, nullable=True)
    department_id = Column(Integer, nullable=True)
    cost_center_id = Column(Integer, nullable=True)
    total_employees = Column(Integer)
    eligible_employees = Column(Integer)
    total_payable = Column(Numeric(12, 2))
    status = Column(String(50), default="generated")
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    deleted_at = Column(DateTime)

class GratuityConfiguration(Base):
    __tablename__ = "gratuity_configuration"
    id = Column(Integer, primary_key=True, index=True)
    min_years = Column(Float, nullable=False, default=5.0)
    payable_days = Column(Integer, nullable=False, default=15)
    month_days = Column(Integer, nullable=False, default=26)
    exit_only = Column(Boolean, default=False)
    year_rounding = Column(String(20), default="Round Down")
    salary_components = Column(Text, default='["Basic Salary", "House Rent Allowance", "Special Allowance"]')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class GratuityRecord(Base):
    __tablename__ = "gratuity_records"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    years_of_service = Column(Float, nullable=False)
    last_drawn_salary = Column(Numeric(10, 2), nullable=False)
    gratuity_amount = Column(Numeric(10, 2), nullable=False)
    calculation_date = Column(Date, default=datetime.utcnow)
    status = Column(String(20), default="pending")
    month = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)

    employee = relationship("Employee", back_populates="gratuity_records")

class GratuitySummary(Base):
    __tablename__ = "gratuity_summaries"
    id = Column(Integer, primary_key=True, index=True)
    total_employees = Column(Integer, default=0)
    eligible_employees = Column(Integer, default=0)
    total_payable = Column(Numeric(12, 2), default=0)
    processed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class HoldSalary(Base):
    __tablename__ = "hold_salaries"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    hold_from = Column(Date, nullable=False)
    hold_reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="hold_salaries")

class PayrollRun(Base):
    __tablename__ = "payroll_runs"
    id = Column(Integer, primary_key=True, index=True)
    period = Column(String, nullable=False, unique=True)
    run_date = Column(DateTime, nullable=False)
    runtime = Column(String)
    result = Column(String)
    total_net_payroll = Column(Float)
    status = Column(String)
