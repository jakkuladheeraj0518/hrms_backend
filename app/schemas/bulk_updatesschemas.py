from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field

# ============================================================
# MASTER SCHEMAS (renamed to Bulk masters)
# ============================================================

class BulkMasterBase(BaseModel):
    id: Optional[int]
    name: str
    is_default: Optional[bool] = False

class BulkMasterRead(BulkMasterBase):
    id: int

# ============================================================
# EMPLOYEE SCHEMAS
# ============================================================

class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None
    date_of_joining: Optional[date] = None
    position: Optional[str] = None
    notes: Optional[str] = None

    business_unit_name: Optional[str] = None
    location_name: Optional[str] = None
    department_name: Optional[str] = None
    designation_name: Optional[str] = None
    cost_center_name: Optional[str] = None
    shift_policy_name: Optional[str] = None
    week_off_policy_name: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: int

    class Config:
        orm_mode = True


class UploadResponse(BaseModel):
    parsed_count: int
    parsed_preview: List[EmployeeBase]
    masters_found: Dict[str, Any]


# ============================================================
# EMPLOYEE OPTIONS (bulk update)
# ============================================================

class Selections(BaseModel):
    businessUnits: Optional[Dict[str, bool]] = {}
    bulkLocations: Optional[Dict[str, bool]] = {}
    bulkCostCenters: Optional[Dict[str, bool]] = {}
    bulkDepartments: Optional[Dict[str, bool]] = {}
    bulkDesignations: Optional[Dict[str, bool]] = {}


class SalarySettings(BaseModel):
    doNotCalculateOvertime: Optional[bool] = False
    doNotDeductESI: Optional[bool] = False
    deductESIAboveCeiling: Optional[bool] = False
    doNotDeductPF: Optional[bool] = False
    doNotDeductPensionPF: Optional[bool] = False
    deductPFAboveCeilingEmployee: Optional[bool] = False
    deductPFAboveCeilingEmployer: Optional[bool] = False
    deductPFOnGrossSalary: Optional[bool] = False
    deductPFExtraContribution: Optional[bool] = False
    doNotDeductProfessionalTax: Optional[bool] = False
    professionalTaxState: Optional[str] = None
    doNotDeductIncomeTaxTDS: Optional[bool] = False
    doNotDeductLWF: Optional[bool] = False
    lwfState: Optional[str] = None


class AttendanceSettings(BaseModel):
    enableSelfiePunch: Optional[bool] = False
    enableRemotePunch: Optional[bool] = False
    enableMissedPunch: Optional[bool] = False
    missedPunchLimit: Optional[int] = None
    enableWebChatPunch: Optional[bool] = False
    enableTimeRelaxation: Optional[bool] = False
    scanAtAllLocations: Optional[bool] = False
    ignoreTimeStrikes: Optional[bool] = False
    leavePolicies: Optional[bool] = False


class TravelSettings(BaseModel):
    enableTravelPunch: Optional[bool] = False
    travelPunchRequiresApproval: Optional[bool] = False
    travelPunchAttendance: Optional[bool] = False
    enableLiveTravel: Optional[bool] = False
    enableAutoShiftSelection: Optional[bool] = False


class CommunitySettings(BaseModel):
    makeCommunityAdmin: Optional[bool] = False
    allowPosting: Optional[bool] = False
    allowCommenting: Optional[bool] = False


class WorkmanSettings(BaseModel):
    pinNeverExpires: Optional[bool] = False
    allowMultiDeviceLogins: Optional[bool] = False


class BulkUpdateRequest(BaseModel):
    selections: Selections
    salarySettings: SalarySettings
    attendanceSettings: AttendanceSettings
    travelSettings: TravelSettings
    communitySettings: CommunitySettings
    workmanSettings: WorkmanSettings
    applyToSelectedEmployees: Optional[bool] = True


class EmployeePreview(BaseModel):
    id: int
    employee_code: str
    first_name: str
    last_name: Optional[str]
    email: Optional[str]
    mobile: Optional[str]


class BulkUpdateResponse(BaseModel):
    matched_count: int
    updated_count: int
    preview: List[EmployeePreview]


# ============================================================
# EMPLOYEE ADDRESS
# ============================================================

class EmployeeAddressBase(BaseModel):
    employee_id: int
    address_line1: str
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    address_type: Optional[str] = "Permanent"


class EmployeeAddressCreate(EmployeeAddressBase):
    pass


class EmployeeAddressRead(EmployeeAddressBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


# ============================================================
# BIOMETRIC CODES
# ============================================================

class EmployeeBiometricBase(BaseModel):
    employee_id: int
    employee_code: str
    name: str
    location: Optional[str] = None
    department: Optional[str] = None
    cost_center: Optional[str] = None
    business_unit: Optional[str] = None
    biometric_code: Optional[str] = None


class EmployeeBiometricCreate(EmployeeBiometricBase):
    pass


class EmployeeBiometricUpdate(BaseModel):
    location: Optional[str] = None
    department: Optional[str] = None
    cost_center: Optional[str] = None
    business_unit: Optional[str] = None
    biometric_code: Optional[str] = None


class EmployeeBiometricBulkUpdate(BaseModel):
    employee_ids: List[int]
    location: Optional[str] = None
    department: Optional[str] = None
    cost_center: Optional[str] = None
    business_unit: Optional[str] = None
    biometric_code: Optional[str] = None


class EmployeeBiometricOut(EmployeeBiometricBase):
    id: int

    class Config:
        orm_mode = True


# ============================================================
# BANK DETAILS
# ============================================================

class EmployeeBankBase(BaseModel):
    employee_id: int
    bank_name: Optional[str] = None
    ifsc_code: Optional[str] = None
    account_no: Optional[str] = None


class EmployeeBankCreate(EmployeeBankBase):
    verified: Optional[bool] = False


class EmployeeBankResponse(EmployeeBankBase):
    id: Optional[int]
    verified: Optional[bool] = False
    employee_name: str
    employee_code: str
    department: Optional[str] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None

    class Config:
        orm_mode = True


class EmployeeBankUpdate(BaseModel):
    bank_name: Optional[str] = None
    ifsc_code: Optional[str] = None
    account_no: Optional[str] = None
    verified: Optional[bool] = None


# ============================================================
# SALARY REVISION
# ============================================================

class SalaryRevisionBase(BaseModel):
    basic: float = Field(..., ge=0)
    hra: float = Field(..., ge=0)
    sa: float = Field(..., ge=0)
    mda: float = Field(..., ge=0)
    ca: float = Field(..., ge=0)
    ta: float = Field(..., ge=0)
    effective_month: int = Field(..., ge=1, le=12)
    effective_year: int = Field(..., ge=2000)
    remarks: Optional[str] = None


class SalaryRevisionCreate(SalaryRevisionBase):
    employee_id: int


class EmployeeSimple(BaseModel):
    id: int
    employee_code: str
    first_name: str
    last_name: Optional[str] = None
    employee_name: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    business_unit: Optional[str] = None
    cost_center: Optional[str] = None

    class Config:
        orm_mode = True


class SalaryRevisionOut(SalaryRevisionBase):
    id: int
    employee_id: int
    employee: EmployeeSimple

    class Config:
        orm_mode = True


# ============================================================
# SALARY DEDUCTION
# ============================================================

class SalaryDeductionBase(BaseModel):
    gi: Optional[float] = 0
    gratuity: Optional[float] = 0


class SalaryDeductionCreate(SalaryDeductionBase):
    employee_id: int


class SalaryDeductionOut(SalaryDeductionBase):
    id: int
    employee_id: int
    last_updated: Optional[datetime]
    employee: EmployeeSimple

    class Config:
        orm_mode = True


# ============================================================
# WORK PROFILE
# ============================================================

class WorkProfileBase(BaseModel):
    employee_id: int
    location: Optional[str] = None
    cost_center: Optional[str] = None
    department: Optional[str] = None
    grade: Optional[str] = None
    designation: Optional[str] = None
    shift_policy: Optional[str] = None
    week_off_policy: Optional[str] = None
    business_unit: Optional[str] = None


class WorkProfileCreate(WorkProfileBase):
    pass


class WorkProfileUpdate(BaseModel):
    location: Optional[str] = None
    cost_center: Optional[str] = None
    department: Optional[str] = None
    grade: Optional[str] = None
    designation: Optional[str] = None
    shift_policy: Optional[str] = None
    week_off_policy: Optional[str] = None
    business_unit: Optional[str] = None


class EmployeeWorkProfileOut(BaseModel):
    id: int
    employee_id: int
    employee_code: str
    name: str
    location: Optional[str]
    department: Optional[str]
    cost_center: Optional[str]
    business_unit: Optional[str]
    designation: Optional[str]
    grade: Optional[str]
    employment_type: Optional[str]
    date_of_joining: Optional[date]

    class Config:
        orm_mode = True
