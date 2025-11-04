# routers/salary_deductions_router.py
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.bulk_updatesschemas import SalaryDeductionCreate, SalaryDeductionOut, SalaryDeductionBase
from app.services.bulk_updatesservices import SalaryDeductionsService

router = APIRouter(prefix="/salary-deductions", tags=["Salary Deductions"])


@router.get("/", response_model=List[SalaryDeductionOut])
async def list_salary_deductions(
    business_unit_id: Optional[int] = Query(None),
    location_id: Optional[int] = Query(None),
    cost_center_id: Optional[int] = Query(None),
    department_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await SalaryDeductionsService.list_salary_deductions(
        db, business_unit_id, location_id, cost_center_id, department_id
    )


@router.post("/create_salary_deduction", response_model=SalaryDeductionOut)
async def create_salary_deduction(payload: SalaryDeductionCreate, db: AsyncSession = Depends(get_db)):
    return await SalaryDeductionsService.create_salary_deduction(db, payload)


@router.put("/{deduction_id}", response_model=SalaryDeductionOut)
async def update_salary_deduction(
    deduction_id: int,
    payload: SalaryDeductionBase,
    db: AsyncSession = Depends(get_db),
):
    return await SalaryDeductionsService.update_salary_deduction(db, deduction_id, payload)
