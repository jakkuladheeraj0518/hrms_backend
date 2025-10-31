from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.request_service import StrikeExemptionRequestService
from app.schemas.request_schema import (
    StrikeExemptionRequest, StrikeExemptionRequestCreate, StatusUpdate, DeleteResponse
)

router = APIRouter(
    prefix="/strike-exemption-requests",
    tags=["Strike Exemption Requests"]
)

strike_service = StrikeExemptionRequestService()

@router.post("/", response_model=StrikeExemptionRequest)
def create_strike_exemption_request(request: StrikeExemptionRequestCreate, db: Session = Depends(get_db)):
    return strike_service.create_strike_exemption_request(db, request)

@router.get("/", response_model=List[StrikeExemptionRequest])
def get_strike_exemption_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return strike_service.get_all(db, skip, limit)

@router.get("/{request_id}", response_model=StrikeExemptionRequest)
def get_strike_exemption_request(request_id: int, db: Session = Depends(get_db)):
    return strike_service.get(db, request_id)

@router.patch("/{request_id}/status", response_model=StrikeExemptionRequest)
def update_request_status(request_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    return strike_service.update_status(db, request_id, status_update.status)

@router.delete("/{request_id}", response_model=DeleteResponse)
def delete_strike_exemption_request(request_id: int, db: Session = Depends(get_db)):
    return strike_service.delete(db, request_id)



