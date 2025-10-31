from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.request_service import MissedPunchRequestService
from app.schemas.request_schema import (
    MissedPunchRequest, MissedPunchRequestCreate, StatusUpdate, DeleteResponse
)

router = APIRouter(
    prefix="/missed-punch-requests",
    tags=["Missed Punch Requests"]
)

# Initialize service
missed_punch_service = MissedPunchRequestService()

@router.post("/", response_model=MissedPunchRequest)
def create_missed_punch_request(
    request: MissedPunchRequestCreate,
    db: Session = Depends(get_db)
):
    """Create a new missed punch request"""
    return missed_punch_service.create_missed_punch_request(db, request)

@router.get("/", response_model=List[MissedPunchRequest])
def get_missed_punch_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all missed punch requests"""
    return missed_punch_service.get_all(db, skip, limit)

@router.get("/{request_id}", response_model=MissedPunchRequest)
def get_missed_punch_request(request_id: int, db: Session = Depends(get_db)):
    """Get a specific missed punch request by ID"""
    return missed_punch_service.get(db, request_id)

@router.patch("/{request_id}/status", response_model=MissedPunchRequest)
def update_request_status(
    request_id: int,
    status_update: StatusUpdate,
    db: Session = Depends(get_db)
):
    """Update the status of a missed punch request"""
    return missed_punch_service.update_status(db, request_id, status_update.status)

@router.delete("/{request_id}", response_model=DeleteResponse)
def delete_missed_punch_request(request_id: int, db: Session = Depends(get_db)):
    """Delete a missed punch request"""
    return missed_punch_service.delete(db, request_id)



