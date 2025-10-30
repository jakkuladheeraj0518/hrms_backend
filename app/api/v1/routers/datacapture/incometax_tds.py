from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import datacapture_schema as schemas
from app.services import datacapture_service as service
from app.models import datacapture as models
from app.database.session import get_db

router = APIRouter(prefix="/api/datacapture/incometax-tds", tags=["Income Tax TDS"])

# =========================================================
# CREATE Income Tax TDS Record
# =========================================================
@router.post("/", response_model=schemas.IncomeTaxTDS)
def create_income_tax_tds(income_tds: schemas.IncomeTaxTDSCreate, db: Session = Depends(get_db)):
    """Create a new Income Tax TDS record"""
    return service.create_income_tax_tds(db, income_tds)


# =========================================================
# READ All Income Tax TDS Records
# =========================================================
@router.get("/", response_model=List[schemas.IncomeTaxTDS])
def get_all_income_tax_tds(db: Session = Depends(get_db)):
    """Retrieve all Income Tax TDS records"""
    return service.get_all_income_tax_tds(db)


# =========================================================
# READ Income Tax TDS by ID
# =========================================================
@router.get("/{tds_id}", response_model=schemas.IncomeTaxTDS)
def get_income_tax_tds_by_id(tds_id: int, db: Session = Depends(get_db)):
    """Retrieve a single Income Tax TDS record by ID"""
    record = service.get_income_tax_tds_by_id(db, tds_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Income Tax TDS record with ID {tds_id} not found")
    return record


# =========================================================
# UPDATE Income Tax TDS Record
# =========================================================
@router.put("/{tds_id}", response_model=schemas.IncomeTaxTDS)
def update_income_tax_tds(tds_id: int, income_tds: schemas.IncomeTaxTDSCreate, db: Session = Depends(get_db)):
    """Update an existing Income Tax TDS record"""
    record = service.update_income_tax_tds(db, tds_id, income_tds)
    if not record:
        raise HTTPException(status_code=404, detail=f"Income Tax TDS record with ID {tds_id} not found")
    return record


# =========================================================
# DELETE Income Tax TDS Record
# =========================================================
@router.delete("/{tds_id}")
def delete_income_tax_tds(tds_id: int, db: Session = Depends(get_db)):
    """Delete an Income Tax TDS record"""
    ok = service.delete_income_tax_tds(db, tds_id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Income Tax TDS record with ID {tds_id} not found")
    return {"detail": f"Income Tax TDS record with ID {tds_id} deleted successfully"}
