# app/schemas/report_schema.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# ---------------------------
# AI Report
# ---------------------------
class AIReportResponse(BaseModel):
    id: Optional[int] = None
    query: Optional[str] = None
    generated_report: Optional[str] = None
    created_at: Optional[date] = None

    class Config:
        orm_mode = True

# ---------------------------
# Salary / Payroll related
# ---------------------------
class SalarySummaryResponse(BaseModel):
    id: Optional[int] = None
    period: Optional[str] = None
    # include both variants present in models / routers
    SN: Optional[int] = None
    sn: Optional[int] = None
    cost_center: Optional[str] = None
    # include both spelling variants
    employeees: Optional[str] = None
    employees: Optional[str] = None
    pay_days: Optional[int] = None
    earnings: Optional[float] = None
    deductions: Optional[float] = None
    net_salary: Optional[float] = None

    class Config:
        orm_mode = True


class SalaryRegisterConfigResponse(BaseModel):
    id: Optional[int] = None
    # representative subset of boolean flags (models have many booleans)
    employee_code: Optional[bool] = None
    employee_name: Optional[bool] = None
    gender: Optional[bool] = None
    date_of_birth: Optional[bool] = None
    date_of_joining: Optional[bool] = None
    date_of_exit: Optional[bool] = None
    salary_units: Optional[bool] = None

    # attendance / work profile flags (subset)
    total_days: Optional[bool] = None
    presents: Optional[bool] = None
    location: Optional[bool] = None
    cost_center: Optional[bool] = None
    department: Optional[bool] = None
    records_per_page: Optional[int] = None
    amount_rounding: Optional[float] = None
    unit_rounding: Optional[float] = None

    class Config:
        orm_mode = True


class SalarySlipsConfigResponse(BaseModel):
    id: Optional[int] = None
    # mirror same flags as SalaryRegisterConfig (subset)
    employee_code: Optional[bool] = None
    employee_name: Optional[bool] = None
    show_ctc: Optional[bool] = None
    summarize_salary: Optional[bool] = None
    records_per_page: Optional[int] = None

    class Config:
        orm_mode = True


class BankTransferRowResponse(BaseModel):
    id: Optional[int] = None
    business_unit: Optional[str] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    department: Optional[str] = None
    period: Optional[str] = None
    employee_code: Optional[str] = None
    employee_name: Optional[str] = None
    bank_ifsc: Optional[str] = None
    bank_name: Optional[str] = None
    bank_account: Optional[str] = None
    net_amount: Optional[float] = None

    class Config:
        orm_mode = True


class CostToCompanyResponse(BaseModel):
    id: Optional[int] = None
    sn: Optional[int] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    department: Optional[str] = None
    employee_code: Optional[str] = None
    employee_name: Optional[str] = None
    latest_revision_only: Optional[bool] = None
    show_all_revisions: Optional[bool] = None
    salary_component: Optional[str] = None
    employer_cost: Optional[float] = None

    class Config:
        orm_mode = True


class VariableSalaryResponse(BaseModel):
    id: Optional[int] = None
    sn: Optional[int] = None
    location: Optional[str] = None
    department: Optional[str] = None
    salary_component: Optional[str] = None
    employee_name: Optional[str] = None
    designation: Optional[str] = None
    type_of_payment: Optional[str] = None
    rate: Optional[float] = None
    hours: Optional[float] = None
    amount: Optional[float] = None

    class Config:
        orm_mode = True


class StatutoryBonusResponse(BaseModel):
    id: Optional[int] = None
    sn: Optional[int] = None
    employee_name: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    comments: Optional[str] = None
    bonus: Optional[float] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    month: Optional[str] = None

    class Config:
        orm_mode = True


class SalaryDeductionResponse(BaseModel):
    id: Optional[int] = None
    sn: Optional[int] = None
    code: Optional[str] = None
    employee_name: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    amount: Optional[float] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    deduction_type: Optional[str] = None
    month: Optional[str] = None

    class Config:
        orm_mode = True


class EmployeeLoanResponse(BaseModel):
    id: Optional[int] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    department: Optional[str] = None
    employee_name: Optional[str] = None
    report_option: Optional[str] = None
    issued_during: Optional[str] = None
    status: Optional[str] = None
    loan_amount: Optional[float] = None
    balance: Optional[float] = None

    class Config:
        orm_mode = True


class SAPExportResponse(BaseModel):
    id: Optional[int] = None
    period: Optional[str] = None
    format: Optional[str] = None
    remarks: Optional[str] = None

    class Config:
        orm_mode = True


# ---------------------------
# Employee related
# ---------------------------
class EmployeeResponse(BaseModel):
    id: Optional[int] = None
    employee_code: Optional[str] = None
    employee_name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    date_of_joining: Optional[date] = None
    date_of_exit: Optional[date] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    department: Optional[str] = None
    grade: Optional[str] = None
    designation: Optional[str] = None
    aadhaar_no: Optional[str] = None
    pan_no: Optional[str] = None
    esi_no: Optional[str] = None
    pf_uan_no: Optional[str] = None
    mobile_number: Optional[str] = None
    bank_name: Optional[str] = None
    bank_ifsc: Optional[str] = None
    bank_account: Optional[str] = None
    home_phone: Optional[str] = None
    personal_email: Optional[str] = None
    other_info_1: Optional[str] = None
    other_info_2: Optional[str] = None
    other_info_3: Optional[str] = None
    other_info_4: Optional[str] = None
    other_info_5: Optional[str] = None

    class Config:
        orm_mode = True


class EmployeeAddressResponse(BaseModel):
    id: Optional[int] = None
    employee_id: Optional[int] = None
    address_type: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

    class Config:
        orm_mode = True


class EmployeeEventResponse(BaseModel):
    id: Optional[int] = None
    employee_id: Optional[int] = None
    event_type: Optional[str] = None
    date: Optional[date] = None
    location: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None

    class Config:
        orm_mode = True


class PromotionAgeingResponse(BaseModel):
    id: Optional[int] = None
    employee_id: Optional[int] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    last_promoted: Optional[date] = None
    ageing: Optional[str] = None
    grade: Optional[str] = None

    class Config:
        orm_mode = True


class IncrementAgeingResponse(BaseModel):
    id: Optional[int] = None
    employee_id: Optional[int] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    last_increment: Optional[date] = None
    ageing: Optional[str] = None
    grade: Optional[str] = None

    class Config:
        orm_mode = True


class EmployeeJoiningResponse(BaseModel):
    id: Optional[int] = None
    employee_id: Optional[int] = None
    joining_date: Optional[date] = None
    confirmation_date: Optional[date] = None
    location: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    grade: Optional[str] = None

    class Config:
        orm_mode = True


class EmployeeExitResponse(BaseModel):
    id: Optional[int] = None
    employee_id: Optional[int] = None
    location: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    joining_date: Optional[date] = None
    exit_date: Optional[date] = None
    reason_of_exit: Optional[str] = None

    class Config:
        orm_mode = True


class VaccinationStatusResponse(BaseModel):
    id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    location: Optional[str] = None
    vaccine_name: Optional[str] = None
    dose_1_date: Optional[date] = None
    dose_2_date: Optional[date] = None
    booster_date: Optional[date] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True


class WorkmanStatusResponse(BaseModel):
    id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    workman_type: Optional[str] = None
    uan_number: Optional[str] = None
    esi_number: Optional[str] = None
    pf_number: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True


class EmployeeAssetsResponse(BaseModel):
    id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    asset_name: Optional[str] = None
    asset_code: Optional[str] = None
    issue_date: Optional[date] = None
    return_date: Optional[date] = None
    condition: Optional[str] = None
    remarks: Optional[str] = None

    class Config:
        orm_mode = True


class EmployeeRelativesResponse(BaseModel):
    id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    relation_name: Optional[str] = None
    relation_type: Optional[str] = None
    contact_number: Optional[str] = None
    dob: Optional[date] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True


class InactiveEmployeesResponse(BaseModel):
    id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    location: Optional[str] = None
    join_date: Optional[date] = None
    resign_date: Optional[date] = None
    reason: Optional[str] = None

    class Config:
        orm_mode = True


# ---------------------------
# Attendance / Time related
# ---------------------------
class AttendanceRegisterResponse(BaseModel):
    id: Optional[int] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    department: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    employee: Optional[str] = None
    record_type: Optional[str] = None
    show_time_punches: Optional[bool] = None
    show_strikes: Optional[bool] = None
    show_time_summary: Optional[bool] = None

    # also used in annual endpoints
    period: Optional[str] = None
    paid_days: Optional[int] = None
    unpaid_days: Optional[int] = None

    class Config:
        orm_mode = True


class LeaveRegisterResponse(BaseModel):
    # used both as model and router response (two variants present in code)
    id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    joining_date: Optional[date] = None
    confirmation_date: Optional[date] = None
    location: Optional[str] = None
    designation: Optional[str] = None
    date: Optional[date] = None
    remarks: Optional[str] = None
    cost_center: Optional[str] = None
    department: Optional[str] = None
    leave_type: Optional[str] = None
    record_type: Optional[str] = None

    # additional fields used in annual leaves endpoint
    opening: Optional[float] = None
    taken: Optional[float] = None
    granted: Optional[float] = None
    lapsed: Optional[float] = None
    encashed: Optional[float] = None
    correction: Optional[float] = None
    closing: Optional[float] = None
    period: Optional[str] = None

    class Config:
        orm_mode = True


class TimeRegisterResponse(BaseModel):
    id: Optional[int] = None
    employee: Optional[str] = None
    shift_hrs: Optional[str] = None
    early_in: Optional[str] = None
    late_in: Optional[str] = None
    in_hrs: Optional[str] = None
    lunch: Optional[str] = None
    out_hrs: Optional[str] = None
    early_out: Optional[str] = None
    late_out: Optional[str] = None
    paid_hrs: Optional[str] = None
    business_unit: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None
    cost_center: Optional[str] = None
    salary_component: Optional[str] = None

    class Config:
        orm_mode = True


class StrikeRegisterResponse(BaseModel):
    id: Optional[int] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    deduction: Optional[str] = None
    date: Optional[date] = None
    shift: Optional[str] = None
    strike: Optional[str] = None
    strike_count: Optional[int] = None
    base_amount: Optional[float] = None
    deduction_type: Optional[str] = None
    deduction_amount: Optional[float] = None

    class Config:
        orm_mode = True


class TravelRegisterResponse(BaseModel):
    id: Optional[int] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    department: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    salary_component: Optional[str] = None
    employee_id: Optional[str] = None
    employee_name: Optional[str] = None
    distance: Optional[float] = None
    exclude_zero_distance: Optional[bool] = None

    class Config:
        orm_mode = True


class TimePunchResponse(BaseModel):
    id: Optional[int] = None
    business_unit: Optional[str] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    department: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    employee_name: Optional[str] = None
    punch_in_time: Optional[datetime] = None
    punch_out_time: Optional[datetime] = None
    total_hours: Optional[float] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True


class RemotePunchResponse(BaseModel):
    id: Optional[int] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    department: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    employee_name: Optional[str] = None
    datetime: Optional[datetime] = None
    location_coordinates: Optional[str] = None
    hide_empty_records: Optional[bool] = None

    class Config:
        orm_mode = True


class ManualUpdateResponse(BaseModel):
    id: Optional[int] = None
    business_unit: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None
    cost_center: Optional[str] = None
    salary_component: Optional[str] = None
    show_details: Optional[bool] = None
    month: Optional[str] = None
    employee_name: Optional[str] = None
    remarks: Optional[str] = None

    class Config:
        orm_mode = True


# ---------------------------
# Statutory / Tax / Returns
# ---------------------------
class ESIDeductionResponse(BaseModel):
    id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    esi_number: Optional[str] = None
    gross_salary: Optional[float] = None
    esi_amount: Optional[float] = None
    month: Optional[str] = None
    year: Optional[int] = None
    location: Optional[str] = None

    class Config:
        orm_mode = True


class ESICoverageResponse(BaseModel):
    id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    esi_number: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    coverage_start: Optional[date] = None
    coverage_end: Optional[date] = None
    location: Optional[str] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True


class PFDeductionResponse(BaseModel):
    id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    uan_number: Optional[str] = None
    pf_number: Optional[str] = None
    basic_salary: Optional[float] = None
    pf_amount: Optional[float] = None
    month: Optional[str] = None
    year: Optional[int] = None
    location: Optional[str] = None

    class Config:
        orm_mode = True


class PFCoverageResponse(BaseModel):
    id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    uan_number: Optional[str] = None
    pf_number: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    coverage_start: Optional[date] = None
    coverage_end: Optional[date] = None
    status: Optional[str] = None
    location: Optional[str] = None

    class Config:
        orm_mode = True


class OvertimeRegisterResponse(BaseModel):
    id: Optional[int] = None
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    date: Optional[date] = None
    shift: Optional[str] = None
    ot_hours: Optional[float] = None
    rate_per_hour: Optional[float] = None
    ot_amount: Optional[float] = None
    remarks: Optional[str] = None

    class Config:
        orm_mode = True


class RegisterOfLeavesResponse(BaseModel):
    id: Optional[int] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    year: Optional[int] = None
    month_to: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class IncomeTaxDeclarationResponse(BaseModel):
    id: Optional[int] = None
    employee_name: Optional[str] = None
    pan_no: Optional[str] = None
    last_updated: Optional[datetime] = None
    chapter_via: Optional[str] = None
    rent_paid: Optional[float] = None
    tax_regime: Optional[str] = None
    location: Optional[str] = None
    financial_year: Optional[str] = None
    is_active_employee: Optional[bool] = None
    exclude_no_declaration: Optional[bool] = None

    class Config:
        orm_mode = True


class IncomeTaxComputationResponse(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    request_on: Optional[datetime] = None
    location: Optional[str] = None
    department: Optional[str] = None
    cost_center: Optional[str] = None
    employee_count: Optional[int] = None
    month_year: Optional[str] = None
    download_status: Optional[str] = None

    class Config:
        orm_mode = True


class LabourWelfareFundResponse(BaseModel):
    id: Optional[int] = None
    employee_code: Optional[str] = None
    employee_name: Optional[str] = None
    location: Optional[str] = None
    state: Optional[str] = None
    salary: Optional[float] = None
    deduction: Optional[float] = None
    contribution: Optional[float] = None
    month: Optional[str] = None
    cost_center: Optional[str] = None
    department: Optional[str] = None

    class Config:
        orm_mode = True


class TDSReturnResponse(BaseModel):
    id: Optional[int] = None
    return_period_year: Optional[int] = None
    return_period_quarter: Optional[str] = None
    regular_24q_prev_period: Optional[str] = None
    token_no: Optional[str] = None
    change_in_employer_address: Optional[str] = None
    change_in_responsible_person_address: Optional[str] = None

    class Config:
        orm_mode = True


class ChallanDetailsResponse(BaseModel):
    id: Optional[int] = None
    tds_return_id: Optional[int] = None
    selected_period: Optional[str] = None
    nil_tax_return: Optional[bool] = None
    deposit_by_book_entry: Optional[str] = None
    challan_serial_no: Optional[str] = None
    minor_head: Optional[str] = None
    branch_code: Optional[str] = None
    challan_date: Optional[date] = None
    payment_date: Optional[date] = None
    deduction_date: Optional[date] = None
    income_tax: Optional[float] = None
    cess: Optional[float] = None
    interest: Optional[float] = None
    others: Optional[float] = None
    fee: Optional[float] = None

    class Config:
        orm_mode = True


class Form16Response(BaseModel):
    id: Optional[int] = None
    financial_year: Optional[str] = None
    date_of_issue: Optional[date] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    department: Optional[str] = None
    employee_id: Optional[int] = None

    class Config:
        orm_mode = True


# ---------------------------
# Annual reports
# ---------------------------
class AnnualSalarySummaryResponse(BaseModel):
    id: Optional[int] = None
    period: Optional[str] = None
    employees: Optional[int] = None
    earned_salary: Optional[float] = None
    deductions: Optional[float] = None
    net_salary: Optional[float] = None
    paid_days: Optional[int] = None
    unpaid_days: Optional[int] = None
    location: Optional[str] = None
    department: Optional[str] = None
    cost_center: Optional[str] = None

    class Config:
        orm_mode = True


class AnnualSalaryStatementResponse(BaseModel):
    id: Optional[int] = None
    employee_id: Optional[int] = None
    period: Optional[str] = None
    basic_salary: Optional[float] = None
    house_rent_allowance: Optional[float] = None
    medical_allowance: Optional[float] = None
    special_allowance: Optional[float] = None
    conveyance_allowance: Optional[float] = None
    telephone_allowance: Optional[float] = None
    total_earnings: Optional[float] = None
    group_insurance: Optional[float] = None
    gratuity: Optional[float] = None
    pf_deduction: Optional[float] = None
    professional_tax: Optional[float] = None
    total_deductions: Optional[float] = None
    net_earnings: Optional[float] = None

    class Config:
        orm_mode = True


# ---------------------------
# Other / Activity logs
# ---------------------------
class ActivityLogResponse(BaseModel):
    id: Optional[int] = None
    user_name: Optional[str] = None
    action: Optional[str] = None
    description: Optional[str] = None
    timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True
