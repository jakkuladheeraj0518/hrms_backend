from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import datacapture_schema as schemas
from app.services import datacapture_service as service
from app.models import datacapture as models
from app.database.session import get_db

router = APIRouter(prefix="/api/datacapture/extra-days", tags=["Extra Days"])

# =========================================================
# CREATE Extra Days Record
# =========================================================
@router.post("/", response_model=schemas.ExtraDays)
def create_extra_days(extra_days: schemas.ExtraDaysCreate, db: Session = Depends(get_db)):
    """Create a new Extra Days record"""
    return service.create_extra_days(db, extra_days)


# =========================================================
# READ All Extra Days Records
# =========================================================
@router.get("/", response_model=List[schemas.ExtraDays])
def read_extra_days(db: Session = Depends(get_db)):
    """Retrieve all Extra Days records"""
    return service.get_extra_days(db)


# =========================================================
# READ Extra Days by Employee Code
# =========================================================
@router.get("/employee/{employee_code}", response_model=List[schemas.ExtraDays])
def read_extra_days_by_employee(employee_code: str, db: Session = Depends(get_db)):
    """Retrieve Extra Days records by Employee Code"""
    records = db.query(models.ExtraDays).filter(models.ExtraDays.employee_code == employee_code).all()
    if not records:
        raise HTTPException(status_code=404, detail=f"No Extra Days records found for employee code '{employee_code}'")
    return records


# =========================================================
# UPDATE Extra Days Record
# =========================================================
@router.put("/{extra_days_id}", response_model=schemas.ExtraDays)
def update_extra_days(extra_days_id: int, extra_days: schemas.ExtraDaysCreate, db: Session = Depends(get_db)):
    """Update an existing Extra Days record"""
    db_record = db.query(models.ExtraDays).filter(models.ExtraDays.id == extra_days_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Extra Days record not found")

    for key, value in extra_days.dict().items():
        setattr(db_record, key, value)

    db.commit()
    db.refresh(db_record)
    return db_record


# =========================================================
# DELETE Extra Days Record
# =========================================================
@router.delete("/{extra_days_id}")
def delete_extra_days(extra_days_id: int, db: Session = Depends(get_db)):
    """Delete an Extra Days record"""
    db_record = db.query(models.ExtraDays).filter(models.ExtraDays.id == extra_days_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Extra Days record not found")

    db.delete(db_record)
    db.commit()
    return {"detail": f"Extra Days record with ID {extra_days_id} deleted successfully"}
