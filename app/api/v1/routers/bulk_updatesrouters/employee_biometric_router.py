from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.services.bulk_updatesservices import EmployeeBiometricService
from app.schemas.bulk_updatesschemas import EmployeeBiometricOut, EmployeeBiometricCreate, EmployeeBiometricUpdate

router = APIRouter(prefix="/employee-biometric", tags=["Employee Biometric"])


@router.get("/", response_model=List[EmployeeBiometricOut])
async def list_biometric_codes(
    business_unit_id: Optional[int] = Query(None),
    location_id: Optional[int] = Query(None),
    cost_center_id: Optional[int] = Query(None),
    department_id: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_db),
):
    return await EmployeeBiometricService.list_biometrics(
        session=session,
        business_unit_id=business_unit_id,
        location_id=location_id,
        cost_center_id=cost_center_id,
        department_id=department_id,
    )


@router.post("/", response_model=EmployeeBiometricOut)
async def create_biometric(data: EmployeeBiometricCreate, session: AsyncSession = Depends(get_db)):
    return await EmployeeBiometricService.create_biometric(data, session)


@router.put("/{employee_id}", response_model=EmployeeBiometricOut)
async def update_biometric(employee_id: int, data: EmployeeBiometricUpdate, session: AsyncSession = Depends(get_db)):
    return await EmployeeBiometricService.update_biometric(employee_id, data, session)
