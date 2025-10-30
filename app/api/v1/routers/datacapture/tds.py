from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import datacapture_schema as schemas
from app.services import datacapture_service as service
from app.database.session import get_db

# =========================================================
# Router Configuration
# =========================================================
router = APIRouter(prefix="/api/tds-challans", tags=["TDS Challans"])

# =========================================================
# CREATE
# =========================================================
@router.post("/", response_model=schemas.TDSChallan)
def create_tds_challan(
    challan: schemas.TDSChallanCreate,
    db: Session = Depends(get_db)
):
    """Create a new TDS Challan record."""
    return service.create_tds_challan(db, challan)

# =========================================================
# READ ALL
# =========================================================
@router.get("/", response_model=List[schemas.TDSChallan])
def get_all_tds_challans(db: Session = Depends(get_db)):
    """Fetch all TDS Challans."""
    return service.get_tds_challans(db)

# =========================================================
# READ BY ID
# =========================================================
@router.get("/{challan_id}", response_model=schemas.TDSChallan)
def get_tds_challan_by_id(
    challan_id: int,
    db: Session = Depends(get_db)
):
    """Fetch a specific TDS Challan by ID."""
    challan = service.get_tds_challan_by_id(db, challan_id)
    if not challan:
        raise HTTPException(status_code=404, detail="TDS Challan not found")
    return challan

# =========================================================
# UPDATE
# =========================================================
@router.put("/{challan_id}", response_model=schemas.TDSChallan)
def update_tds_challan(
    challan_id: int,
    updated_challan: schemas.TDSChallanCreate,
    db: Session = Depends(get_db)
):
    """Update an existing TDS Challan record."""
    challan = service.update_tds_challan(db, challan_id, updated_challan)
    if not challan:
        raise HTTPException(status_code=404, detail="TDS Challan not found")
    return challan

# =========================================================
# DELETE
# =========================================================
@router.delete("/{challan_id}", response_model=dict)
def delete_tds_challan(
    challan_id: int,
    db: Session = Depends(get_db)
):
    """Delete a TDS Challan record by ID."""
    success = service.delete_tds_challan(db, challan_id)
    if not success:
        raise HTTPException(status_code=404, detail="TDS Challan not found")
    return {"detail": "TDS Challan deleted successfully"}
