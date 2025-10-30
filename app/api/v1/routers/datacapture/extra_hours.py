from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import datacapture_schema as schemas
from app.services import datacapture_service as service
from app.models import datacapture as models
from app.database.session import get_db

router = APIRouter(prefix="/api/datacapture/extra-hours", tags=["Extra Hours"])

# =========================================================
# CREATE Extra Hours Record
# =========================================================
@router.post("/", response_model=schemas.ExtraHours)
def create_extra_hours(extra_hours: schemas.ExtraHoursCreate, db: Session = Depends(get_db)):
    """Create a new Extra Hours record"""
    return service.create_extra_hours(db, extra_hours)


# =========================================================
# READ All Extra Hours Records
# =========================================================
@router.get("/", response_model=List[schemas.ExtraHours])
def get_all_extra_hours(db: Session = Depends(get_db)):
    """Retrieve all Extra Hours records"""
    return service.get_extra_hours(db)


# =========================================================
# READ Extra Hours by ID
# =========================================================
@router.get("/{extra_id}", response_model=schemas.ExtraHours)
def get_extra_hours_by_id(extra_id: int, db: Session = Depends(get_db)):
    """Retrieve a single Extra Hours record by its ID"""
    record = db.query(models.ExtraHours).filter(models.ExtraHours.id == extra_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Extra Hours record with ID {extra_id} not found")
    return record


# =========================================================
# UPDATE Extra Hours Record
# =========================================================
@router.put("/{extra_id}", response_model=schemas.ExtraHours)
def update_extra_hours(extra_id: int, extra_update: schemas.ExtraHoursCreate, db: Session = Depends(get_db)):
    """Update an existing Extra Hours record"""
    record = db.query(models.ExtraHours).filter(models.ExtraHours.id == extra_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Extra Hours record with ID {extra_id} not found")

    for key, value in extra_update.dict().items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


# =========================================================
# DELETE Extra Hours Record
# =========================================================
@router.delete("/{extra_id}")
def delete_extra_hours(extra_id: int, db: Session = Depends(get_db)):
    """Delete an Extra Hours record"""
    record = db.query(models.ExtraHours).filter(models.ExtraHours.id == extra_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Extra Hours record with ID {extra_id} not found")

    db.delete(record)
    db.commit()
    return {"detail": f"Extra Hours record with ID {extra_id} deleted successfully"}
