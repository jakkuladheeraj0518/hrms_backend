from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from app.database.base import Base

# ---------------- Salary Variable ----------------
class SalaryVariable(Base):
    __tablename__ = "salary_variables"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    employee_code = Column(String, nullable=False)
    location = Column(String)
    department = Column(String)
    business_unit = Column(String)
    source_component = Column(String)
    target_component = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    amount = Column(Float, default=0)
    comments = Column(String)
    total = Column(Float, default=0)
    month = Column(String, nullable=False)


class DeductionVariable(Base):
    __tablename__ = "deduction_variables"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    employee_code = Column(String, nullable=False)
    location = Column(String)
    department = Column(String)
    business_unit = Column(String)
    source_component = Column(String)
    target_component = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    amount = Column(Float, default=0)
    comments = Column(String)
    total = Column(Float, default=0)
    month = Column(String, nullable=False)


class TDSChallan(Base):
    __tablename__ = "tds_challans"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, nullable=False)
    bsrcode = Column(String)
    date = Column(Date)
    challan = Column(String)


class DeductionTDS(Base):
    __tablename__ = "deduction_tds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    position = Column(String)
    grosssalary = Column(Float, default=0)
    calculatedexemptions = Column(Float, default=0)
    additionalexemptions = Column(Float, default=0)
    netsalary = Column(Float, default=0)
    code = Column(String)
    month = Column(String)
    created_date = Column(Date)


class IncomeTaxTDS(Base):
    __tablename__ = "income_tax_tds"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, nullable=False)
    employee_name = Column(String, nullable=False)
    designation = Column(String)
    status = Column(String, default="Enabled")
    tds_amount = Column(Float, default=0)
    month = Column(String)
    created_date = Column(Date)


class ExtraDays(Base):
    __tablename__ = "extra_days"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    employee_code = Column(String, nullable=False)
    designation = Column(String)
    joining_date = Column(Date)
    extra_days = Column(Float, default=0)
    arrear = Column(Float, default=0)
    ot = Column(Float, default=0)
    comments = Column(String, default="")
    month = Column(String)


class ExtraHours(Base):
    __tablename__ = "extra_hours"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    employee_code = Column(String, nullable=False)
    designation = Column(String)
    month = Column(String, nullable=False)
    hours_worked = Column(Float, default=0)
    comments = Column(String, default="")


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    employee = Column(String, nullable=False)
    loan_amount = Column(Float, nullable=False)
    disbursement_date = Column(Date, nullable=False)
    deduction_start = Column(Date, nullable=False)
    installments = Column(Integer, nullable=False)
    interest_method = Column(String, default="Interest Free")
    add_in_salary = Column(Boolean, default=False)
    created_date = Column(Date)


class DataCaptureLoan(Base):
    __tablename__ = "data_capture_loans"

    id = Column(Integer, primary_key=True, index=True)
    employee = Column(String, nullable=False)
    designation = Column(String)
    department = Column(String)
    loan_amount = Column(Float, nullable=False)
    issue_date = Column(Date, nullable=False)
    interest_method = Column(String, default="Interest Free")
    remarks = Column(String, default="")
    created_date = Column(Date)


class ITDeclaration(Base):
    __tablename__ = "it_declarations"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    employee_code = Column(String, nullable=False)
    financial_year = Column(String, nullable=False)
    apply_new_tax_regime = Column(Boolean, default=False)

    children_education_expenses = Column(Float, default=0.0)
    employee_provident_fund = Column(Float, default=0.0)
    housing_loan_principal_repayment = Column(Float, default=0.0)
    insurance_premium = Column(Float, default=0.0)
    mutual_funds = Column(Float, default=0.0)
    national_savings_certificate = Column(Float, default=0.0)
    others_80c = Column(Float, default=0.0)
    public_provident_fund = Column(Float, default=0.0)
    contribution_pension_funds_80ccc = Column(Float, default=0.0)
    contribution_nps_80ccd1 = Column(Float, default=0.0)
    contribution_nps_80ccd1b = Column(Float, default=0.0)
    employer_contribution_nps_80ccd2 = Column(Float, default=0.0)
    rajiv_gandhi_equity_savings_80ccg = Column(Float, default=0.0)
    contributions_agriwaver_corpus_80ccn = Column(Float, default=0.0)
    medical_insurance_self_non_senior = Column(Float, default=0.0)
    medical_insurance_parents_non_senior = Column(Float, default=0.0)
    income_previous_employer = Column(Float, default=0.0)
    tds_previous_employer = Column(Float, default=0.0)
    income_current_employer = Column(Float, default=0.0)
    tds_current_employer = Column(Float, default=0.0)
    income_other_sources = Column(Float, default=0.0)
    income_house_property = Column(Float, default=0.0)
    relief_u_s_89 = Column(Float, default=0.0)
    actual_rent_paid = Column(Float, default=0.0)
    created_date = Column(Date)


class TDSReturn(Base):
    __tablename__ = "tds_returns"

    id = Column(Integer, primary_key=True, index=True)
    financial_year = Column(String, nullable=False)
    quarter = Column(String, nullable=False)
    receipt_number = Column(String, default="")
    created_date = Column(Date)
