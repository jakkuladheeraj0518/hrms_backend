from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models.superadmin import Transaction, Company
from app.schemas.superadmin import TransactionResponse as TransactionSchema, TransactionCreate, TransactionUpdate

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])

@router.get("/", response_model=List[TransactionSchema])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    payment_method: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all transactions with optional filters"""
    query = db.query(Transaction)
    
    if status:
        query = query.filter(Transaction.status == status)
    
    if payment_method:
        query = query.filter(Transaction.payment_method == payment_method)
    
    if start_date:
        query = query.filter(Transaction.date >= datetime.strptime(start_date, "%Y-%m-%d").date())
    
    if end_date:
        query = query.filter(Transaction.date <= datetime.strptime(end_date, "%Y-%m-%d").date())
    
    transactions = query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()
    return transactions

@router.get("/stats")
def get_transaction_stats(db: Session = Depends(get_db)):
    """Get transaction statistics"""
    total_transactions = db.query(Transaction).count()
    total_paid = db.query(func.sum(Transaction.amount))\
        .filter(Transaction.status == "Paid").scalar() or 0.0
    total_unpaid = db.query(func.sum(Transaction.amount))\
        .filter(Transaction.status == "Unpaid").scalar() or 0.0
    
    paid_count = db.query(Transaction).filter(Transaction.status == "Paid").count()
    unpaid_count = db.query(Transaction).filter(Transaction.status == "Unpaid").count()
    
    return {
        "total_transactions": total_transactions,
        "total_paid_amount": round(total_paid, 2),
        "total_unpaid_amount": round(total_unpaid, 2),
        "paid_count": paid_count,
        "unpaid_count": unpaid_count
    }

@router.get("/{transaction_id}", response_model=TransactionSchema)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get a specific transaction by ID"""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.get("/invoice/{invoice_id}")
def get_transaction_by_invoice(invoice_id: str, db: Session = Depends(get_db)):
    """Get transaction by invoice ID with full details"""
    transaction = db.query(Transaction).filter(Transaction.invoice_id == invoice_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    company = db.query(Company).filter(Company.id == transaction.company_id).first()
    
    return {
        "id": transaction.id,
        "invoice_id": transaction.invoice_id,
        "company_id": transaction.company_id,
        "company_name": company.name if company else "N/A",
        "company_email": company.email if company else "N/A",
        "company_logo": company.logo if company else None,
        "amount": transaction.amount,
        "payment_method": transaction.payment_method,
        "status": transaction.status,
        "date": transaction.date,
        "due_date": transaction.due_date,
        "plan": transaction.plan,
        "billing_cycle": transaction.billing_cycle,
        "subtotal": transaction.subtotal,
        "tax": transaction.tax,
        "total": transaction.total,
        "from": {
            "name": transaction.from_name,
            "address": transaction.from_address,
            "email": transaction.from_email
        },
        "to": {
            "name": transaction.to_name,
            "address": transaction.to_address,
            "email": transaction.to_email
        }
    }

@router.post("/", response_model=TransactionSchema)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """Create a new transaction"""
    # Check if invoice ID already exists
    existing = db.query(Transaction).filter(Transaction.invoice_id == transaction.invoice_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Invoice ID already exists")
    
    # Check if company exists
    company = db.query(Company).filter(Company.id == transaction.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.put("/{transaction_id}", response_model=TransactionSchema)
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db)
):
    """Update a transaction"""
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    update_data = transaction_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_transaction, key, value)
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.patch("/{transaction_id}/status")
def update_transaction_status(
    transaction_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update transaction status"""
    if status not in ["Paid", "Unpaid"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db_transaction.status = status
    db.commit()
    db.refresh(db_transaction)
    
    return {
        "message": f"Transaction status updated to {status}",
        "transaction": db_transaction
    }

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Delete a transaction"""
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}