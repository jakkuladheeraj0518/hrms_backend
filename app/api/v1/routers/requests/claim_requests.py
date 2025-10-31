from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.request_service import ClaimRequestService
from app.schemas.request_schema import (
    ClaimRequest, ClaimRequestCreate, StatusUpdate, DeleteResponse
)

router = APIRouter(
    prefix="/claim-requests",
    tags=["Claim Requests"]
)

claim_service = ClaimRequestService()

@router.post("/", response_model=ClaimRequest)
def create_claim_request(request: ClaimRequestCreate, db: Session = Depends(get_db)):
    return claim_service.create_claim_request(db, request)

@router.get("/", response_model=List[ClaimRequest])
def get_claim_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return claim_service.get_all(db, skip, limit)

@router.get("/{request_id}", response_model=ClaimRequest)
def get_claim_request(request_id: int, db: Session = Depends(get_db)):
    return claim_service.get(db, request_id)

@router.patch("/{request_id}/status", response_model=ClaimRequest)
def update_request_status(request_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    return claim_service.update_status(db, request_id, status_update.status)

@router.delete("/{request_id}", response_model=DeleteResponse)
def delete_claim_request(request_id: int, db: Session = Depends(get_db)):
    return claim_service.delete(db, request_id)



