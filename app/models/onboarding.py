from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Float, JSON, Text, ForeignKey
from datetime import datetime
from app.database.base import Base
from sqlalchemy.orm import relationship


class Location(Base):
    __tablename__ = "location"
    id = Column("location_id", Integer, primary_key=True, index=True)
    # DB column is `location_name`; keep attribute name `location` for code/schemas
    location = Column("location_name", String, nullable=False, unique=True)


class Department(Base):
    __tablename__ = "department"
    id = Column("department_id", Integer, primary_key=True, index=True)
    # DB column is `department_name`; keep attribute name `department` for code/schemas
    department = Column("department_name", String, nullable=False, unique=True)


class CostCenter(Base):
    __tablename__ = "cost_center"
    id = Column("cost_center_id", Integer, primary_key=True, index=True)
    # DB column is `costcenter_name`; keep attribute name `costcenter` for code/schemas
    costcenter = Column("costcenter_name", String, nullable=False, unique=True)


class Grade(Base):
    __tablename__ = "grade"
    id = Column("grade_id", Integer, primary_key=True, index=True)
    # DB column is `grade_name`; keep attribute name `grade` for code/schemas
    grade = Column("grade_name", String, nullable=False, unique=True)


class Designation(Base):
    __tablename__ = "designation"
    id = Column("designation_id", Integer, primary_key=True, index=True)
    # DB column is `designation_name`; keep attribute name `designation` for code/schemas
    designation = Column("designation_name", String, nullable=False, unique=True)


class ShiftPolicy(Base):
    __tablename__ = "shift_policie"
    id = Column("shift_policy_id", Integer, primary_key=True, index=True)
    # DB column is `shift_policy_name`; keep attribute name `shift_policy` for code/schemas
    shift_policy = Column("shift_policy_name", String, nullable=False, unique=True)


class WeekOffPolicy(Base):
    __tablename__ = "week_off_policie"
    id = Column("week_off_policy_id", Integer, primary_key=True, index=True)
    # DB column is `week_off_policy_name`; keep attribute name `week_off_policy` for code/schemas
    week_off_policy = Column("week_off_policy_name", String, nullable=False, unique=True)


class OnboardingEmployee(Base):
    __tablename__ = "onboarding_employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column("firstName", String, nullable=False)
    middle_name = Column("middleName", String)
    last_name = Column("lastName", String)
    joining_date = Column("joiningDate", Date, nullable=False)
    confirmation_date = Column("confirmationDate", Date)
    dob = Column("dob", Date)
    gender = Column("gender", String)
    employee_code = Column("employeeCode", String, unique=True, nullable=False)
    biometric_code = Column("biometricCode", String)
    mobile = Column("mobile", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    send_mobile_login = Column("sendMobileLogin", Boolean, default=False)
    send_web_login = Column("sendWebLogin", Boolean, default=True)
    location = Column("location", String)
    cost_center = Column("costCenter", String)
    department = Column("department", String)
    grade = Column("grade", String)
    designation = Column("designation", String)
    shift_policy = Column("shiftPolicy", String)
    week_off_policy = Column("weekOffPolicy", String)
    # Add approved flag (was referenced in query but missing)
    approved = Column(Boolean, default=False)
 
    # relationships: Candidate.employee <-> OnboardingEmployee.candidates
    candidates = relationship("Candidate", back_populates="employee", cascade="all, delete-orphan")
    # OfferLetter.employee <-> OnboardingEmployee.offer_letters
    offer_letters = relationship("OfferLetter", back_populates="employee")


# Simple candidate info (Bulk Onboarding)
class BulkCandidate(Base):
    __tablename__ = "bulk_candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    status = Column(String, default="Form Sent")
    created_at = Column(DateTime, default=datetime.utcnow)

# Credit Transaction
class CreditTransaction(Base):
    __tablename__ = "credit_transactions"

    id = Column(Integer, primary_key=True, index=True)
    used_credits = Column(Integer, nullable=False)
    purpose = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

#form
class Candidate(Base):
    __tablename__ = "candidates"
    __table_args__ = {"extend_existing": True}

    # --- Core Fields ---
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)  # matches frontend `candidate?.phone`
    # link to an onboarding Employee record if this candidate becomes an employee
    employee_id = Column(Integer, ForeignKey("onboarding_employees.id"), nullable=True, index=True)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    # --- Candidate Details ---
    firstName = Column(String, nullable=True)  # optional, can split first/last if needed
    lastName = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    homePhone = Column(String, nullable=True)
    emergencyContact = Column(String, nullable=True)

    # --- Family Members ---
    fatherName = Column(String, nullable=True)
    fatherPhone = Column(String, nullable=True)
    fatherDOB = Column(Date, nullable=True)
    motherName = Column(String, nullable=True)
    motherPhone = Column(String, nullable=True)
    motherDOB = Column(Date, nullable=True)
    marital = Column(String, nullable=True)

    # --- Personal Info ---
    blood = Column(String, nullable=True)
    drivingLicense = Column(String, nullable=True)
    aadhaar = Column(String, nullable=True)
    pan = Column(String, nullable=True)
    uan = Column(String, nullable=True)
    esi = Column(String, nullable=True)

    # --- Addresses ---
    presentAddress = Column(String, nullable=True)
    permanentAddress = Column(String, nullable=True)

    # --- Bank Details ---
    bankName = Column(String, nullable=True)
    ifsc = Column(String, nullable=True)
    accountNumber = Column(String, nullable=True)
    accountName = Column(String, nullable=True)

     # Uploaded Documents
    aadhaarFile = Column(String, nullable=True)
    panFile = Column(String, nullable=True)

      # 🔗 Relationships
    employee = relationship("OnboardingEmployee", back_populates="candidates")
    offer_letters = relationship("OfferLetter", back_populates="candidate")

    # New form backend


class OnboardingForm(Base):
    __tablename__ = "onboarding_forms"

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String, nullable=False)
    candidate_email = Column(String, nullable=False)
    candidate_phone = Column(String, nullable=False)
    policies = Column(String, default="No policies attached")
    offer_letter = Column(String, default="Offer letter skipped")
    finalized = Column(Boolean, default=False)

#attachedoffer letter 

class OfferLetter(Base):
    __tablename__ = "offer_letters"

    id = Column(Integer, primary_key=True, index=True)
    # Link to candidate (form) and optionally the employee record
    candidate_id = Column(Integer, ForeignKey("candidates.id"), index=True)
    employee_id = Column(Integer, ForeignKey("onboarding_employees.id"), nullable=True, index=True)
    offer_template = Column(String)
    gross_salary = Column(Float)
    salary_breakup = Column(JSON)
    esi_options = Column(JSON)
    pf_options = Column(JSON)
    professional_tax = Column(JSON)
    income_tax = Column(JSON)
    lwf = Column(JSON)
    employee_profile = Column(JSON)
    joining_date = Column(String)
    confirmation_date = Column(String)
    dob = Column(String)
    notice_period = Column(Integer)
    gender = Column(String)

        # 🔗 Relationships
    candidate = relationship("Candidate", back_populates="offer_letters")
    employee = relationship("OnboardingEmployee", back_populates="offer_letters")

#finalize and send forms 
class FinalizedForm(Base):
    __tablename__ = "finalized_forms"

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String, nullable=False)
    candidate_email = Column(String, nullable=False)
    candidate_phone = Column(String, nullable=False)
    send_form = Column(Boolean, default=True)
    status = Column(String, default="saved")
    finalized_at = Column(DateTime, default=datetime.utcnow)

#onbarding form single /partb/table
class OnboardingCandidate(Base):
    __tablename__ = "onboarding_candidates"  # new table

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    mobile = Column(String, nullable=True)

    mobile_verification = Column(Boolean, default=True)
    pan_verification = Column(Boolean, default=False)
    bank_verification = Column(Boolean, default=False)
    aadhaar_verification = Column(Boolean, default=False)
    credit_balance = Column(Integer, default=0)

    # Part B - policies accepted
    policies_attached = Column(Boolean, default=False)
    form_status = Column(String, default="Pending")  # Pending / Approved / Rejected
    finalized_at = Column(DateTime, default=datetime.utcnow)


class OnboardingSetting(Base):
    __tablename__ = "onboarding_settings"

    id = Column(Integer, primary_key=True, index=True)
    # Use SQLAlchemy's generic JSON type so the model works with SQLite and Postgres.
    # Use a callable default (dict) to avoid sharing a mutable default between rows.
    fields = Column(JSON, default=dict)      # {"presentAddress": True, ...}
    documents = Column(JSON, default=dict)   # {"PAN Card": True, ...}

#offerletterform


class OfferLetterForm(Base):
    __tablename__ = "offer_letter_forms"

    id = Column(Integer, primary_key=True, index=True)

    # Template
    template_name = Column(String, default="")
    salary_structure = Column(String, default="")

    # Salary Breakup
    basic_salary = Column(Float, default=0)
    hra = Column(Float, default=0)
    special_allowance = Column(Float, default=0)
    medical_allowance = Column(Float, default=0)
    conveyance_allowance = Column(Float, default=0)
    telephone_allowance = Column(Float, default=0)
    gross_salary = Column(Float, default=0)
    total_salary = Column(Float, default=0)

    # Deductions
    group_insurance = Column(Float, default=0)
    gratuity = Column(Float, default=0)
    professional_tax_amount = Column(Float, default=0)
    esi_deduction = Column(Float, default=0)
    pf_deduction = Column(Float, default=0)
    net_salary = Column(Float, default=0)

    # Employer Contributions
    esi_contribution = Column(Float, default=0)
    pf_contribution = Column(Float, default=0)
    pension_contribution = Column(Float, default=0)
    edli_admin_charges = Column(Float, default=0)
    total_ctc = Column(Float, default=0)

    # Employee Profile
    location = Column(String, default="")
    cost_center = Column(String, default="")
    department = Column(String, default="")
    grade = Column(String, default="")
    designation = Column(String, default="")
    work_shift = Column(String, default="")
    joining_date = Column(Date, nullable=True)
    confirmation_date = Column(Date, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    notice_period = Column(Integer, default=0)
    gender = Column(String, default="")

    # ESI Options
    esi_do_not_deduct = Column(Boolean, default=False)
    esi_above_ceiling = Column(Boolean, default=False)

    # PF Options
    pf_do_not_deduct = Column(Boolean, default=False)
    pf_do_not_deduct_pension = Column(Boolean, default=False)
    pf_deduct_employee_ceiling = Column(Boolean, default=False)
    pf_deduct_employer_ceiling = Column(Boolean, default=False)
    pf_deduct_on_gross = Column(Boolean, default=False)
    pf_extra_contribution = Column(Boolean, default=False)
    pf_min_deduction = Column(Float, default=0)

    # Professional Tax Options
    professional_tax_do_not_deduct = Column(Boolean, default=False)
    professional_tax_state = Column(String, default="")

    # Income Tax Options
    income_tax_do_not_deduct = Column(Boolean, default=False)
    income_tax_metro_city = Column(Boolean, default=False)

    # Labour Welfare Fund Options
    lwf_do_not_deduct = Column(Boolean, default=False)
    lwf_state = Column(String, default="")
#offerletter
class OfferLetterTemplate(Base):
    __tablename__ = "offer_letter_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    content = Column(String, nullable=False)


# Backwards-compatible alias: some modules import `Employees` from this module.
# We renamed the onboarding-specific class to `OnboardingEmployee` to avoid
# colliding with other app-level Employee models. Export the old name so
# existing imports keep working without changing other files.
Employees = OnboardingEmployee