from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db

from app.schemas import datacapture_schema as schemas
from app.services import datacapture_service as service

# Router Configuration
router = APIRouter(prefix="/api/datacapture/loans", tags=["Data Capture Loans"])


# ---------------------------
# CREATE
# ---------------------------
@router.post("/", response_model=schemas.DataCaptureLoan)
def create_loan(
    loan: schemas.DataCaptureLoanCreate,
    db: Session = Depends(get_db),
):
    """Create a new Data Capture Loan record"""
    return service.create_data_capture_loan(db, loan)


# ---------------------------
# READ ALL
# ---------------------------
@router.get("/", response_model=List[schemas.DataCaptureLoan])
def read_loans(db: Session = Depends(get_db)):
    """Retrieve all Data Capture Loan records"""
    return service.get_data_capture_loans(db)


# ---------------------------
# READ BY ID
# ---------------------------
@router.get("/{loan_id}", response_model=schemas.DataCaptureLoan)
def read_loan_by_id(loan_id: int, db: Session = Depends(get_db)):
    """Retrieve a single Data Capture Loan record by ID"""
    loan = service.get_data_capture_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail=f"Loan with ID {loan_id} not found")
    return loan


# ---------------------------
# UPDATE
# ---------------------------
@router.put("/{loan_id}", response_model=schemas.DataCaptureLoan)
def update_loan(
    loan_id: int,
    loan_update: schemas.DataCaptureLoanCreate,
    db: Session = Depends(get_db),
):
    """Update an existing Data Capture Loan record"""
    updated_loan = service.update_data_capture_loan(db, loan_id, loan_update)
    if not updated_loan:
        raise HTTPException(status_code=404, detail=f"Loan with ID {loan_id} not found")
    return updated_loan


# ---------------------------
# DELETE
# ---------------------------
@router.delete("/{loan_id}")
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    """Delete a Data Capture Loan record"""
    success = service.delete_data_capture_loan(db, loan_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Loan with ID {loan_id} not found")
    return {"detail": f"Loan with ID {loan_id} deleted successfully"}
