from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from typing import List, Optional
from app.schemas.bulk_updatesschemas import EmployeeBankResponse, EmployeeBankCreate
from app.services.bulk_updatesservices import EmployeeBankService

router = APIRouter(prefix="/bank", tags=["Employee Bank Details"])


# 🟢 1. Get All Employees and Bank Details
@router.get("/", response_model=List[EmployeeBankResponse])
async def get_all_employee_bank_details(
    business_unit_id: Optional[int] = Query(None),
    location_id: Optional[int] = Query(None),
    department_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await EmployeeBankService.get_all_employee_bank_details(
        db, business_unit_id, location_id, department_id
    )


# 🟢 2. Update or Create Employee Bank Details
@router.post("/update")
async def update_employee_bank_details(
    updates: List[EmployeeBankCreate],
    db: AsyncSession = Depends(get_db),
):
    return await EmployeeBankService.update_employee_bank_details(updates, db)


# 🟢 3. Get Employees for Dropdown
@router.get("/employees")
async def get_employees(db: AsyncSession = Depends(get_db)):
    return await EmployeeBankService.get_employees_for_dropdown(db)
