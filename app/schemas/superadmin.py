from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime

# Company Schemas
class CompanyBase(BaseModel):
    name: str
    email: EmailStr
    account_url: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    plan_name: Optional[str] = None
    plan_type: Optional[str] = None
    currency: str = "USD"
    language: str = "English"
    status: str = "Active"
    logo: Optional[str] = None

class CompanyCreate(CompanyBase):
    password: str

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    account_url: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    plan_name: Optional[str] = None
    plan_type: Optional[str] = None
    currency: Optional[str] = None
    language: Optional[str] = None
    status: Optional[str] = None
    logo: Optional[str] = None
    password: Optional[str] = None

class Company(CompanyBase):
    id: int
    created_date: date
    expiring_on: Optional[date] = None
    price: float
    register_date: date
    
    class Config:
        from_attributes = True

# Domain Schemas
class DomainBase(BaseModel):
    domain_url: str
    plan: Optional[str] = None
    plan_type: Optional[str] = None
    price: float = 0.0
    

class DomainCreate(DomainBase):
    company_id: int

class DomainUpdate(BaseModel):
    domain_url: Optional[str] = None
    plan: Optional[str] = None
    plan_type: Optional[str] = None
    status: Optional[str] = None
    price: Optional[float] = None
    expiring_on: Optional[date] = None

class Domain(DomainBase):
    id: int
    company_id: int
    status: str
    created_date: date
    expiring_on: Optional[date] = None
    
    class Config:
        from_attributes = True

# Package Schemas
class PackageBase(BaseModel):
    name: str
    type: str
    price: float
    position: Optional[int] = None
    currency: str = "USD"
    discount_type: Optional[str] = None
    discount: float = 0.0
    limitations_invoices: Optional[int] = None
    max_customers: Optional[int] = None
    product: Optional[int] = None
    supplier: Optional[int] = None
    trial_days: int = 0
    is_recommended: bool = False
    status: str = "Active"
    description: Optional[str] = None
    modules: Optional[str] = None
    logo: Optional[str] = None

class PackageCreate(PackageBase):
    pass

class PackageUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    price: Optional[float] = None
    position: Optional[int] = None
    currency: Optional[str] = None
    discount_type: Optional[str] = None
    discount: Optional[float] = None
    limitations_invoices: Optional[int] = None
    max_customers: Optional[int] = None
    product: Optional[int] = None
    supplier: Optional[int] = None
    trial_days: Optional[int] = None
    is_recommended: Optional[bool] = None
    status: Optional[str] = None
    description: Optional[str] = None
    modules: Optional[str] = None
    logo: Optional[str] = None

class Package(PackageBase):
    id: int
    created_date: date
    
    class Config:
        from_attributes = True

# Transaction Schemas
class TransactionBase(BaseModel):
    invoice_id: str
    company_id: int
    amount: float
    payment_method: Optional[str] = None
    status: str = "Unpaid"
    due_date: Optional[date] = None
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
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[date] = None

class Transaction(TransactionBase):
    id: int
    date: date
    created_at: datetime
    
    class Config:
        from_attributes = True

# Subscription Schemas
class SubscriptionBase(BaseModel):
    company_id: int
    package_id: Optional[int] = None
    plan: str
    billing_cycle: str
    payment_method: Optional[str] = None
    amount: float
    status: str = "Paid"
    expiring_on: Optional[date] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    package_id: Optional[int] = None
    plan: Optional[str] = None
    billing_cycle: Optional[str] = None
    payment_method: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    expiring_on: Optional[date] = None

class Subscription(SubscriptionBase):
    id: int
    created_date: date
    
    class Config:
        from_attributes = True

# Dashboard Schemas
class DashboardStatsResponse(BaseModel):
    total_companies: int
    active_companies: int
    total_subscribers: int
    total_earnings: float
    company_growth: float
    active_growth: float
    subscriber_growth: float
    earnings_growth: float

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

class DashboardResponse(BaseModel):
    stats: DashboardStatsResponse
    revenue_data: List[RevenueDataPoint]
    plan_distribution: List[PlanDistribution]
    recent_transactions: List[RecentTransaction]
    recently_registered: List[RecentCompany]
    expired_plans: List[ExpiredPlan]