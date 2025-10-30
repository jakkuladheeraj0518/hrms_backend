from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from app.database.session import get_db

from app.schemas import datacapture_schema as schemas
from app.services import datacapture_service as service

router = APIRouter(prefix="/api/datacapture/deductions", tags=["Deduction Variables"])


# =========================================================
# Upload CSV and bulk insert
# =========================================================
@router.post("/upload")
def upload_deduction_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a CSV file to bulk insert Deduction Variable records.
    Expected columns: employee_name, employee_code, location, department, business_unit,
    source_component, target_component, start_date, end_date, amount, comments, total, month
    """
    try:
        df = pd.read_csv(file.file, encoding="utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {e}")

    saved_ids = []

    for _, row in df.iterrows():
        row = row.fillna("")

        if not row.get("employee_name") or not row.get("month"):
            continue

        deduction_data = schemas.DeductionVariableCreate(
            employee_name=str(row.get("employee_name")),
            employee_code=str(row.get("employee_code")),
            location=str(row.get("location", "")),
            department=str(row.get("department", "")),
            business_unit=str(row.get("business_unit", "")),
            source_component=str(row.get("source_component", "")),
            target_component=str(row.get("target_component", "")),
            start_date=pd.to_datetime(row.get("start_date"), errors="coerce").date()
            if pd.notna(pd.to_datetime(row.get("start_date"), errors="coerce")) else None,
            end_date=pd.to_datetime(row.get("end_date"), errors="coerce").date()
            if pd.notna(pd.to_datetime(row.get("end_date"), errors="coerce")) else None,
            amount=float(row.get("amount", 0)),
            comments=str(row.get("comments", "")),
            total=float(row.get("total", 0)),
            month=str(row.get("month"))
        )

        db_deduction = service.create_deduction_variable(db, deduction_data)
        saved_ids.append(db_deduction.id)

    return {
        "message": f"{len(saved_ids)} deduction records inserted successfully",
        "ids": saved_ids
    }


# =========================================================
# Create single deduction record
# =========================================================
@router.post("/", response_model=schemas.DeductionVariable)
def create_deduction(deduction: schemas.DeductionVariableCreate, db: Session = Depends(get_db)):
    """Create a new single Deduction Variable record"""
    db_deduction = service.create_deduction_variable(db, deduction)
    return db_deduction


# =========================================================
# Get all deduction records
# =========================================================
@router.get("/", response_model=list[schemas.DeductionVariable])
def get_deductions(db: Session = Depends(get_db)):
    """Retrieve all Deduction Variable records"""
    return service.get_deduction_variables(db)


# =========================================================
# Get deduction by ID
# =========================================================
@router.get("/{deduction_id}", response_model=schemas.DeductionVariable)
def get_deduction_by_id(deduction_id: int, db: Session = Depends(get_db)):
    """Retrieve a single Deduction Variable by ID"""
    deduction = service.get_deduction_variable_by_id(db, deduction_id)
    if not deduction:
        raise HTTPException(status_code=404, detail="Deduction variable not found")
    return deduction


# =========================================================
# Update record
# =========================================================
@router.put("/{deduction_id}", response_model=schemas.DeductionVariable)
def update_deduction(deduction_id: int, deduction: schemas.DeductionVariableCreate, db: Session = Depends(get_db)):
    """Update a Deduction Variable record"""
    db_deduction = service.update_deduction_variable(db, deduction_id, deduction)
    if not db_deduction:
        raise HTTPException(status_code=404, detail="Deduction variable not found")
    return db_deduction


# =========================================================
# Delete record
# =========================================================
@router.delete("/{deduction_id}")
def delete_deduction(deduction_id: int, db: Session = Depends(get_db)):
    """Delete a Deduction Variable record"""
    deleted = service.delete_deduction_variable(db, deduction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Deduction variable not found")
    return {"message": f"Deduction variable with ID {deduction_id} deleted successfully"}
