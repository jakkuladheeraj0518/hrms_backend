from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from app.repositories.superadmin import (
    CompanyRepository, PackageRepository, SubscriptionRepository,
    TransactionRepository, DomainRepository
)
from app.schemas.superadmin import (
    CompanyCreate, CompanyUpdate, CompanyResponse,
    PackageCreate, PackageUpdate, PackageResponse,
    SubscriptionCreate, SubscriptionResponse,
    TransactionCreate, TransactionResponse,
    DomainCreate, DomainUpdate, DomainResponse,
    DashboardStats, CompanyStats, FilterParams
)
from app.utils.superadmin import hash_password, generate_invoice_id, calculate_expiry_date

class DashboardService:
    @staticmethod
    def get_dashboard_stats(db: Session) -> DashboardStats:
        """Get comprehensive dashboard statistics"""
        total_companies = CompanyRepository.get_count(db)
        active_companies = CompanyRepository.get_active_count(db)
        inactive_companies = CompanyRepository.get_inactive_count(db)
        total_subscribers = SubscriptionRepository.get_count(db)
        active_subscribers = SubscriptionRepository.get_active_count(db)
        expired_subscribers = SubscriptionRepository.get_expired_count(db)
        total_earnings = TransactionRepository.get_total_earnings(db)
        total_transactions = TransactionRepository.get_count(db)
        
        return DashboardStats(
            total_companies=total_companies,
            active_companies=active_companies,
            inactive_companies=inactive_companies,
            total_subscribers=total_subscribers,
            active_subscribers=active_subscribers,
            expired_subscribers=expired_subscribers,
            total_earnings=total_earnings,
            total_transactions=total_transactions
        )
    
    @staticmethod
    def get_company_stats(db: Session) -> CompanyStats:
        """Get company/package statistics"""
        total_plans = PackageRepository.get_count(db)
        active_plans = PackageRepository.get_count(db, {'status': 'Active'})
        inactive_plans = total_plans - active_plans
        
        return CompanyStats(
            total_plans=total_plans,
            active_plans=active_plans,
            inactive_plans=inactive_plans,
            plan_types=2  # Monthly and Yearly
        )

class CompanyService:
    @staticmethod
    def get_all_companies(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[FilterParams] = None
    ) -> List[CompanyResponse]:
        """Get all companies with optional filters"""
        filter_dict = filters.dict(exclude_none=True) if filters else None
        companies = CompanyRepository.get_all(db, skip, limit, filter_dict)
        return [CompanyResponse.from_orm(c) for c in companies]
    
    @staticmethod
    def get_company(db: Session, company_id: int) -> CompanyResponse:
        """Get company by ID"""
        company = CompanyRepository.get_by_id(db, company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )
        return CompanyResponse.from_orm(company)
    
    @staticmethod
    def create_company(db: Session, company: CompanyCreate) -> CompanyResponse:
        """Create new company"""
        # Check if email already exists
        existing = CompanyRepository.get_by_email(db, company.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        company_data = company.dict(exclude={'password'})
        company_data['password_hash'] = hash_password(company.password)
        
        # Calculate expiry date if plan is selected
        if company.plan_type:
            company_data['register_date'] = company_data.get('created_date')
            billing_cycle = "30 Days" if company.plan_type == "Monthly" else "365 Days"
            company_data['expiring_on'] = calculate_expiry_date(billing_cycle)
        
        db_company = CompanyRepository.create(db, company_data)
        return CompanyResponse.from_orm(db_company)
    
    @staticmethod
    def update_company(db: Session, company_id: int, company: CompanyUpdate) -> CompanyResponse:
        """Update company"""
        db_company = CompanyRepository.update(
            db, company_id, company.dict(exclude_unset=True)
        )
        if not db_company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )
        return CompanyResponse.from_orm(db_company)
    
    @staticmethod
    def delete_company(db: Session, company_id: int) -> Dict[str, str]:
        """Delete company"""
        if not CompanyRepository.delete(db, company_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )
        return {"message": "Company deleted successfully"}
    
    @staticmethod
    def search_companies(db: Session, search_term: str) -> List[CompanyResponse]:
        """Search companies by name or email"""
        companies = CompanyRepository.search(db, search_term)
        return [CompanyResponse.from_orm(c) for c in companies]

class PackageService:
    @staticmethod
    def get_all_packages(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[FilterParams] = None
    ) -> List[PackageResponse]:
        """Get all packages with optional filters"""
        filter_dict = filters.dict(exclude_none=True) if filters else None
        packages = PackageRepository.get_all(db, skip, limit, filter_dict)
        return [PackageResponse.from_orm(p) for p in packages]
    
    @staticmethod
    def get_package(db: Session, package_id: int) -> PackageResponse:
        """Get package by ID"""
        package = PackageRepository.get_by_id(db, package_id)
        if not package:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Package not found"
            )
        return PackageResponse.from_orm(package)
    
    @staticmethod
    def create_package(db: Session, package: PackageCreate) -> PackageResponse:
        """Create new package"""
        package_data = package.dict(exclude={'modules'})
        modules_data = [m.dict() for m in package.modules]
        
        db_package = PackageRepository.create(db, package_data, modules_data)
        return PackageResponse.from_orm(db_package)
    
    @staticmethod
    def update_package(db: Session, package_id: int, package: PackageUpdate) -> PackageResponse:
        """Update package"""
        db_package = PackageRepository.update(
            db, package_id, package.dict(exclude_unset=True)
        )
        if not db_package:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Package not found"
            )
        return PackageResponse.from_orm(db_package)
    
    @staticmethod
    def delete_package(db: Session, package_id: int) -> Dict[str, str]:
        """Delete package"""
        if not PackageRepository.delete(db, package_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Package not found"
            )
        return {"message": "Package deleted successfully"}

class SubscriptionService:
    @staticmethod
    def get_all_subscriptions(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[FilterParams] = None
    ) -> List[SubscriptionResponse]:
        """Get all subscriptions with optional filters"""
        filter_dict = filters.dict(exclude_none=True) if filters else None
        subscriptions = SubscriptionRepository.get_all(db, skip, limit, filter_dict)
        return [SubscriptionResponse.from_orm(s) for s in subscriptions]
    
    @staticmethod
    def get_subscription(db: Session, subscription_id: int) -> SubscriptionResponse:
        """Get subscription by ID"""
        subscription = SubscriptionRepository.get_by_id(db, subscription_id)
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found"
            )
        return SubscriptionResponse.from_orm(subscription)
    
    @staticmethod
    def create_subscription(db: Session, subscription: SubscriptionCreate) -> SubscriptionResponse:
        """Create new subscription"""
        subscription_data = subscription.dict()
        db_subscription = SubscriptionRepository.create(db, subscription_data)
        return SubscriptionResponse.from_orm(db_subscription)

class TransactionService:
    @staticmethod
    def get_all_transactions(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[FilterParams] = None
    ) -> List[TransactionResponse]:
        """Get all transactions with optional filters"""
        filter_dict = filters.dict(exclude_none=True) if filters else None
        transactions = TransactionRepository.get_all(db, skip, limit, filter_dict)
        return [TransactionResponse.from_orm(t) for t in transactions]
    
    @staticmethod
    def get_transaction(db: Session, transaction_id: int) -> TransactionResponse:
        """Get transaction by ID"""
        transaction = TransactionRepository.get_by_id(db, transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        return TransactionResponse.from_orm(transaction)
    
    @staticmethod
    def create_transaction(db: Session, transaction: TransactionCreate) -> TransactionResponse:
        """Create new transaction"""
        # Check if invoice ID already exists
        existing = TransactionRepository.get_by_invoice_id(db, transaction.invoice_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invoice ID already exists"
            )
        
        transaction_data = transaction.dict()
        db_transaction = TransactionRepository.create(db, transaction_data)
        return TransactionResponse.from_orm(db_transaction)
    
    @staticmethod
    def delete_transaction(db: Session, transaction_id: int) -> Dict[str, str]:
        """Delete transaction"""
        if not TransactionRepository.delete(db, transaction_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        return {"message": "Transaction deleted successfully"}

class DomainService:
    @staticmethod
    def get_all_domains(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[FilterParams] = None
    ) -> List[DomainResponse]:
        """Get all domains with optional filters"""
        filter_dict = filters.dict(exclude_none=True) if filters else None
        domains = DomainRepository.get_all(db, skip, limit, filter_dict)
        return [DomainResponse.from_orm(d) for d in domains]
    
    @staticmethod
    def get_domain(db: Session, domain_id: int) -> DomainResponse:
        """Get domain by ID"""
        domain = DomainRepository.get_by_id(db, domain_id)
        if not domain:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Domain not found"
            )
        return DomainResponse.from_orm(domain)
    
    @staticmethod
    def create_domain(db: Session, domain: DomainCreate) -> DomainResponse:
        """Create new domain"""
        # Check if domain URL already exists
        existing = DomainRepository.get_by_url(db, domain.domain_url)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Domain URL already exists"
            )
        
        domain_data = domain.dict()
        db_domain = DomainRepository.create(db, domain_data)
        return DomainResponse.from_orm(db_domain)
    
    @staticmethod
    def update_domain_status(
        db: Session,
        domain_id: int,
        domain_update: DomainUpdate
    ) -> DomainResponse:
        """Update domain status (Approve/Reject)"""
        db_domain = DomainRepository.update_status(db, domain_id, domain_update.status)
        if not db_domain:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Domain not found"
            )
        return DomainResponse.from_orm(db_domain)
    
    @staticmethod
    def delete_domain(db: Session, domain_id: int) -> Dict[str, str]:
        """Delete domain"""
        if not DomainRepository.delete(db, domain_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Domain not found"
            )
        return {"message": "Domain deleted successfully"}