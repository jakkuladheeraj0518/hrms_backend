from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class EmployeeBase(BaseModel):
    employee_id: str
    name: str
    email: Optional[str] = None
    department: Optional[str] = None
    location_id: Optional[int] = None
    department_id: Optional[int] = None
    cost_center_id: Optional[int] = None
    daily_salary: Optional[float] = None
    joining_date: Optional[date] = None
    exit_date: Optional[date] = None
    is_active: Optional[bool] = True

class EmployeeCreate(EmployeeBase): pass
class EmployeeResponse(EmployeeBase):
    id: int
    class Config: orm_mode = True

class PayrollPeriodCreate(BaseModel):
    name: str
    start_date: date
    end_date: date
    days: int

class PayrollPeriodUpdate(BaseModel):
    name: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    days: Optional[int]
    status: Optional[str]

class PayrollPeriodResponse(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    days: int
    status: str
    is_reporting_enabled: bool
    class Config: orm_mode = True

class RecalculationRequest(BaseModel):
    date_from: date
    date_to: date
    all_employees: bool
    employee_id: Optional[int]

class RecalculationResponse(BaseModel):
    id: int
    status: str
    progress: int
    message: str
    records_processed: int
    records_updated: int

class RecalculationStatusResponse(BaseModel):
    id: int
    date_from: date
    date_to: date
    employee_id: Optional[int]
    all_employees: bool
    status: str
    progress: int
    records_processed: int
    records_updated: int
    started_at: datetime
    class Config: orm_mode = True

class AttendanceRecordResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    emp_id: str
    date: date
    check_in: Optional[str]
    check_out: Optional[str]
    hours_worked: float
    status: str
    is_manual: bool

class AttendanceDetailResponse(BaseModel):
    total_records: int
    records_updated: int
    employees_count: int
    attendance_data: List[AttendanceRecordResponse]

class AttendancePostRequest(BaseModel):
    employee_id: int
    date: date
    check_in: Optional[str]
    check_out: Optional[str]

class LocationSchema(BaseModel):
    id: Optional[int]
    name: str
    class Config: orm_mode = True

class DepartmentSchema(BaseModel):
    id: Optional[int]
    name: str
    class Config: orm_mode = True

class CostCenterSchema(BaseModel):
    id: Optional[int]
    name: str
    class Config: orm_mode = True

class EmployeeSchema(BaseModel):
    id: Optional[int]
    employee_id: str
    name: str
    location_id: Optional[int]
    department_id: Optional[int]
    cost_center_id: Optional[int]
    daily_salary: float
    class Config: orm_mode = True

class LeaveTypeSchema(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]
    class Config: orm_mode = True

class LeaveBalanceSchema(BaseModel):
    id: Optional[int]
    employee_id: int
    leave_type_id: int
    balance_days: float
    balance_as_on: date
    class Config: orm_mode = True

class LeaveEncashmentSchema(BaseModel):
    id: Optional[int]
    employee_id: int
    leave_type_id: int
    payment_period: date
    leave_balance: float
    daily_salary: float
    encashment_days: float
    encashment_amount: float
    processed: bool
    class Config: orm_mode = True

class GenerateEncashmentRequest(BaseModel):
    leave_type_id: int
    balance_as_on: date
    balance_above: float
    payment_period: date
    location_ids: Optional[List[int]] = []
    department_ids: Optional[List[int]] = []
    cost_center_ids: Optional[List[int]] = []

class BonusComponents(BaseModel):
    basic: Optional[bool] = False
    hra: Optional[bool] = False
    sa: Optional[bool] = False
    mda: Optional[bool] = False
    conveyance: Optional[bool] = False
    telephone: Optional[bool] = False

class BonusConfigurationBase(BaseModel):
    bonus_rate: float = 8.33
    eligibility_cutoff: float = 21000
    min_wages: float = 7000
    min_bonus: float = 100
    max_bonus: float = 0

class BonusGenerateRequest(BaseModel):
    payment_period: str
    location_id: Optional[int] = None
    department_id: Optional[int] = None
    cost_center_id: Optional[int] = None
    employee_search: Optional[str] = ""
    basic_salary: Optional[float] = None
    components: BonusComponents
    bonus_config: BonusConfigurationBase

class BonusRecordResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    payment_period: str
    base_salary: float
    bonus_amount: float
    status: str
    class Config: orm_mode = True

class BonusSummaryResponse(BaseModel):
    eligible_employees: int
    total_payable: float
    records: List[BonusRecordResponse]

class BonusProcessResponse(BaseModel):
    message: str
    processed_count: int
    total_amount: float
    status: str

class SalaryComponentBase(BaseModel):
    employee_id: int
    basic_salary: Optional[float] = 0
    hra: Optional[float] = 0
    special_allowance: Optional[float] = 0
    medical_allowance: Optional[float] = 0
    conveyance_allowance: Optional[float] = 0
    telephone_allowance: Optional[float] = 0
    effective_from: date
    is_current: Optional[bool] = True

class SalaryComponentCreate(SalaryComponentBase): pass
class SalaryComponentResponse(SalaryComponentBase):
    id: int
    class Config: orm_mode = True

class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    email: str
    department_id: Optional[int] = None
    daily_salary: float
    joining_date: date
    exit_date: Optional[date]
    location_id: Optional[int]
    cost_center_id: Optional[int]
    is_active: Optional[bool] = True

class EmployeeResponse(EmployeeCreate):
    id: int
    class Config: orm_mode = True

class GratuityCalculationRequest(BaseModel):
    month: str
    payable_days: int
    month_days: int
    min_years: float
    exit_only: bool
    year_rounding: str
    location: str
    department: str
    salary_components: List[str]

class GratuityRecordResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: Optional[str]
    base_salary: float
    years_in_service: float
    gratuity_amount: float
    status: str
    month: str
    year: int
    is_processed: bool
    class Config: orm_mode = True

class GratuitySummaryResponse(BaseModel):
    eligible_employees: int
    total_payable: float
    records: List[GratuityRecordResponse]

class GratuityConfigurationResponse(BaseModel):
    id: int
    min_years: float
    payable_days: int
    month_days: int
    exit_only: bool
    year_rounding: str
    salary_components: str
    updated_at: datetime
    class Config: orm_mode = True

class HoldSalaryBase(BaseModel):
    employee_id: int
    hold_from: date
    hold_reason: str

class HoldSalaryCreate(HoldSalaryBase): pass
class HoldSalaryOut(BaseModel):
    id: int
    employee_name: str
    hold_from: date
    hold_reason: str
    class Config: orm_mode = True

class PayrollRunCreate(BaseModel):
    period: str
    total_net_payroll: float

class PayrollRunResponse(BaseModel):
    id: int
    period: str
    run_date: datetime
    runtime: str
    result: str
    total_net_payroll: float
    status: str
    class Config: orm_mode = True

class PayrollChartResponse(BaseModel):
    labels: List[str]
    values: List[float]
