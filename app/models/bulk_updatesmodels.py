from sqlalchemy import (
    Column, Integer, String, Boolean, Date, ForeignKey,
    DateTime, UniqueConstraint, func, Text, Float
)
from sqlalchemy.orm import relationship
from app.database import Base


# -------------------- Core Master Models --------------------
class BusinessUnit(Base):
    __tablename__ = "business_units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False)
    employees = relationship("EmployeeBulkUpdates", back_populates="business_unit_rel")


class BulkLocation(Base):
    __tablename__ = "bulk_locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False)
    is_default = Column(Boolean, default=False)
    employees = relationship("EmployeeBulkUpdates", back_populates="location")


class BulkDepartment(Base):
    __tablename__ = "bulk_departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False)
    is_default = Column(Boolean, default=False)
    employees = relationship("EmployeeBulkUpdates", back_populates="department")


class BulkDesignation(Base):
    __tablename__ = "bulk_designations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False)
    is_default = Column(Boolean, default=False)
    employees = relationship("EmployeeBulkUpdates", back_populates="designation")


class BulkCostCenter(Base):
    __tablename__ = "bulk_cost_centers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False)
    is_default = Column(Boolean, default=False)
    employees = relationship("EmployeeBulkUpdates", back_populates="cost_center")


class BulkShiftPolicy(Base):
    __tablename__ = "bulk_shift_policies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False)
    is_default = Column(Boolean, default=False)
    employees = relationship("EmployeeBulkUpdates", back_populates="shift_policy")


class BulkWeekOffPolicy(Base):
    __tablename__ = "bulk_week_off_policies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=False)
    is_default = Column(Boolean, default=False)
    employees = relationship("EmployeeBulkUpdates", back_populates="week_off_policy")


# -------------------- Employee Core Model --------------------
class EmployeeBulkUpdates(Base):
    __tablename__ = "bulkemployee"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(64), unique=True, index=True, nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=True)
    employee_name = Column(String(256), nullable=True)
    business_unit = Column(String(128), nullable=True)
    email = Column(String(256), unique=True, nullable=True)
    position = Column(String(100), nullable=True)
    mobile = Column(String(32), nullable=True)
    date_of_joining = Column(Date, nullable=True)

    location_id = Column(Integer, ForeignKey("bulk_locations.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("bulk_departments.id"), nullable=True)
    designation_id = Column(Integer, ForeignKey("bulk_designations.id"), nullable=True)
    cost_center_id = Column(Integer, ForeignKey("bulk_cost_centers.id"), nullable=True)
    business_unit_id = Column(Integer, ForeignKey("business_units.id"), nullable=True)
    shift_policy_id = Column(Integer, ForeignKey("bulk_shift_policies.id"), nullable=True)
    week_off_policy_id = Column(Integer, ForeignKey("bulk_week_off_policies.id"), nullable=True)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    location = relationship("BulkLocation", back_populates="employees", lazy="joined")
    department = relationship("BulkDepartment", back_populates="employees", lazy="joined")
    designation = relationship("BulkDesignation", back_populates="employees", lazy="joined")
    cost_center = relationship("BulkCostCenter", back_populates="employees", lazy="joined")
    business_unit_rel = relationship("BusinessUnit", back_populates="employees", lazy="joined")

    shift_policy = relationship("BulkShiftPolicy", back_populates="employees", lazy="joined")
    week_off_policy = relationship("BulkWeekOffPolicy", back_populates="employees", lazy="joined")

    addresses = relationship("EmployeeBulkUpdatesAddress", back_populates="employee", cascade="all, delete-orphan")
    bank_details = relationship("EmployeeBulkUpdatesBank", back_populates="employee", uselist=False)
    biometric_record = relationship("EmployeeBulkUpdatesBiometric", back_populates="employee", uselist=False, cascade="all, delete-orphan")
    salary_revisions = relationship(
        "SalaryRevision",
        back_populates="employee",
        cascade="all, delete-orphan",
        order_by="SalaryRevision.effective_year.desc(), SalaryRevision.effective_month.desc()",
    )
    salary_deduction = relationship("SalaryDeduction", back_populates="employee", uselist=False)
    work_profile = relationship("WorkProfile", back_populates="employee", uselist=False)


# -------------------- Employee Options --------------------
class EmployeeBulkUpdatesOptions(Base):
    __tablename__ = "employee_options"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("bulkemployee.id"), unique=True, nullable=False)
    options = Column(Text, nullable=False)  # JSON dumped string

    employee = relationship("EmployeeBulkUpdates", lazy="joined")


# -------------------- Employee Address --------------------
class EmployeeBulkUpdatesAddress(Base):
    __tablename__ = "employee_addresses"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("bulkemployee.id", ondelete="CASCADE"), nullable=False)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    pincode = Column(String(10))
    address_type = Column(String(50), default="Permanent")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("employee_id", "address_type", name="uq_employee_address_type"),
    )

    employee = relationship("EmployeeBulkUpdates", back_populates="addresses")


# -------------------- Employee Biometric --------------------
class EmployeeBulkUpdatesBiometric(Base):
    __tablename__ = "employees_biometric_codes"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    cost_center = Column(String(128), nullable=True)
    business_unit = Column(String(128), nullable=True)
    biometric_code = Column(String(50), nullable=True)

    employee_id = Column(Integer, ForeignKey("bulkemployee.id"), unique=True, nullable=False)
    employee = relationship("EmployeeBulkUpdates", back_populates="biometric_record", lazy="joined")


# -------------------- Employee Bank --------------------
class EmployeeBulkUpdatesBank(Base):
    __tablename__ = "employee_bank_details"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("bulkemployee.id", ondelete="CASCADE"), unique=True, nullable=False)
    bank_name = Column(String(128), nullable=True)
    ifsc_code = Column(String(32), nullable=True)
    account_no = Column(String(32), nullable=True)
    verified = Column(Boolean, default=False)

    employee = relationship("EmployeeBulkUpdates", back_populates="bank_details")


# -------------------- Salary Revision --------------------
class SalaryRevision(Base):
    __tablename__ = "salary_revisions"
    __table_args__ = (
        UniqueConstraint("employee_id", "effective_month", "effective_year", name="uq_employee_effective"),
    )

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("bulkemployee.id", ondelete="CASCADE"), nullable=False)

    basic = Column(Integer, nullable=False, default=0)
    hra = Column(Integer, nullable=False, default=0)
    sa = Column(Integer, nullable=False, default=0)
    mda = Column(Integer, nullable=False, default=0)
    ca = Column(Integer, nullable=False, default=0)
    ta = Column(Integer, nullable=False, default=0)

    effective_month = Column(Integer, nullable=False)
    effective_year = Column(Integer, nullable=False)
    remarks = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    employee = relationship("EmployeeBulkUpdates", back_populates="salary_revisions", lazy="joined")


# -------------------- Salary Deduction --------------------
class SalaryDeduction(Base):
    __tablename__ = "salary_deductions"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("bulkemployee.id"), nullable=False)
    gi = Column(Float, default=0)
    gratuity = Column(Float, default=0)
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    employee = relationship("EmployeeBulkUpdates", back_populates="salary_deduction")


# -------------------- Work Profile --------------------
class WorkProfile(Base):
    __tablename__ = "work_profiles"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("bulkemployee.id"), nullable=False)

    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    location = Column(String(100))
    cost_center = Column(String(100))
    department = Column(String(100))
    grade = Column(String(50))
    designation = Column(String(100))
    shift_policy = Column(String(100))
    week_off_policy = Column(String(100))
    business_unit = Column(String(100), nullable=True)

    employee = relationship("EmployeeBulkUpdates", back_populates="work_profile")
    
