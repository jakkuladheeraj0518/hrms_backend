from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Company
from app.schemas import Company as CompanySchema, CompanyCreate, CompanyUpdate

router = APIRouter(prefix="/api/companies", tags=["Companies"])

@router.get("/", response_model=List[CompanySchema])
def get_companies(
    skip: int = 0,
    limit: int = 100,
    plan: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all companies with optional filters"""
    query = db.query(Company)
    
    if plan:
        query = query.filter(Company.plan_type == plan)
    
    if status:
        query = query.filter(Company.status == status)
    
    if search:
        query = query.filter(
            (Company.name.ilike(f"%{search}%")) |
            (Company.email.ilike(f"%{search}%")) |
            (Company.account_url.ilike(f"%{search}%"))
        )
    
    companies = query.offset(skip).limit(limit).all()
    return companies

@router.get("/stats")
def get_company_stats(db: Session = Depends(get_db)):
    """Get company statistics"""
    total_companies = db.query(Company).count()
    active_companies = db.query(Company).filter(Company.status == "Active").count()
    inactive_companies = db.query(Company).filter(Company.status == "Inactive").count()
    
    # Count unique locations (based on address)
    locations = db.query(func.count(func.distinct(Company.address))).scalar()
    
    return {
        "total_companies": total_companies,
        "active_companies": active_companies,
        "inactive_companies": inactive_companies,
        "company_locations": locations
    }

@router.get("/{company_id}", response_model=CompanySchema)
def get_company(company_id: int, db: Session = Depends(get_db)):
    """Get a specific company by ID"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.post("/", response_model=CompanySchema)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """Create a new company"""
    # Check if email already exists
    existing = db.query(Company).filter(Company.email == company.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if account URL already exists
    if company.account_url:
        existing_url = db.query(Company).filter(Company.account_url == company.account_url).first()
        if existing_url:
            raise HTTPException(status_code=400, detail="Account URL already taken")
    
    # Create new company
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.put("/{company_id}", response_model=CompanySchema)
def update_company(
    company_id: int,
    company_update: CompanyUpdate,
    db: Session = Depends(get_db)
):
    """Update a company"""
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Update only provided fields
    update_data = company_update.dict(exclude_unset=True)
    
    # Check email uniqueness if updating
    if "email" in update_data and update_data["email"] != db_company.email:
        existing = db.query(Company).filter(Company.email == update_data["email"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check account URL uniqueness if updating
    if "account_url" in update_data and update_data["account_url"] != db_company.account_url:
        existing_url = db.query(Company).filter(Company.account_url == update_data["account_url"]).first()
        if existing_url:
            raise HTTPException(status_code=400, detail="Account URL already taken")
    
    for key, value in update_data.items():
        setattr(db_company, key, value)
    
    db.commit()
    db.refresh(db_company)
    return db_company

@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    """Delete a company"""
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db.delete(db_company)
    db.commit()
    return {"message": "Company deleted successfully"}

@router.post("/{company_id}/upgrade")
def upgrade_company_plan(
    company_id: int,
    plan_name: str,
    plan_type: str,
    amount: float,
    payment_date: str,
    next_payment_date: str,
    expiring_on: str,
    db: Session = Depends(get_db)
):
    """Upgrade company plan"""
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Update company plan details
    db_company.plan_name = plan_name
    db_company.plan_type = plan_type
    db_company.price = amount
    db_company.expiring_on = datetime.strptime(expiring_on, "%Y-%m-%d").date()
    
    db.commit()
    db.refresh(db_company)
    
    return {
        "message": "Plan upgraded successfully",
        "company": db_company
    }