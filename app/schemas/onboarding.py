from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import date, datetime


# Lookup Schemas for dropdowns
class LocationBase(BaseModel):
    location: str
    class Config:
        orm_mode = True

class DepartmentBase(BaseModel):
    department: str
    class Config:
        orm_mode = True

class CostCenterBase(BaseModel):
    costcenter: str
    class Config:
        orm_mode = True

class GradeBase(BaseModel):
    grade: str
    class Config:
        orm_mode = True

class DesignationBase(BaseModel):
    designation: str
    class Config:
        orm_mode = True

class ShiftPolicyBase(BaseModel):
    shift_policy: str
    class Config:
        orm_mode = True

class WeekOffPolicyBase(BaseModel):
    week_off_policy: str
    class Config:
        orm_mode = True

class EmployeeBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    joining_date: Optional[date] = None
    confirmation_date: Optional[date] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    employee_code: Optional[str] = None
    biometric_code: Optional[str] = None
    mobile: str
    email: EmailStr
    send_mobile_login: Optional[bool] = False
    send_web_login: Optional[bool] = True
    approved: Optional[bool] = False
    location_id: Optional[int] = None
    cost_center_id: Optional[int] = None
    department_id: Optional[int] = None
    grade_id: Optional[int] = None
    designation_id: Optional[int] = None
    shift_policy_id: Optional[int] = None
    week_off_policy_id: Optional[int] = None
    notes: Optional[str] = None
    position: Optional[str] = None
    daily_salary: Optional[float] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    employee_code: str
    email: str
    mobile: str
    joining_date: Optional[date]
    approved: bool

    class Config:
        orm_mode = True

# ---------------- Candidate Schemas ----------------form backend
class Document(BaseModel):
    type: str
    link: str

class CandidateBase(BaseModel):
    # Core Fields
    name: str
    email: str
    phone: str
    status: Optional[str] = "Pending"

    # Candidate Details
    firstName: Optional[str]
    lastName: Optional[str]
    dob: Optional[date]
    homePhone: Optional[str]
    emergencyContact: Optional[str]

    # Family Members
    fatherName: Optional[str]
    fatherPhone: Optional[str]
    fatherDOB: Optional[date]
    motherName: Optional[str]
    motherPhone: Optional[str]
    motherDOB: Optional[date]
    marital: Optional[str]

    # Personal Info
    blood: Optional[str]
    drivingLicense: Optional[str]
    aadhaar: Optional[str]
    pan: Optional[str]
    uan: Optional[str]
    esi: Optional[str]

    # Addresses
    presentAddress: Optional[str]
    permanentAddress: Optional[str]

    # Bank Details
    bankName: Optional[str]
    ifsc: Optional[str]
    accountNumber: Optional[str]
    accountName: Optional[str]

    # Documents
    aadhaarFile: Optional[str]
    panFile: Optional[str]
    created_at: datetime

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    status: Optional[str]

    firstName: Optional[str]
    lastName: Optional[str]
    dob: Optional[date]
    homePhone: Optional[str]
    emergencyContact: Optional[str]

    fatherName: Optional[str]
    fatherPhone: Optional[str]
    fatherDOB: Optional[date]
    motherName: Optional[str]
    motherPhone: Optional[str]
    motherDOB: Optional[date]
    marital: Optional[str]

    blood: Optional[str]
    drivingLicense: Optional[str]
    aadhaar: Optional[str]
    pan: Optional[str]
    uan: Optional[str]
    esi: Optional[str]

    presentAddress: Optional[str]
    permanentAddress: Optional[str]

    bankName: Optional[str]
    ifsc: Optional[str]
    accountNumber: Optional[str]
    accountName: Optional[str]
    aadhaarFile: Optional[str]
    panFile: Optional[str]
    created_at: datetime

class CandidateStatusUpdate(BaseModel):
    status: str

class CandidateResponse(CandidateBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True



# Bulk Onboarding Schemas
class BulkCandidateCreate(BaseModel):
    name: str
    email: EmailStr
    mobile: str

class VerificationOptions(BaseModel):
    mobile: bool = True
    pan: bool = True
    bank: bool = True
    aadhar: bool = True

class BulkOnboardingRequest(BaseModel):
    candidates: List[BulkCandidateCreate]
    verification_options: VerificationOptions
    credits: int

class BulkCandidateResponse(BulkCandidateCreate):
    id: int
    status: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional

class OnboardingFormCreate(BaseModel):
    candidate_name: str
    candidate_email: str
    candidate_phone: str
    policies: Optional[str] = None
    offer_letter: Optional[str] = None


class OnboardingFormUpdate(BaseModel):
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_phone: Optional[str] = None
    policies: Optional[str] = None
    offer_letter: Optional[str] = None


class OnboardingFormResponse(BaseModel):
    id: int
    candidate_name: str
    candidate_email: str
    candidate_phone: str
    policies: str
    offer_letter: str
    finalized: bool

    class Config:
        orm_mode = True

#attachoffer letter----


class OfferLetterBase(BaseModel):
    candidate_id: int
    offer_template: Optional[str]
    gross_salary: Optional[float]
    salary_breakup: Optional[Dict[str, float]]
    esi_options: Optional[Dict[str, bool]]
    pf_options: Optional[Dict[str, bool]]
    professional_tax: Optional[Dict[str, Any]]
    income_tax: Optional[Dict[str, bool]]
    lwf: Optional[Dict[str, Any]]
    employee_profile: Optional[Dict[str, str]]
    joining_date: Optional[str]
    confirmation_date: Optional[str]
    dob: Optional[str]
    notice_period: Optional[int]
    gender: Optional[str]


class OfferLetterCreate(OfferLetterBase):
    pass


class OfferLetterUpdate(OfferLetterBase):
    pass


class OfferLetterResponse(OfferLetterBase):
    id: int

    class Config:
        orm_mode = True

#finalize and send forms 
class FinalizeRequest(BaseModel):
    candidate_name: str
    candidate_email: str
    candidate_phone: str
    send_form: bool
#onbarding form single /partb/table

class OnboardingCandidateBase(BaseModel):
    candidate_name: str
    email: Optional[str]
    mobile: Optional[str]
    mobile_verification: bool = True
    pan_verification: bool = False
    bank_verification: bool = False
    aadhaar_verification: bool = False
    credit_balance: int = 0
    policies_attached: bool = False
    form_status: str = "Pending"

class OnboardingCandidateCreate(OnboardingCandidateBase):
    pass

class OnboardingCandidateUpdate(OnboardingCandidateBase):
    pass

class OnboardingCandidateResponse(OnboardingCandidateBase):
    id: int
    class Config:
        orm_mode = True
class ReviewFormSchema(BaseModel):
    candidate_name: str
    email: str | None
    mobile: str | None
    mobile_verification: bool
    pan_verification: bool
    bank_verification: bool
    aadhaar_verification: bool
    credit_balance: int
    policies_attached: bool
    form_status: str

    class Config:
        orm_mode = True

class OnboardingSettingsResponse(BaseModel):
    fields: Dict[str, bool]
    documents: Dict[str, bool]

class UpdateFieldRequest(BaseModel):
    field: str
    required: bool

class UpdateDocumentRequest(BaseModel):
    document: str
    required: bool


#offerletterform

class OfferLetterFormBase(BaseModel):
    # Template
    template_name: Optional[str] = ""
    salary_structure: Optional[str] = ""

    # Salary Breakup
    basic_salary: Optional[float] = 0
    hra: Optional[float] = 0
    special_allowance: Optional[float] = 0
    medical_allowance: Optional[float] = 0
    conveyance_allowance: Optional[float] = 0
    telephone_allowance: Optional[float] = 0
    gross_salary: Optional[float] = 0
    total_salary: Optional[float] = 0

    # Deductions
    group_insurance: Optional[float] = 0
    gratuity: Optional[float] = 0
    professional_tax_amount: Optional[float] = 0
    esi_deduction: Optional[float] = 0
    pf_deduction: Optional[float] = 0
    net_salary: Optional[float] = 0

    # Employer Contributions
    esi_contribution: Optional[float] = 0
    pf_contribution: Optional[float] = 0
    pension_contribution: Optional[float] = 0
    edli_admin_charges: Optional[float] = 0
    total_ctc: Optional[float] = 0

    # Employee Profile
    location: Optional[str] = ""
    cost_center: Optional[str] = ""
    department: Optional[str] = ""
    grade: Optional[str] = ""
    designation: Optional[str] = ""
    work_shift: Optional[str] = ""
    joining_date: Optional[date] = None
    confirmation_date: Optional[date] = None
    date_of_birth: Optional[date] = None
    notice_period: Optional[int] = 0
    gender: Optional[str] = ""

    # ESI Options
    esi_do_not_deduct: Optional[bool] = False
    esi_above_ceiling: Optional[bool] = False

    # PF Options
    pf_do_not_deduct: Optional[bool] = False
    pf_do_not_deduct_pension: Optional[bool] = False
    pf_deduct_employee_ceiling: Optional[bool] = False
    pf_deduct_employer_ceiling: Optional[bool] = False
    pf_deduct_on_gross: Optional[bool] = False
    pf_extra_contribution: Optional[bool] = False
    pf_min_deduction: Optional[float] = 0

    # Professional Tax Options
    professional_tax_do_not_deduct: Optional[bool] = False
    professional_tax_state: Optional[str] = ""

    # Income Tax Options
    income_tax_do_not_deduct: Optional[bool] = False
    income_tax_metro_city: Optional[bool] = False

    # Labour Welfare Fund Options
    lwf_do_not_deduct: Optional[bool] = False
    lwf_state: Optional[str] = ""


class OfferLetterFormCreate(OfferLetterFormBase):
    pass

class OfferLetterFormUpdate(OfferLetterFormBase):
    pass

class OfferLetterFormResponse(OfferLetterFormBase):
    id: int

    class Config:
        orm_mode = True

# Schema for reading templates
class Template(BaseModel):
    id: int
    name: str
    content: str

    class Config:
        orm_mode = True

# Schema for creating templates
class TemplateCreate(BaseModel):
    name: str
    content: str

# Generate letter input
class GenerateLetterRequest(BaseModel):
    template_id: int
    field_values: Dict[str, str]

# Response
class GenerateLetterResponse(BaseModel):
    generated_letter: str   