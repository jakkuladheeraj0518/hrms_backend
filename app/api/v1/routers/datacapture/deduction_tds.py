from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database.session import get_db

from app.models import datacapture as models
from app.schemas import datacapture_schema as schemas

router = APIRouter(
    prefix="/api/deduction-tds",
    tags=["Deduction TDS"]
)

# =========================================================
# GET: All Deduction TDS Records (with optional filters)
# =========================================================
@router.get("/", response_model=List[schemas.DeductionTDSBase])
def get_all_deduction_tds(
    month: Optional[str] = Query(None, description="Filter by month, e.g., '2025-10'"),
    name: Optional[str] = Query(None, description="Filter by employee name"),
    db: Session = Depends(get_db)
):
    """Retrieve all Deduction TDS records, optionally filtered by month or name."""
    query = db.query(models.DeductionTDS)

    if month:
        query = query.filter(models.DeductionTDS.month == month)
    if name:
        query = query.filter(models.DeductionTDS.name.ilike(f"%{name}%"))

    return query.order_by(models.DeductionTDS.id.desc()).all()


# =========================================================
# GET: Single Record by ID
# =========================================================
@router.get("/{deduction_id}", response_model=schemas.DeductionTDSBase)
def get_deduction_tds_by_id(deduction_id: int, db: Session = Depends(get_db)):
    """Retrieve a Deduction TDS record by ID."""
    record = db.query(models.DeductionTDS).filter(models.DeductionTDS.id == deduction_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Deduction TDS record with ID {deduction_id} not found")
    return record


# =========================================================
# POST: Create New Deduction TDS Record
# =========================================================
@router.post("/", response_model=schemas.DeductionTDSBase)
def create_deduction_tds(
    deduction_tds: schemas.DeductionTDSCreate,
    db: Session = Depends(get_db)
):
    """Create a new Deduction TDS record."""
    netsalary = (
        deduction_tds.grosssalary
        - deduction_tds.calculatedexemptions
        - deduction_tds.additionalexemptions
    )

    new_record = models.DeductionTDS(
        name=deduction_tds.name,
        position=deduction_tds.position,
        grosssalary=deduction_tds.grosssalary,
        calculatedexemptions=deduction_tds.calculatedexemptions,
        additionalexemptions=deduction_tds.additionalexemptions,
        netsalary=netsalary,
        code=deduction_tds.code,
        month=deduction_tds.month,
        created_date=date.today()
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


# =========================================================
# PUT: Update Existing Record
# =========================================================
@router.put("/{deduction_id}", response_model=schemas.DeductionTDSBase)
def update_deduction_tds(
    deduction_id: int,
    deduction_tds: schemas.DeductionTDSCreate,
    db: Session = Depends(get_db)
):
    """Update an existing Deduction TDS record by ID."""
    record = db.query(models.DeductionTDS).filter(models.DeductionTDS.id == deduction_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Deduction TDS record with ID {deduction_id} not found")

    record.name = deduction_tds.name
    record.position = deduction_tds.position
    record.grosssalary = deduction_tds.grosssalary
    record.calculatedexemptions = deduction_tds.calculatedexemptions
    record.additionalexemptions = deduction_tds.additionalexemptions
    record.code = deduction_tds.code
    record.month = deduction_tds.month
    record.netsalary = (
        deduction_tds.grosssalary
        - deduction_tds.calculatedexemptions
        - deduction_tds.additionalexemptions
    )

    db.commit()
    db.refresh(record)
    return record


# =========================================================
# DELETE: Remove Record
# =========================================================
@router.delete("/{deduction_id}", response_model=dict)
def delete_deduction_tds(deduction_id: int, db: Session = Depends(get_db)):
    """Delete a Deduction TDS record by ID."""
    record = db.query(models.DeductionTDS).filter(models.DeductionTDS.id == deduction_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Deduction TDS record with ID {deduction_id} not found")

    db.delete(record)
    db.commit()
    return {"detail": f"Deduction TDS record with ID {deduction_id} deleted successfully"}
