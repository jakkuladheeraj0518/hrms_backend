# routers/salary_revision_router.py
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
import app.schemas.bulk_updatesschemas as schemas
from app.services.bulk_updatesservices import SalaryRevisionService

router = APIRouter(prefix="/salary-revision", tags=["Salary Revision"])


@router.get("/", response_model=List[schemas.SalaryRevisionOut])
async def get_all_salaries(
    db: AsyncSession = Depends(get_db),
    business_unit: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
):
    return await SalaryRevisionService.get_all_salaries(
        db, business_unit, location, department
    )


@router.post("/", response_model=schemas.SalaryRevisionOut)
async def create_or_update_salary(
    salary: schemas.SalaryRevisionCreate,
    db: AsyncSession = Depends(get_db),
):
    return await SalaryRevisionService.create_or_update_salary(db, salary)
