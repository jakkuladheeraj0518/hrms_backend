from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.database import get_db
from app.models import Package, Subscription
from app.schemas import Package as PackageSchema, PackageCreate, PackageUpdate

router = APIRouter(prefix="/api/packages", tags=["Packages"])

@router.get("/", response_model=List[PackageSchema])
def get_packages(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all packages with optional filters"""
    query = db.query(Package)
    
    if type:
        query = query.filter(Package.type == type)
    
    if status:
        query = query.filter(Package.status == status)
    
    if search:
        query = query.filter(Package.name.ilike(f"%{search}%"))
    
    packages = query.offset(skip).limit(limit).all()
    return packages

@router.get("/stats")
def get_package_stats(db: Session = Depends(get_db)):
    """Get package statistics"""
    total_plans = db.query(Package).count()
    active_plans = db.query(Package).filter(Package.status == "Active").count()
    inactive_plans = db.query(Package).filter(Package.status == "Inactive").count()
    plan_types = db.query(func.count(func.distinct(Package.type))).scalar()
    
    return {
        "total_plans": total_plans,
        "active_plans": active_plans,
        "inactive_plans": inactive_plans,
        "plan_types": plan_types
    }

@router.get("/with-subscribers")
def get_packages_with_subscribers(db: Session = Depends(get_db)):
    """Get all packages with subscriber counts"""
    packages = db.query(Package).all()
    
    result = []
    for package in packages:
        subscriber_count = db.query(Subscription)\
            .filter(Subscription.package_id == package.id)\
            .count()
        
        result.append({
            "id": package.id,
            "name": package.name,
            "type": package.type,
            "price": package.price,
            "subscribers": subscriber_count,
            "status": package.status,
            "created_date": package.created_date
        })
    
    return result

@router.get("/{package_id}", response_model=PackageSchema)
def get_package(package_id: int, db: Session = Depends(get_db)):
    """Get a specific package by ID"""
    package = db.query(Package).filter(Package.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package

@router.post("/", response_model=PackageSchema)
def create_package(package: PackageCreate, db: Session = Depends(get_db)):
    """Create a new package"""
    # Check if package with same name and type exists
    existing = db.query(Package).filter(
        Package.name == package.name,
        Package.type == package.type
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Package '{package.name}' with type '{package.type}' already exists"
        )
    
    db_package = Package(**package.dict())
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package

@router.put("/{package_id}", response_model=PackageSchema)
def update_package(
    package_id: int,
    package_update: PackageUpdate,
    db: Session = Depends(get_db)
):
    """Update a package"""
    db_package = db.query(Package).filter(Package.id == package_id).first()
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")
    
    update_data = package_update.dict(exclude_unset=True)
    
    # Check uniqueness if name or type is being updated
    if "name" in update_data or "type" in update_data:
        new_name = update_data.get("name", db_package.name)
        new_type = update_data.get("type", db_package.type)
        
        existing = db.query(Package).filter(
            Package.name == new_name,
            Package.type == new_type,
            Package.id != package_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Package '{new_name}' with type '{new_type}' already exists"
            )
    
    for key, value in update_data.items():
        setattr(db_package, key, value)
    
    db.commit()
    db.refresh(db_package)
    return db_package

@router.delete("/{package_id}")
def delete_package(package_id: int, db: Session = Depends(get_db)):
    """Delete a package"""
    db_package = db.query(Package).filter(Package.id == package_id).first()
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")
    
    # Check if package has active subscriptions
    active_subs = db.query(Subscription)\
        .filter(Subscription.package_id == package_id)\
        .filter(Subscription.status == "Paid")\
        .count()
    
    if active_subs > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete package with {active_subs} active subscriptions"
        )
    
    db.delete(db_package)
    db.commit()
    return {"message": "Package deleted successfully"}