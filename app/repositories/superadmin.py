from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models.superadmin import (
    Company, Package, Subscription, Transaction, Domain,
    CompanyStatus, PaymentStatus, DomainStatus, PlanName, PlanType
)

class CompanyRepository:
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Company]:
        query = db.query(Company)
        
        if filters:
            if filters.get('status'):
                query = query.filter(Company.status == filters['status'])
            if filters.get('plan_name'):
                query = query.filter(Company.plan_name == filters['plan_name'])
            if filters.get('plan_type'):
                query = query.filter(Company.plan_type == filters['plan_type'])
            if filters.get('date_from'):
                query = query.filter(Company.created_date >= filters['date_from'])
            if filters.get('date_to'):
                query = query.filter(Company.created_date <= filters['date_to'])
        
        return query.order_by(desc(Company.created_date)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, company_id: int) -> Optional[Company]:
        return db.query(Company).filter(Company.id == company_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[Company]:
        return db.query(Company).filter(Company.email == email).first()
    
    @staticmethod
    def create(db: Session, company_data: Dict[str, Any]) -> Company:
        db_company = Company(**company_data)
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return db_company
    
    @staticmethod
    def update(db: Session, company_id: int, company_data: Dict[str, Any]) -> Optional[Company]:
        db_company = CompanyRepository.get_by_id(db, company_id)
        if db_company:
            for key, value in company_data.items():
                if value is not None:
                    setattr(db_company, key, value)
            db_company.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_company)
        return db_company
    
    @staticmethod
    def delete(db: Session, company_id: int) -> bool:
        db_company = CompanyRepository.get_by_id(db, company_id)
        if db_company:
            db.delete(db_company)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_count(db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        query = db.query(func.count(Company.id))
        if filters and filters.get('status'):
            query = query.filter(Company.status == filters['status'])
        return query.scalar()
    
    @staticmethod
    def get_active_count(db: Session) -> int:
        return db.query(func.count(Company.id)).filter(
            Company.status == CompanyStatus.ACTIVE
        ).scalar()
    
    @staticmethod
    def get_inactive_count(db: Session) -> int:
        return db.query(func.count(Company.id)).filter(
            Company.status == CompanyStatus.INACTIVE
        ).scalar()
    
    @staticmethod
    def search(db: Session, search_term: str, limit: int = 10) -> List[Company]:
        return db.query(Company).filter(
            or_(
                Company.name.ilike(f"%{search_term}%"),
                Company.email.ilike(f"%{search_term}%")
            )
        ).limit(limit).all()

class PackageRepository:
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Package]:
        query = db.query(Package)
        
        if filters:
            if filters.get('status'):
                query = query.filter(Package.status == filters['status'])
            if filters.get('plan_type'):
                query = query.filter(Package.plan_type == filters['plan_type'])
        
        return query.order_by(Package.position, desc(Package.created_date)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, package_id: int) -> Optional[Package]:
        return db.query(Package).filter(Package.id == package_id).first()
    
    @staticmethod
    def create(db: Session, package_data: Dict[str, Any], modules: List[Dict[str, Any]]) -> Package:
        db_package = Package(**package_data)
        db.add(db_package)
        db.flush()
        
        # Add modules
        for module in modules:
            db_module = PackageModule(package_id=db_package.id, **module)
            db.add(db_module)
        
        db.commit()
        db.refresh(db_package)
        return db_package
    
    @staticmethod
    def update(db: Session, package_id: int, package_data: Dict[str, Any]) -> Optional[Package]:
        db_package = PackageRepository.get_by_id(db, package_id)
        if db_package:
            for key, value in package_data.items():
                if value is not None:
                    setattr(db_package, key, value)
            db_package.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_package)
        return db_package
    
    @staticmethod
    def delete(db: Session, package_id: int) -> bool:
        db_package = PackageRepository.get_by_id(db, package_id)
        if db_package:
            db.delete(db_package)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_count(db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        query = db.query(func.count(Package.id))
        if filters and filters.get('status'):
            query = query.filter(Package.status == filters['status'])
        return query.scalar()

class SubscriptionRepository:
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Subscription]:
        query = db.query(Subscription)
        
        if filters:
            if filters.get('status'):
                query = query.filter(Subscription.status == filters['status'])
            if filters.get('payment_method'):
                query = query.filter(Subscription.payment_method == filters['payment_method'])
            if filters.get('date_from'):
                query = query.filter(Subscription.created_date >= filters['date_from'])
            if filters.get('date_to'):
                query = query.filter(Subscription.created_date <= filters['date_to'])
        
        return query.order_by(desc(Subscription.created_date)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, subscription_id: int) -> Optional[Subscription]:
        return db.query(Subscription).filter(Subscription.id == subscription_id).first()
    
    @staticmethod
    def create(db: Session, subscription_data: Dict[str, Any]) -> Subscription:
        db_subscription = Subscription(**subscription_data)
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        return db_subscription
    
    @staticmethod
    def get_count(db: Session) -> int:
        return db.query(func.count(Subscription.id)).scalar()
    
    @staticmethod
    def get_active_count(db: Session) -> int:
        return db.query(func.count(Subscription.id)).filter(
            Subscription.status == PaymentStatus.PAID,
            Subscription.expiring_on > datetime.utcnow()
        ).scalar()
    
    @staticmethod
    def get_expired_count(db: Session) -> int:
        return db.query(func.count(Subscription.id)).filter(
            Subscription.expiring_on < datetime.utcnow()
        ).scalar()

class TransactionRepository:
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Transaction]:
        query = db.query(Transaction)
        
        if filters:
            if filters.get('status'):
                query = query.filter(Transaction.status == filters['status'])
            if filters.get('payment_method'):
                query = query.filter(Transaction.payment_method == filters['payment_method'])
            if filters.get('date_from'):
                query = query.filter(Transaction.payment_date >= filters['date_from'])
            if filters.get('date_to'):
                query = query.filter(Transaction.payment_date <= filters['date_to'])
        
        return query.order_by(desc(Transaction.payment_date)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, transaction_id: int) -> Optional[Transaction]:
        return db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    @staticmethod
    def get_by_invoice_id(db: Session, invoice_id: str) -> Optional[Transaction]:
        return db.query(Transaction).filter(Transaction.invoice_id == invoice_id).first()
    
    @staticmethod
    def create(db: Session, transaction_data: Dict[str, Any]) -> Transaction:
        db_transaction = Transaction(**transaction_data)
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    
    @staticmethod
    def delete(db: Session, transaction_id: int) -> bool:
        db_transaction = TransactionRepository.get_by_id(db, transaction_id)
        if db_transaction:
            db.delete(db_transaction)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_total_earnings(db: Session) -> float:
        result = db.query(func.sum(Transaction.total)).filter(
            Transaction.status == PaymentStatus.PAID
        ).scalar()
        return float(result) if result else 0.0
    
    @staticmethod
    def get_count(db: Session) -> int:
        return db.query(func.count(Transaction.id)).scalar()

class DomainRepository:
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Domain]:
        query = db.query(Domain)
        
        if filters:
            if filters.get('status'):
                query = query.filter(Domain.status == filters['status'])
            if filters.get('plan_name'):
                query = query.filter(Domain.plan_name == filters['plan_name'])
            if filters.get('date_from'):
                query = query.filter(Domain.created_date >= filters['date_from'])
            if filters.get('date_to'):
                query = query.filter(Domain.created_date <= filters['date_to'])
        
        return query.order_by(desc(Domain.created_date)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, domain_id: int) -> Optional[Domain]:
        return db.query(Domain).filter(Domain.id == domain_id).first()
    
    @staticmethod
    def get_by_url(db: Session, domain_url: str) -> Optional[Domain]:
        return db.query(Domain).filter(Domain.domain_url == domain_url).first()
    
    @staticmethod
    def create(db: Session, domain_data: Dict[str, Any]) -> Domain:
        db_domain = Domain(**domain_data)
        db.add(db_domain)
        db.commit()
        db.refresh(db_domain)
        return db_domain
    
    @staticmethod
    def update_status(db: Session, domain_id: int, status: DomainStatus) -> Optional[Domain]:
        db_domain = DomainRepository.get_by_id(db, domain_id)
        if db_domain:
            db_domain.status = status
            db.commit()
            db.refresh(db_domain)
        return db_domain
    
    @staticmethod
    def delete(db: Session, domain_id: int) -> bool:
        db_domain = DomainRepository.get_by_id(db, domain_id)
        if db_domain:
            db.delete(db_domain)
            db.commit()
            return True
        return False