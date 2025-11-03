from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import datacapture_schema as schemas
from app.models import datacapture as models
from app.database.session import get_db

router = APIRouter(prefix="/loans", tags=["Loans"])

# =========================================================
# CREATE LOAN
# =========================================================
@router.post("/", response_model=schemas.Loan)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    """Create a new Loan record"""
    db_loan = models.Loan(**loan.dict())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


# =========================================================
# READ ALL LOANS
# =========================================================
@router.get("/", response_model=List[schemas.Loan])
def get_all_loans(db: Session = Depends(get_db)):
    """Retrieve all Loan records"""
    return db.query(models.Loan).all()


# =========================================================
# READ LOAN BY ID
# =========================================================
@router.get("/{loan_id}", response_model=schemas.Loan)
def get_loan_by_id(loan_id: int, db: Session = Depends(get_db)):
    """Retrieve a Loan record by its ID"""
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail=f"Loan with ID {loan_id} not found")
    return loan


# =========================================================
# UPDATE LOAN
# =========================================================
@router.put("/{loan_id}", response_model=schemas.Loan)
def update_loan(loan_id: int, updated_loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    """Update an existing Loan record"""
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail=f"Loan with ID {loan_id} not found")

    for key, value in updated_loan.dict().items():
        setattr(loan, key, value)

    db.commit()
    db.refresh(loan)
    return loan


# =========================================================
# DELETE LOAN
# =========================================================
@router.delete("/{loan_id}")
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    """Delete a Loan record"""
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail=f"Loan with ID {loan_id} not found")

    db.delete(loan)
    db.commit()
    return {"detail": f"Loan with ID {loan_id} deleted successfully"}
