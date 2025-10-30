from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime


# =========================================================
# DASHBOARD RESPONSE SCHEMAS
# =========================================================

class RevenueDataPoint(BaseModel):
    month: str
    income: float
    expenses: float


class PlanDistribution(BaseModel):
    name: str
    value: int
    percentage: float


class RecentTransaction(BaseModel):
    id: str
    company: str
    date: str
    amount: str
    plan: str
    logo: str


class RecentCompany(BaseModel):
    company: str
    plan: str
    users: str
    domain: str
    logo: str


class ExpiredPlan(BaseModel):
    company: str
    expired: str
    plan: str
    logo: str


class DashboardStatsResponse(BaseModel):
    total_companies: int
    active_companies: int
    total_subscribers: int
    total_earnings: float
    company_growth: float
    active_growth: float
    subscriber_growth: float
    earnings_growth: float


class DashboardResponse(BaseModel):
    stats: DashboardStatsResponse
    revenue_data: List[RevenueDataPoint]
    plan_distribution: List[PlanDistribution]
    recent_transactions: List[RecentTransaction]
    recently_registered: List[RecentCompany]
    expired_plans: List[ExpiredPlan]


# =========================================================
# PACKAGE MODULE SCHEMAS
# =========================================================

class PackageModuleBase(BaseModel):
    module_name: str
    description: Optional[str] = None
    status: Optional[str] = "Active"


class PackageModuleCreate(PackageModuleBase):
    package_id: int


class PackageModuleUpdate(PackageModuleBase):
    pass


class PackageModuleResponse(PackageModuleBase):
    id: int
    package_id: int
    created_date: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }


# =========================================================
# PACKAGE SCHEMAS
# =========================================================

class PackageBase(BaseModel):
    name: str
    plan_type: str
    price: float
    position: Optional[int] = None
    currency: Optional[str] = "USD"
    discount_type: Optional[str] = None
    discount: Optional[float] = 0.0
    max_invoices: Optional[int] = None
    max_customers: Optional[int] = None
    max_products: Optional[int] = None
    max_suppliers: Optional[int] = None
    trial_days: Optional[int] = 0
    is_recommended: Optional[bool] = False
    access_trial: Optional[bool] = False
    status: Optional[str] = "Active"
    description: Optional[str] = None
    logo: Optional[str] = None
    modules: Optional[str] = None


class PackageCreate(PackageBase):
    pass


class PackageUpdate(PackageBase):
    pass


class PackageResponse(PackageBase):
    id: int
    created_date: Optional[date]
    package_modules: Optional[List[PackageModuleResponse]] = []

    model_config = {
        "from_attributes": True
    }


# =========================================================
# COMPANY SCHEMAS
# =========================================================

class CompanyBase(BaseModel):
    name: str
    email: EmailStr
    account_url: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    plan_name: Optional[str] = None
    plan_type: Optional[str] = None
    currency: Optional[str] = "USD"
    language: Optional[str] = "English"
    status: Optional[str] = "Active"
    logo: Optional[str] = None


class CompanyCreate(CompanyBase):
    password: str
    expiring_on: Optional[date] = None
    price: Optional[float] = 0.0


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    plan_name: Optional[str] = None
    plan_type: Optional[str] = None
    status: Optional[str] = None
    logo: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int
    created_date: Optional[date]
    expiring_on: Optional[date]
    price: Optional[float]
    register_date: Optional[date]

    model_config = {
        "from_attributes": True
    }


# =========================================================
# DOMAIN SCHEMAS
# =========================================================

class DomainBase(BaseModel):
    domain_url: str
    plan_name: Optional[str] = None
    plan_type: Optional[str] = None
    status: Optional[str] = "Pending"
    expiring_on: Optional[date] = None
    price: Optional[float] = 0.0


class DomainCreate(DomainBase):
    company_id: int


class DomainUpdate(DomainBase):
    pass


class DomainResponse(DomainBase):
    id: int
    company_id: int
    created_date: Optional[date]

    model_config = {
        "from_attributes": True
    }


# =========================================================
# TRANSACTION SCHEMAS
# =========================================================

class TransactionBase(BaseModel):
    invoice_id: str
    amount: float
    payment_method: Optional[str] = None
    status: Optional[str] = "Unpaid"
    plan: Optional[str] = None
    billing_cycle: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    from_name: Optional[str] = None
    from_address: Optional[str] = None
    from_email: Optional[str] = None
    to_name: Optional[str] = None
    to_address: Optional[str] = None
    to_email: Optional[str] = None


class TransactionCreate(TransactionBase):
    company_id: int
    due_date: Optional[date] = None


class TransactionUpdate(TransactionBase):
    status: Optional[str] = None


class TransactionResponse(TransactionBase):
    id: int
    company_id: int
    date: Optional[date]
    due_date: Optional[date]
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }


# =========================================================
# SUBSCRIPTION SCHEMAS
# =========================================================

class SubscriptionBase(BaseModel):
    plan_name: str
    plan_type: str
    billing_cycle: str
    payment_method: Optional[str] = None
    amount: float
    status: Optional[str] = "Paid"
    expiring_on: Optional[date] = None


class SubscriptionCreate(SubscriptionBase):
    company_id: int
    package_id: Optional[int] = None


class SubscriptionUpdate(SubscriptionBase):
    status: Optional[str] = None


class SubscriptionResponse(SubscriptionBase):
    id: int
    company_id: int
    package_id: Optional[int]
    created_date: Optional[date]

    model_config = {
        "from_attributes": True
    }
