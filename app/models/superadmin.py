from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Boolean,
    ForeignKey, Enum as SQLEnum, Text, func
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


# =========================
# ENUM DEFINITIONS
# =========================
class CompanyStatus(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class PlanType(str, enum.Enum):
    MONTHLY = "Monthly"
    YEARLY = "Yearly"


class PlanName(str, enum.Enum):
    BASIC = "Basic"
    ADVANCED = "Advanced"
    PREMIUM = "Premium"
    ENTERPRISE = "Enterprise"


class PaymentStatus(str, enum.Enum):
    PAID = "Paid"
    UNPAID = "Unpaid"
    PENDING = "Pending"


class PaymentMethod(str, enum.Enum):
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    PAYPAL = "Paypal"
    BANK_TRANSFER = "Bank Transfer"


class DomainStatus(str, enum.Enum):
    APPROVED = "Approved"
    PENDING = "Pending"
    REJECTED = "Rejected"


# =========================
# COMPANY MODEL
# =========================
class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    account_url = Column(String, unique=True)
    phone = Column(String)
    website = Column(String)
    password = Column(String, nullable=False)
    address = Column(Text)
    plan_name = Column(String)
    plan_type = Column(String)
    currency = Column(String, default="USD")
    language = Column(String, default="English")
    status = Column(String, default="Active")
    logo = Column(String)
    created_date = Column(Date, server_default=func.current_date())
    expiring_on = Column(Date)
    price = Column(Float, default=0.0)
    register_date = Column(Date, server_default=func.current_date())
    
    # Relationships
    domains = relationship("Domain", back_populates="company", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="company", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="company", cascade="all, delete-orphan")


# =========================
# DOMAIN MODEL
# =========================
class Domain(Base):
    __tablename__ = "domains"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    domain_url = Column(String, unique=True, nullable=False)
    plan_name = Column(String)
    plan_type = Column(String)
    status = Column(String, default="Pending")  # Approved, Pending, Rejected
    created_date = Column(Date, server_default=func.current_date())
    expiring_on = Column(Date)
    price = Column(Float, default=0.0)
    
    # Relationships
    company = relationship("Company", back_populates="domains")


# =========================
# PACKAGE MODEL
# =========================
class Package(Base):
    __tablename__ = "packages"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Basic, Advanced, Premium, Enterprise
    plan_type = Column(String, nullable=False)  # Monthly, Yearly
    price = Column(Float, nullable=False)
    position = Column(Integer)
    currency = Column(String, default="USD")
    discount_type = Column(String)  # Fixed, Percentage
    discount = Column(Float, default=0.0)
    max_invoices = Column(Integer)
    max_customers = Column(Integer)
    max_products = Column(Integer)
    max_suppliers = Column(Integer)
    trial_days = Column(Integer, default=0)
    is_recommended = Column(Boolean, default=False)
    access_trial = Column(Boolean, default=False)
    status = Column(String, default="Active")
    description = Column(Text)
    logo = Column(String)
    created_date = Column(Date, server_default=func.current_date())
    
    # Plan Modules (stored as comma-separated string or JSON)
    modules = Column(Text)  # Example: "invoices,customers,products"
    
    # Relationships
    subscriptions = relationship("Subscription", back_populates="package")


# =========================
# TRANSACTION MODEL
# =========================
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String, unique=True, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    amount = Column(Float, nullable=False)
    payment_method = Column(String)  # Credit Card, Debit Card, Paypal, Bank Transfer
    status = Column(String, default="Unpaid")  # Paid, Unpaid
    date = Column(Date, server_default=func.current_date())
    due_date = Column(Date)
    
    # Invoice Details
    plan = Column(String)
    billing_cycle = Column(String)
    subtotal = Column(Float)
    tax = Column(Float)
    total = Column(Float)
    
    # From/To Information
    from_name = Column(String)
    from_address = Column(Text)
    from_email = Column(String)
    to_name = Column(String)
    to_address = Column(Text)
    to_email = Column(String)
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="transactions")


# =========================
# SUBSCRIPTION MODEL
# =========================
class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    package_id = Column(Integer, ForeignKey("packages.id", ondelete="SET NULL"), nullable=True)
    
    plan_name = Column(String, nullable=False)
    plan_type = Column(String, nullable=False)
    billing_cycle = Column(String, nullable=False)  # 30 Days, 365 Days
    payment_method = Column(String)
    amount = Column(Float, nullable=False)
    status = Column(String, default="Paid")  # Paid, Unpaid, Expired
    
    created_date = Column(Date, server_default=func.current_date())
    expiring_on = Column(Date)
    
    # Relationships
    company = relationship("Company", back_populates="subscriptions")
    package = relationship("Package", back_populates="subscriptions")
