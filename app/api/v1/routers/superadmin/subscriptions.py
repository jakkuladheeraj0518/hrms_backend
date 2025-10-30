from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, date

from app.database import get_db
from app.models.superadmin import Subscription, Company, Package
from app.schemas.superadmin import SubscriptionResponse as SubscriptionSchema, SubscriptionCreate, SubscriptionUpdate

router = APIRouter(prefix="/api/subscriptions", tags=["Subscriptions"])

@router.get("/", response_model=List[SubscriptionSchema])
def get_subscriptions(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    plan: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all subscriptions with optional filters"""
    query = db.query(Subscription)
    
    if status:
        query = query.filter(Subscription.status == status)
    
    if plan:
        query = query.filter(Subscription.plan.ilike(f"%{plan}%"))
    
    subscriptions = query.order_by(Subscription.created_date.desc()).offset(skip).limit(limit).all()
    return subscriptions

@router.get("/stats")
def get_subscription_stats(db: Session = Depends(get_db)):
    """Get subscription statistics"""
    total_revenue = db.query(func.sum(Subscription.amount))\
        .filter(Subscription.status == "Paid").scalar() or 0.0
    
    total_subscribers = db.query(Subscription).count()
    active_subscribers = db.query(Subscription).filter(Subscription.status == "Paid").count()
    
    # Count expired subscriptions
    today = date.today()
    expired_subscribers = db.query(Subscription)\
        .filter(Subscription.expiring_on < today)\
        .count()
    
    return {
        "total_revenue": round(total_revenue, 2),
        "total_subscribers": total_subscribers,
        "active_subscribers": active_subscribers,
        "expired_subscribers": expired_subscribers
    }

@router.get("/with-details")
def get_subscriptions_with_details(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get subscriptions with company details"""
    subscriptions = db.query(Subscription).offset(skip).limit(limit).all()
    
    result = []
    for sub in subscriptions:
        company = db.query(Company).filter(Company.id == sub.company_id).first()
        package = db.query(Package).filter(Package.id == sub.package_id).first() if sub.package_id else None
        
        result.append({
            "id": sub.id,
            "company_name": company.name if company else "N/A",
            "company_email": company.email if company else "N/A",
            "plan": sub.plan,
            "billing_cycle": sub.billing_cycle,
            "payment_method": sub.payment_method,
            "amount": sub.amount,
            "status": sub.status,
            "created_date": sub.created_date,
            "expiring_on": sub.expiring_on,
            "package_details": {
                "name": package.name,
                "type": package.type
            } if package else None
        })
    
    return result

@router.get("/{subscription_id}", response_model=SubscriptionSchema)
def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """Get a specific subscription by ID"""
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@router.get("/company/{company_id}")
def get_company_subscriptions(company_id: int, db: Session = Depends(get_db)):
    """Get all subscriptions for a specific company"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    subscriptions = db.query(Subscription)\
        .filter(Subscription.company_id == company_id)\
        .order_by(Subscription.created_date.desc())\
        .all()
    
    return {
        "company": {
            "id": company.id,
            "name": company.name,
            "email": company.email
        },
        "subscriptions": subscriptions
    }

@router.post("/", response_model=SubscriptionSchema)
def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    """Create a new subscription"""
    # Check if company exists
    company = db.query(Company).filter(Company.id == subscription.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Check if package exists if package_id is provided
    if subscription.package_id:
        package = db.query(Package).filter(Package.id == subscription.package_id).first()
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")
    
    db_subscription = Subscription(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@router.put("/{subscription_id}", response_model=SubscriptionSchema)
def update_subscription(
    subscription_id: int,
    subscription_update: SubscriptionUpdate,
    db: Session = Depends(get_db)
):
    """Update a subscription"""
    db_subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    update_data = subscription_update.dict(exclude_unset=True)
    
    # Check if package exists if package_id is being updated
    if "package_id" in update_data and update_data["package_id"]:
        package = db.query(Package).filter(Package.id == update_data["package_id"]).first()
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")
    
    for key, value in update_data.items():
        setattr(db_subscription, key, value)
    
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@router.patch("/{subscription_id}/status")
def update_subscription_status(
    subscription_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update subscription status"""
    if status not in ["Paid", "Unpaid", "Expired"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    db_subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db_subscription.status = status
    db.commit()
    db.refresh(db_subscription)
    
    return {
        "message": f"Subscription status updated to {status}",
        "subscription": db_subscription
    }

@router.delete("/{subscription_id}")
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """Delete a subscription"""
    db_subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db.delete(db_subscription)
    db.commit()
    return {"message": "Subscription deleted successfully"}

@router.post("/check-expired")
def check_and_update_expired_subscriptions(db: Session = Depends(get_db)):
    """Check and update expired subscriptions"""
    today = date.today()
    
    expired_subs = db.query(Subscription)\
        .filter(Subscription.expiring_on < today)\
        .filter(Subscription.status != "Expired")\
        .all()
    
    count = 0
    for sub in expired_subs:
        sub.status = "Expired"
        count += 1
    
    db.commit()
    
    return {
        "message": f"Updated {count} expired subscriptions",
        "count": count
    }