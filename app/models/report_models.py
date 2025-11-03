from sqlalchemy import Column, Integer, String, Date, Float, Text,Boolean, Enum, DateTime, ForeignKey   
from app.database import Base
import enum
from sqlalchemy.orm import relationship
from datetime import datetime


# ✅ Task 1: AI Report
class AIReport(Base):
    __tablename__ = "ai_reports"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(255), nullable=False)
    generated_report = Column(Text, nullable=False)
    created_at = Column(Date)


# ✅ Task 2: Salary Report
# app/models/report_models.py
from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

# ---------------------------
# Salary summary (detailed per employee)
# ---------------------------
class SalarySummary(Base):
    __tablename__ = "salary_summaries"
    id = Column(Integer, primary_key=True, index=True)
    period = Column(String, index=True)        # e.g., "SEP-2025"
    SN = Column(Integer, default=1)
    cost_center = Column(String, index=True)
    employeees = Column(String, index=True)
    pay_days = Column(Integer, default=0)
    earnings = Column(Float, default=0.0)
    deductions = Column(Float, default=0.0)
    net_salary = Column(Float, default=0.0)


class SalaryRegisterConfig(Base):
    __tablename__ = "salary_register_configs"

    id = Column(Integer, primary_key=True, index=True)

    # ===== Basic Details =====
    employee_code = Column(Boolean, default=False)
    employee_name = Column(Boolean, default=False)
    gender = Column(Boolean, default=False)
    date_of_birth = Column(Boolean, default=False)
    date_of_joining = Column(Boolean, default=False)
    date_of_exit = Column(Boolean, default=False)
    salary_units = Column(Boolean, default=False)

    # ===== Personal Details =====
    esi_ip_number = Column(Boolean, default=False)
    pf_uan_number = Column(Boolean, default=False)
    income_tax_pan = Column(Boolean, default=False)
    aadhar_number = Column(Boolean, default=False)
    office_email = Column(Boolean, default=False)
    mobile_phone = Column(Boolean, default=False)
    bank_name = Column(Boolean, default=False)
    bank_ifsc = Column(Boolean, default=False)
    bank_account = Column(Boolean, default=False)

    # ===== Attendance =====
    total_days = Column(Boolean, default=False)
    presents = Column(Boolean, default=False)
    absents = Column(Boolean, default=False)
    week_offs = Column(Boolean, default=False)
    holidays = Column(Boolean, default=False)
    extra_days = Column(Boolean, default=False)
    arrear_days = Column(Boolean, default=False)
    overtime_days = Column(Boolean, default=False)
    leave_breakup = Column(Boolean, default=False)
    paid_leaves = Column(Boolean, default=False)
    unpaid_leaves = Column(Boolean, default=False)
    payable_days = Column(Boolean, default=False)
    unpaid_days = Column(Boolean, default=False)

    # ===== Work Profile =====
    location = Column(Boolean, default=False)
    cost_center = Column(Boolean, default=False)
    department = Column(Boolean, default=False)
    designation = Column(Boolean, default=False)

    # ===== Excel Info =====
    show_ctc = Column(Boolean, default=False)
    show_time_strikes = Column(Boolean, default=False)

    # ===== Summarization =====
    summarize_salary = Column(Boolean, default=False)
    summarize_deductions = Column(Boolean, default=False)

    # ===== Extra Info =====
    other_info_1 = Column(Boolean, default=False)
    other_info_2 = Column(Boolean, default=False)
    other_info_3 = Column(Boolean, default=False)
    other_info_4 = Column(Boolean, default=False)
    other_info_5 = Column(Boolean, default=False)

    # ===== Rounding / Pagination =====
    amount_rounding = Column(Float, default=0)
    unit_rounding = Column(Float, default=0)
    records_per_page = Column(Integer, default=10)

class SalarySlipsConfig(Base):
    __tablename__ = "salary_Slips_configs"

    id = Column(Integer, primary_key=True, index=True)

    # ===== Basic Details =====
    employee_code = Column(Boolean, default=False)
    employee_name = Column(Boolean, default=False)
    gender = Column(Boolean, default=False)
    date_of_birth = Column(Boolean, default=False)
    date_of_joining = Column(Boolean, default=False)
    date_of_exit = Column(Boolean, default=False)
    salary_units = Column(Boolean, default=False)

    # ===== Personal Details =====
    esi_ip_number = Column(Boolean, default=False)
    pf_uan_number = Column(Boolean, default=False)
    income_tax_pan = Column(Boolean, default=False)
    aadhar_number = Column(Boolean, default=False)
    office_email = Column(Boolean, default=False)
    mobile_phone = Column(Boolean, default=False)
    bank_name = Column(Boolean, default=False)
    bank_ifsc = Column(Boolean, default=False)
    bank_account = Column(Boolean, default=False)

    # ===== Attendance =====
    total_days = Column(Boolean, default=False)
    presents = Column(Boolean, default=False)
    absents = Column(Boolean, default=False)
    week_offs = Column(Boolean, default=False)
    holidays = Column(Boolean, default=False)
    extra_days = Column(Boolean, default=False)
    arrear_days = Column(Boolean, default=False)
    overtime_days = Column(Boolean, default=False)
    leave_breakup = Column(Boolean, default=False)
    paid_leaves = Column(Boolean, default=False)
    unpaid_leaves = Column(Boolean, default=False)
    payable_days = Column(Boolean, default=False)
    unpaid_days = Column(Boolean, default=False)

    # ===== Work Profile =====
    location = Column(Boolean, default=False)
    cost_center = Column(Boolean, default=False)
    department = Column(Boolean, default=False)
    designation = Column(Boolean, default=False)

    # ===== Excel Info =====
    show_ctc = Column(Boolean, default=False)
    show_time_strikes = Column(Boolean, default=False)

    # ===== Summarization =====
    summarize_salary = Column(Boolean, default=False)
    summarize_deductions = Column(Boolean, default=False)

    # ===== Extra Info =====
    other_info_1 = Column(Boolean, default=False)
    other_info_2 = Column(Boolean, default=False)
    other_info_3 = Column(Boolean, default=False)
    other_info_4 = Column(Boolean, default=False)
    other_info_5 = Column(Boolean, default=False)

    # ===== Rounding / Pagination =====
    amount_rounding = Column(Float, default=0)
    unit_rounding = Column(Float, default=0)
    records_per_page = Column(Integer, default=10)

class BankTransferRow(Base):
    __tablename__ = "bank_transfer_rows"

    id = Column(Integer, primary_key=True, index=True)

    # --- Filter Fields ---
    business_unit = Column(String)
    location = Column(String)
    cost_center = Column(String)
    department = Column(String)

    # --- Period Info ---
    period = Column(String)

    # --- Employee Info ---
    employee_code = Column(String)
    employee_name = Column(String)

    # --- Bank Info ---
    bank_ifsc = Column(String)
    bank_name = Column(String)
    bank_account = Column(String)

    # --- Amount Info ---
    net_amount = Column(Float)

class CostToCompany(Base):
    __tablename__ = "cost_to_company"

    id = Column(Integer, primary_key=True, index=True)
    sn = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    cost_center = Column(String, nullable=True)
    department = Column(String, nullable=True)
    employee_code = Column(String, nullable=True)
    employee_name = Column(String, nullable=True)
    latest_revision_only = Column(Boolean, default=True)
    show_all_revisions = Column(Boolean, default=False)
    salary_component = Column(String, nullable=True)
    employer_cost = Column(Float, nullable=True)


# -------------------------------
# 2️⃣ Variable Salary Model
# -------------------------------
class VariableSalary(Base):
    __tablename__ = "variable_salary"

    id = Column(Integer, primary_key=True, index=True)
    sn = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    department = Column(String, nullable=True)
    salary_component = Column(String, nullable=True)
    employee_name = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    type_of_payment = Column(String, nullable=True)
    rate = Column(Float, nullable=True)
    hours = Column(Float, nullable=True)
    amount = Column(Float, nullable=True)



# ---------- 1️⃣ Statutory Bonus ----------
class StatutoryBonus(Base):
    __tablename__ = "statutory_bonus"

    id = Column(Integer, primary_key=True, index=True)
    sn = Column(Integer)
    employee_name = Column(String, nullable=False)
    department = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    comments = Column(String, nullable=True)
    bonus = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    cost_center = Column(String, nullable=True)
    month = Column(String, nullable=True)


# ---------- 2️⃣ Salary Deductions ----------
class SalaryDeduction(Base):
    __tablename__ = "salary_deductions"

    id = Column(Integer, primary_key=True, index=True)
    sn = Column(Integer)
    code = Column(String, nullable=True)
    employee_name = Column(String, nullable=False)
    department = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    cost_center = Column(String, nullable=True)
    deduction_type = Column(String, nullable=True)
    month = Column(String, nullable=True)


# ---------- 3️⃣ Employee Loans ----------
class EmployeeLoan(Base):
    __tablename__ = "employee_loans"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=True)
    cost_center = Column(String, nullable=True)
    department = Column(String, nullable=True)
    employee_name = Column(String, nullable=False)
    report_option = Column(String, nullable=True)
    issued_during = Column(String, nullable=True)
    status = Column(String, nullable=True)
    loan_amount = Column(Float, nullable=True)
    balance = Column(Float, nullable=True)


# ---------- 4️⃣ SAP Export ----------
class SAPExport(Base):
    __tablename__ = "sap_export"

    id = Column(Integer, primary_key=True, index=True)
    period = Column(String, nullable=True)
    format = Column(String, nullable=True)
    remarks = Column(String, nullable=True)



class RecordTypeEnum(str, enum.Enum):
    all = "All Records"
    active = "Active Records"
    inactive = "Inactive Records"

class AttendanceRegister(Base):
    __tablename__ = "attendance_registers"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=True)
    cost_center = Column(String, nullable=True)
    department = Column(String, nullable=True)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date, nullable=False)
    employee = Column(String, nullable=True)
    record_type = Column(Enum(RecordTypeEnum), default=RecordTypeEnum.all)
    show_time_punches = Column(Boolean, default=False)
    show_strikes = Column(Boolean, default=False)
    show_time_summary = Column(Boolean, default=False)




class TimeRegister(Base):
    __tablename__ = "time_register"

    id = Column(Integer, primary_key=True, index=True)
    employee = Column(String, nullable=False)
    shift_hrs = Column(String)
    early_in = Column(String)
    late_in = Column(String)
    in_hrs = Column(String)
    lunch = Column(String)
    out_hrs = Column(String)
    early_out = Column(String)
    late_out = Column(String)
    paid_hrs = Column(String)
    business_unit = Column(String)
    location = Column(String)
    department = Column(String)
    cost_center = Column(String)
    salary_component = Column(String)



# ------------------ 1. Strike Register ------------------
class StrikeRegister(Base):
    __tablename__ = "strike_register"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=True)
    cost_center = Column(String, nullable=True)
    deduction = Column(String, nullable=True)
    date = Column(Date, nullable=True)
    shift = Column(String, nullable=True)
    strike = Column(String, nullable=True)
    strike_count = Column(Integer, nullable=True)
    base_amount = Column(Float, nullable=True)
    deduction_type = Column(String, nullable=True)
    deduction_amount = Column(Float, nullable=True)


# ------------------ 2. Travel Register ------------------
class TravelRegister(Base):
    __tablename__ = "travel_register"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=True)
    cost_center = Column(String, nullable=True)
    department = Column(String, nullable=True)
    from_date = Column(Date, nullable=True)
    to_date = Column(Date, nullable=True)
    salary_component = Column(String, nullable=True)
    employee_id = Column(String, nullable=True)
    employee_name = Column(String, nullable=True)
    distance = Column(Float, nullable=True)
    exclude_zero_distance = Column(Boolean, default=False)


# ------------------ 3. Time Punches ------------------
class TimePunch(Base):
    __tablename__ = "time_punches"

    id = Column(Integer, primary_key=True, index=True)
    business_unit = Column(String, nullable=True)
    location = Column(String, nullable=True)
    cost_center = Column(String, nullable=True)
    department = Column(String, nullable=True)
    from_date = Column(Date, nullable=True)
    to_date = Column(Date, nullable=True)
    employee_name = Column(String, nullable=True)
    punch_in_time = Column(DateTime, nullable=True)
    punch_out_time = Column(DateTime, nullable=True)
    total_hours = Column(Float, nullable=True)
    status = Column(String, nullable=True)


# ------------------ 4. Remote Punch ------------------
class RemotePunch(Base):
    __tablename__ = "remote_punch"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=True)
    cost_center = Column(String, nullable=True)
    department = Column(String, nullable=True)
    from_date = Column(Date, nullable=True)
    to_date = Column(Date, nullable=True)
    employee_name = Column(String, nullable=True)
    datetime = Column(DateTime, nullable=True)
    location_coordinates = Column(String, nullable=True)
    hide_empty_records = Column(Boolean, default=False)


# ------------------ 5. Manual Updates ------------------
class ManualUpdate(Base):
    __tablename__ = "manual_updates"

    id = Column(Integer, primary_key=True, index=True)
    business_unit = Column(String, nullable=True)
    location = Column(String, nullable=True)
    department = Column(String, nullable=True)
    cost_center = Column(String, nullable=True)
    salary_component = Column(String, nullable=True)
    show_details = Column(Boolean, default=False)
    month = Column(String, nullable=True)
    employee_name = Column(String, nullable=True)
    remarks = Column(String, nullable=True)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String, unique=True, nullable=False)
    employee_name = Column(String, nullable=False)
    gender = Column(String)
    date_of_birth = Column(Date)
    date_of_joining = Column(Date)
    date_of_exit = Column(Date)
    location = Column(String)
    cost_center = Column(String)
    department = Column(String)
    grade = Column(String)
    designation = Column(String)
    aadhaar_no = Column(String)
    pan_no = Column(String)
    esi_no = Column(String)
    pf_uan_no = Column(String)
    mobile_number = Column(String)
    bank_name = Column(String)
    bank_ifsc = Column(String)
    bank_account = Column(String)
    home_phone = Column(String)
    personal_email = Column(String)
    other_info_1 = Column(String)
    other_info_2 = Column(String)
    other_info_3 = Column(String)
    other_info_4 = Column(String)
    other_info_5 = Column(String)

    # Relationships
    addresses = relationship("EmployeeAddress", back_populates="employee")
    events = relationship("EmployeeEvent", back_populates="employee")
    joinings = relationship("EmployeeJoining", back_populates="employee")
    exits = relationship("EmployeeExit", back_populates="employee")


class EmployeeAddress(Base):
    __tablename__ = "employee_addresses"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    address_type = Column(String)
    address_line_1 = Column(String)
    address_line_2 = Column(String)
    city = Column(String)
    pincode = Column(String)
    state = Column(String)
    country = Column(String)

    employee = relationship("Employee", back_populates="addresses")


class EmployeeEvent(Base):
    __tablename__ = "employee_events"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    event_type = Column(String)  # Birthday, Work Anniversary, Wedding Anniversary
    date = Column(Date)
    location = Column(String)
    department = Column(String)
    designation = Column(String)

    employee = relationship("Employee", back_populates="events")


class PromotionAgeing(Base):
    __tablename__ = "promotion_ageing"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    designation = Column(String)
    department = Column(String)
    last_promoted = Column(Date)
    ageing = Column(String)
    grade = Column(String)

    employee = relationship("Employee")


class IncrementAgeing(Base):
    __tablename__ = "increment_ageing"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    designation = Column(String)
    department = Column(String)
    last_increment = Column(Date)
    ageing = Column(String)
    grade = Column(String)

    employee = relationship("Employee")


class EmployeeJoining(Base):
    __tablename__ = "employee_joinings"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    joining_date = Column(Date)
    confirmation_date = Column(Date)
    location = Column(String)
    department = Column(String)
    designation = Column(String)
    grade = Column(String)

    employee = relationship("Employee", back_populates="joinings")


class EmployeeExit(Base):
    __tablename__ = "employee_exits"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    location = Column(String)
    department = Column(String)
    designation = Column(String)
    joining_date = Column(Date)
    exit_date = Column(Date)
    reason_of_exit = Column(String)
    employee = relationship("Employee", back_populates="exits")
from sqlalchemy import Column, Integer, String, Date, Float
from app.database import Base

# 1️⃣ Vaccination Status
class VaccinationStatus(Base):
    __tablename__ = "vaccination_status"
    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    employee_code = Column(String)
    department = Column(String)
    designation = Column(String)
    location = Column(String)
    vaccine_name = Column(String)
    dose_1_date = Column(Date)
    dose_2_date = Column(Date)
    booster_date = Column(Date)
    status = Column(String)

# 2️⃣ Workman Status
class WorkmanStatus(Base):
    __tablename__ = "workman_status"
    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    employee_code = Column(String)
    department = Column(String)
    designation = Column(String)
    workman_type = Column(String)
    uan_number = Column(String)
    esi_number = Column(String)
    pf_number = Column(String)
    location = Column(String)
    status = Column(String)

# 3️⃣ Employee Assets
class EmployeeAssets(Base):
    __tablename__ = "employee_assets"
    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    employee_code = Column(String)
    asset_name = Column(String)
    asset_code = Column(String)
    issue_date = Column(Date)
    return_date = Column(Date)
    condition = Column(String)
    remarks = Column(String)

# 4️⃣ Employee Relatives
class EmployeeRelatives(Base):
    __tablename__ = "employee_relatives"
    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    employee_code = Column(String)
    relation_name = Column(String)
    relation_type = Column(String)
    contact_number = Column(String)
    dob = Column(Date)
    address = Column(String)

# 5️⃣ Inactive Employees
class InactiveEmployees(Base):
    __tablename__ = "inactive_employees"
    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    employee_code = Column(String)
    department = Column(String)
    designation = Column(String)
    location = Column(String)
    join_date = Column(Date)
    resign_date = Column(Date)
    reason = Column(String)

# 6️⃣ ESI Deduction
class ESIDeduction(Base):
    __tablename__ = "esi_deduction"
    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    employee_code = Column(String)
    esi_number = Column(String)
    gross_salary = Column(Float)
    esi_amount = Column(Float)
    month = Column(String)
    year = Column(Integer)
    location = Column(String)

# 7️⃣ ESI Coverage
class ESICoverage(Base):
    __tablename__ = "esi_coverage"
    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    employee_code = Column(String)
    esi_number = Column(String)
    department = Column(String)
    designation = Column(String)
    coverage_start = Column(Date)
    coverage_end = Column(Date)
    location = Column(String)
    status = Column(String)

# 8️⃣ PF Deduction
class PFDeduction(Base):
    __tablename__ = "pf_deduction"
    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    employee_code = Column(String)
    uan_number = Column(String)
    pf_number = Column(String)
    basic_salary = Column(Float)
    pf_amount = Column(Float)
    month = Column(String)
    year = Column(Integer)
    location = Column(String)

# 9️⃣ PF Coverage
class PFCoverage(Base):
    __tablename__ = "pf_coverage"
    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    employee_code = Column(String)
    uan_number = Column(String)
    pf_number = Column(String)
    department = Column(String)
    designation = Column(String)
    coverage_start = Column(Date)
    coverage_end = Column(Date)
    status = Column(String)
    location = Column(String)

# 🔟 Overtime Register
class OvertimeRegister(Base):
    __tablename__ = "overtime_register"
    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String)
    employee_code = Column(String)
    department = Column(String)
    designation = Column(String)
    date = Column(Date)
    shift = Column(String)
    ot_hours = Column(Float)
    rate_per_hour = Column(Float)
    ot_amount = Column(Float)
    remarks = Column(String)
#  1. Register of Leaves
# -----------------------------
class RegisterOfLeaves(Base):
    __tablename__ = "register_of_leaves"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(100), nullable=False)
    cost_center = Column(String(100), nullable=True)
    year = Column(Integer, nullable=False)
    month_to = Column(String(50), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


# -----------------------------
# 2. Income Tax Declarations
# -----------------------------
class IncomeTaxDeclaration(Base):
    __tablename__ = "income_tax_declarations"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String(150), nullable=False)
    pan_no = Column(String(20), nullable=True)
    last_updated = Column(DateTime)
    chapter_via = Column(String(100), nullable=True)
    rent_paid = Column(Float, nullable=True)
    tax_regime = Column(String(50), nullable=True)
    location = Column(String(100), nullable=True)
    financial_year = Column(String(20), nullable=False)
    is_active_employee = Column(Boolean, default=True)
    exclude_no_declaration = Column(Boolean, default=False)


# -----------------------------
# 3. Income Tax Computation
# -----------------------------
class IncomeTaxComputation(Base):
    __tablename__ = "income_tax_computation"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255))
    request_on = Column(DateTime)
    location = Column(String(100))
    department = Column(String(100))
    cost_center = Column(String(100))
    employee_count = Column(Integer)
    month_year = Column(String(20))
    download_status = Column(String(50), default="Pending")





# ---------------- LABOUR WELFARE FUND ----------------
class LabourWelfareFund(Base):
    __tablename__ = "labour_welfare_fund"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), nullable=False)
    employee_name = Column(String(100), nullable=False)
    location = Column(String(100))
    state = Column(String(100))
    salary = Column(Float, default=0.0)
    deduction = Column(Float, default=0.0)
    contribution = Column(Float, default=0.0)
    month = Column(String(20))
    cost_center = Column(String(100))
    department = Column(String(100))


# ---------------- TDS RETURN ----------------
class TDSReturn(Base):
    __tablename__ = "tds_return"

    id = Column(Integer, primary_key=True, index=True)
    return_period_year = Column(Integer, nullable=False)
    return_period_quarter = Column(String(20), nullable=False)
    regular_24q_prev_period = Column(String(10), nullable=False)  # Yes/No
    token_no = Column(String(100), nullable=False)
    change_in_employer_address = Column(String(10), default="No")
    change_in_responsible_person_address = Column(String(10), default="No")


# ---------------- CHALLAN DETAILS ----------------
class ChallanDetails(Base):
    __tablename__ = "challan_details"

    id = Column(Integer, primary_key=True, index=True)
    tds_return_id = Column(Integer, ForeignKey("tds_return.id", ondelete="CASCADE"))
    selected_period = Column(String(20))
    nil_tax_return = Column(Boolean, default=False)
    deposit_by_book_entry = Column(String(10), default="No")
    challan_serial_no = Column(String(50))
    minor_head = Column(String(100))
    branch_code = Column(String(50))
    challan_date = Column(Date)
    payment_date = Column(Date)
    deduction_date = Column(Date)
    income_tax = Column(Float, default=0.0)
    cess = Column(Float, default=0.0)
    interest = Column(Float, default=0.0)
    others = Column(Float, default=0.0)
    fee = Column(Float, default=0.0)


class Form16(Base):
    __tablename__ = "form16"

    id = Column(Integer, primary_key=True, index=True)
    financial_year = Column(String, nullable=False)
    date_of_issue = Column(Date, nullable=False)
    location = Column(String)
    cost_center = Column(String)
    department = Column(String)
    employee_id = Column(Integer, ForeignKey("employees.id"))

    employee = relationship("Employee", back_populates="form16_records")


class AnnualSalarySummary(Base):
    __tablename__ = "annual_salary_summary"

    id = Column(Integer, primary_key=True, index=True)
    period = Column(String, nullable=False)
    employees = Column(Integer)
    earned_salary = Column(Float)
    deductions = Column(Float)
    net_salary = Column(Float)
    paid_days = Column(Integer)
    unpaid_days = Column(Integer)
    location = Column(String)
    department = Column(String)
    cost_center = Column(String)


class AnnualSalaryStatement(Base):
    __tablename__ = "annual_salary_statement"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    period = Column(String, nullable=False)

    basic_salary = Column(Float)
    house_rent_allowance = Column(Float)
    medical_allowance = Column(Float)
    special_allowance = Column(Float)
    conveyance_allowance = Column(Float)
    telephone_allowance = Column(Float)
    total_earnings = Column(Float)

    group_insurance = Column(Float)
    gratuity = Column(Float)
    pf_deduction = Column(Float)
    professional_tax = Column(Float)
    total_deductions = Column(Float)
    net_earnings = Column(Float)

    employee = relationship("Employee", back_populates="salary_statements")



class LeaveRegister(Base):
    __tablename__ = "leave_register"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    leave_type = Column(String)
    opening = Column(Float)
    taken = Column(Float)
    granted = Column(Float)
    lapsed = Column(Float)
    encashed = Column(Float)
    correction = Column(Float)
    closing = Column(Float)
    period = Column(String)

    employee = relationship("Employee", back_populates="leave_records")


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    action = Column(String, nullable=False)
    description = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)