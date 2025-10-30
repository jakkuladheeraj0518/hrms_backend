from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from typing import List
from app.database.session import get_db

from app.schemas import datacapture_schema as schemas
from app.services import datacapture_service as service

router = APIRouter(prefix="/api/datacapture/salary", tags=["Salary Variable"])

# =========================================================
# BULK UPLOAD FROM CSV
# =========================================================
@router.post("/upload")
def upload_salary_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a CSV file and bulk insert Salary Variable records"""
    try:
        df = pd.read_csv(file.file, encoding="utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {e}")

    saved_ids = []

    for _, row in df.iterrows():
        row = row.fillna("")

        if not row.get("employee_name") or not row.get("month"):
            continue

        salary_data = schemas.SalaryVariableCreate(
            employee_name=str(row.get("employee_name")),
            employee_code=str(row.get("employee_code", "")),
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

        db_salary = service.create_salary_variable(db, salary_data)
        saved_ids.append(db_salary.id)

    return {
        "message": f"{len(saved_ids)} salary records inserted successfully",
        "ids": saved_ids
    }


# =========================================================
# CREATE SINGLE RECORD
# =========================================================
@router.post("/", response_model=schemas.SalaryVariableBase)
def create_salary(salary: schemas.SalaryVariableCreate, db: Session = Depends(get_db)):
    """Create a new Salary Variable record"""
    return service.create_salary_variable(db, salary)


# =========================================================
# READ ALL RECORDS
# =========================================================
@router.get("/", response_model=List[schemas.SalaryVariableBase])
def get_salaries(db: Session = Depends(get_db)):
    """Retrieve all Salary Variable records"""
    return service.get_salary_variables(db)


# =========================================================
# READ ONE RECORD BY ID
# =========================================================
@router.get("/{salary_id}", response_model=schemas.SalaryVariableBase)
def get_salary_by_id(salary_id: int, db: Session = Depends(get_db)):
    """Retrieve a Salary Variable record by ID"""
    salary = service.get_salary_variable_by_id(db, salary_id)
    if not salary:
        raise HTTPException(status_code=404, detail=f"Salary record with ID {salary_id} not found")
    return salary


# =========================================================
# UPDATE RECORD
# =========================================================
@router.put("/{salary_id}", response_model=schemas.SalaryVariableBase)
def update_salary(salary_id: int, salary_update: schemas.SalaryVariableCreate, db: Session = Depends(get_db)):
    """Update an existing Salary Variable record"""
    updated = service.update_salary_variable(db, salary_id, salary_update)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Salary record with ID {salary_id} not found")
    return updated


# =========================================================
# DELETE RECORD
# =========================================================
@router.delete("/{salary_id}")
def delete_salary(salary_id: int, db: Session = Depends(get_db)):
    """Delete a Salary Variable record"""
    success = service.delete_salary_variable(db, salary_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Salary record with ID {salary_id} not found")
    return {"detail": f"Salary record with ID {salary_id} deleted successfully"}
