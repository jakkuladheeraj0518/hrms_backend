from pydantic import BaseModel
from typing import Optional
from datetime import date

class SalaryVariableBase(BaseModel):
    employee_name: str
    employee_code: str
    location: Optional[str] = ""
    department: Optional[str] = ""
    business_unit: Optional[str] = ""
    source_component: Optional[str] = ""
    target_component: Optional[str] = ""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    amount: Optional[float] = 0
    comments: Optional[str] = ""
    total: Optional[float] = 0
    month: str


class SalaryVariableCreate(SalaryVariableBase):
    pass

class SalaryVariable(SalaryVariableBase):
    id: int
    class Config:
        from_attributes = True

class DeductionVariableBase(SalaryVariableBase):
    pass

class DeductionVariableCreate(DeductionVariableBase):
    pass

class DeductionVariable(DeductionVariableBase):
    id: int
    class Config:
        from_attributes = True

class TDSChallanBase(BaseModel):
    month: str
    bsrcode: Optional[str] = ""
    date: Optional[date] = None
    challan: Optional[str] = ""

class TDSChallanCreate(TDSChallanBase):
    pass

class TDSChallan(TDSChallanBase):
    id: int
    class Config:
        from_attributes = True

class DeductionTDSBase(BaseModel):
    name: str
    position: Optional[str] = ""
    grosssalary: float = 0
    calculatedexemptions: float = 0
    additionalexemptions: float = 0
    netsalary: float = 0
    code: Optional[str] = ""
    month: str
    created_date: Optional[date] = None

class DeductionTDSCreate(DeductionTDSBase):
    pass

class DeductionTDS(DeductionTDSBase):
    id: int
    class Config:
        from_attributes = True

class IncomeTaxTDSBase(BaseModel):
    employee_id: str
    employee_name: str
    designation: Optional[str] = ""
    status: Optional[str] = "Enabled"
    tds_amount: float = 0
    month: str
    created_date: Optional[date] = None

class IncomeTaxTDSCreate(IncomeTaxTDSBase):
    pass

class IncomeTaxTDS(IncomeTaxTDSBase):
    id: int
    class Config:
        from_attributes = True

class ExtraDaysBase(BaseModel):
    employee_name: str
    employee_code: str
    designation: Optional[str] = ""
    joining_date: Optional[date] = None
    extra_days: float = 0
    arrear: float = 0
    ot: float = 0
    comments: Optional[str] = ""
    month: str

class ExtraDaysCreate(ExtraDaysBase):
    pass

class ExtraDays(ExtraDaysBase):
    id: int
    class Config:
        from_attributes = True

class ExtraHoursBase(BaseModel):
    employee_name: str
    employee_code: str
    designation: Optional[str] = ""
    month: str
    hours_worked: float = 0
    comments: Optional[str] = ""

class ExtraHoursCreate(ExtraHoursBase):
    pass

class ExtraHours(ExtraHoursBase):
    id: int
    class Config:
        from_attributes = True

class LoanBase(BaseModel):
    employee: str
    loan_amount: float
    disbursement_date: date
    deduction_start: date
    installments: int
    interest_method: Optional[str] = "Interest Free"
    add_in_salary: Optional[bool] = False
    created_date: Optional[date] = None

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int
    class Config:
        from_attributes = True

class DataCaptureLoanBase(BaseModel):
    employee: str
    designation: Optional[str] = ""
    department: Optional[str] = ""
    loan_amount: float
    issue_date: date
    interest_method: Optional[str] = "Interest Free"

class DataCaptureLoanCreate(DataCaptureLoanBase):
    pass

class DataCaptureLoan(DataCaptureLoanBase):
    id: int
    class Config:
        from_attributes = True

class ITDeclarationBase(BaseModel):
    employee_name: str
    employee_code: str
    financial_year: str
    apply_new_tax_regime: Optional[bool] = False
    children_education_expenses: Optional[float] = 0.0
    employee_provident_fund: Optional[float] = 0.0
    housing_loan_principal_repayment: Optional[float] = 0.0
    insurance_premium: Optional[float] = 0.0
    mutual_funds: Optional[float] = 0.0
    national_savings_certificate: Optional[float] = 0.0
    others_80c: Optional[float] = 0.0
    public_provident_fund: Optional[float] = 0.0
    contribution_pension_funds_80ccc: Optional[float] = 0.0
    contribution_nps_80ccd1: Optional[float] = 0.0
    contribution_nps_80ccd1b: Optional[float] = 0.0
    employer_contribution_nps_80ccd2: Optional[float] = 0.0
    rajiv_gandhi_equity_savings_80ccg: Optional[float] = 0.0
    contributions_agriwaver_corpus_80ccn: Optional[float] = 0.0
    medical_insurance_self_non_senior: Optional[float] = 0.0
    medical_insurance_parents_non_senior: Optional[float] = 0.0
    income_previous_employer: Optional[float] = 0.0
    tds_previous_employer: Optional[float] = 0.0
    income_current_employer: Optional[float] = 0.0
    tds_current_employer: Optional[float] = 0.0
    income_other_sources: Optional[float] = 0.0
    income_house_property: Optional[float] = 0.0
    relief_u_s_89: Optional[float] = 0.0
    actual_rent_paid: Optional[float] = 0.0
    created_date: Optional[date] = None

class ITDeclarationCreate(ITDeclarationBase):
    pass

class ITDeclaration(ITDeclarationBase):
    id: int
    class Config:
        from_attributes = True

class TDSReturnBase(BaseModel):
    financial_year: str
    quarter: str
    receipt_number: Optional[str] = None
    created_date: Optional[date] = None

class TDSReturnCreate(TDSReturnBase):
    pass

class TDSReturn(TDSReturnBase):
    id: int
    class Config:
        from_attributes = True


