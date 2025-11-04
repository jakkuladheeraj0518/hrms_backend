from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.bulk_updatesschemas import EmployeeWorkProfileOut
from app.services.bulk_updatesservices import WorkProfileService

router = APIRouter(prefix="/work-profiles", tags=["Work Profiles"])


@router.get("/", response_model=List[EmployeeWorkProfileOut])
async def list_work_profiles(
    business_unit_id: Optional[int] = Query(None),
    location_id: Optional[int] = Query(None),
    cost_center_id: Optional[int] = Query(None),
    department_id: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_db),
):
    """
    Fetch all employees with their work profile info.
    Optionally filter by business unit, location, cost center, or department.
    """
    return await WorkProfileService.list_work_profiles(
        session=session,
        business_unit_id=business_unit_id,
        location_id=location_id,
        cost_center_id=cost_center_id,
        department_id=department_id,
    )
