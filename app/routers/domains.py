from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Domain, Company
from app.schemas import Domain as DomainSchema, DomainCreate, DomainUpdate

router = APIRouter(prefix="/api/domains", tags=["Domains"])

@router.get("/", response_model=List[DomainSchema])
def get_domains(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    plan: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all domains with optional filters"""
    query = db.query(Domain)
    
    if status:
        query = query.filter(Domain.status == status)
    
    if plan:
        query = query.filter(Domain.plan_type == plan)
    
    domains = query.offset(skip).limit(limit).all()
    return domains

@router.get("/{domain_id}", response_model=DomainSchema)
def get_domain(domain_id: int, db: Session = Depends(get_db)):
    """Get a specific domain by ID"""
    domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    return domain

@router.get("/{domain_id}/details")
def get_domain_details(domain_id: int, db: Session = Depends(get_db)):
    """Get domain with company details"""
    domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    company = db.query(Company).filter(Company.id == domain.company_id).first()
    
    return {
        "id": domain.id,
        "domain_url": domain.domain_url,
        "plan": domain.plan,
        "plan_type": domain.plan_type,
        "status": domain.status,
        "price": domain.price,
        "created_date": domain.created_date,
        "expiring_on": domain.expiring_on,
        "company": {
            "name": company.name,
            "email": company.email,
            "logo": company.logo
        } if company else None
    }

@router.post("/", response_model=DomainSchema)
def create_domain(domain: DomainCreate, db: Session = Depends(get_db)):
    """Create a new domain"""
    # Check if domain URL already exists
    existing = db.query(Domain).filter(Domain.domain_url == domain.domain_url).first()
    if existing:
        raise HTTPException(status_code=400, detail="Domain URL already exists")
    
    # Check if company exists
    company = db.query(Company).filter(Company.id == domain.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_domain = Domain(**domain.dict())
    db.add(db_domain)
    db.commit()
    db.refresh(db_domain)
    return db_domain

@router.put("/{domain_id}", response_model=DomainSchema)
def update_domain(
    domain_id: int,
    domain_update: DomainUpdate,
    db: Session = Depends(get_db)
):
    """Update a domain"""
    db_domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not db_domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    update_data = domain_update.dict(exclude_unset=True)
    
    # Check domain URL uniqueness if updating
    if "domain_url" in update_data and update_data["domain_url"] != db_domain.domain_url:
        existing = db.query(Domain).filter(Domain.domain_url == update_data["domain_url"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Domain URL already exists")
    
    for key, value in update_data.items():
        setattr(db_domain, key, value)
    
    db.commit()
    db.refresh(db_domain)
    return db_domain

@router.patch("/{domain_id}/status")
def update_domain_status(
    domain_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update domain status (Approve/Reject)"""
    if status not in ["Approved", "Rejected", "Pending"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    db_domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not db_domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    db_domain.status = status
    db.commit()
    db.refresh(db_domain)
    
    return {
        "message": f"Domain status updated to {status}",
        "domain": db_domain
    }

@router.delete("/{domain_id}")
def delete_domain(domain_id: int, db: Session = Depends(get_db)):
    """Delete a domain"""
    db_domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not db_domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    db.delete(db_domain)
    db.commit()
    return {"message": "Domain deleted successfully"}