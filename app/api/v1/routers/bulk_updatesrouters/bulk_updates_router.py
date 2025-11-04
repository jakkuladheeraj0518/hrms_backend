from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.bulk_updatesservices import BulkUpdatesService
from app.schemas.bulk_updatesschemas import BulkUpdateRequest, BulkUpdateResponse

router = APIRouter(prefix="/bulk-updates", tags=["Bulk Updates"])


# @router.get("/metadata")
# async def get_metadata(session: AsyncSession = Depends(get_db)):
#     return await BulkUpdatesService.get_metadata(session)


@router.post("/apply", response_model=BulkUpdateResponse)
async def apply_bulk_update(payload: BulkUpdateRequest, session: AsyncSession = Depends(get_db)):
    return await BulkUpdatesService.apply_bulk_update(payload, session)
