from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import datacapture_schema as schemas
from app.services import datacapture_service as service
from app.database.session import get_db

# =========================================================
# Router Configuration
# =========================================================
router = APIRouter(prefix="/api/tds-returns", tags=["TDS Returns"])

# =========================================================
# CREATE
# =========================================================
@router.post("/", response_model=schemas.TDSReturn)
def create_tds_return(
    tds_return: schemas.TDSReturnCreate,
    db: Session = Depends(get_db)
):
    """Create a new TDS Return record."""
    return service.create_tds_return(db, tds_return)

# =========================================================
# READ ALL
# =========================================================
@router.get("/", response_model=List[schemas.TDSReturn])
def read_tds_returns(db: Session = Depends(get_db)):
    """Fetch all TDS Return records."""
    return service.get_tds_returns(db)

# =========================================================
# READ BY FINANCIAL YEAR & QUARTER
# =========================================================
@router.get("/{financial_year}/{quarter}", response_model=schemas.TDSReturn)
def read_tds_return_by_quarter(
    financial_year: str,
    quarter: str,
    db: Session = Depends(get_db)
):
    """Fetch a TDS Return by financial year and quarter."""
    db_return = service.get_tds_return_by_quarter(db, financial_year, quarter)
    if not db_return:
        raise HTTPException(status_code=404, detail="TDS Return not found")
    return db_return

# =========================================================
# UPDATE
# =========================================================
@router.put("/{tds_return_id}", response_model=schemas.TDSReturn)
def update_tds_return(
    tds_return_id: int,
    tds_return_update: schemas.TDSReturnCreate,
    db: Session = Depends(get_db)
):
    """Update an existing TDS Return record."""
    updated = service.update_tds_return(db, tds_return_id, tds_return_update)
    if not updated:
        raise HTTPException(status_code=404, detail="TDS Return not found")
    return updated

# =========================================================
# DELETE
# =========================================================
@router.delete("/{tds_return_id}", response_model=dict)
def delete_tds_return(
    tds_return_id: int,
    db: Session = Depends(get_db)
):
    """Delete a TDS Return record by ID."""
    success = service.delete_tds_return(db, tds_return_id)
    if not success:
        raise HTTPException(status_code=404, detail="TDS Return not found")
    return {"detail": "TDS Return deleted successfully"}
