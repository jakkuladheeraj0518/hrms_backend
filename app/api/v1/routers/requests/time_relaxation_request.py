from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.request_service import TimeRelaxationRequestService
from app.schemas.request_schema import (
    TimeRelaxationRequest, TimeRelaxationRequestCreate, StatusUpdate, DeleteResponse
)

router = APIRouter(
    prefix="/time-relaxation-requests",
    tags=["Time Relaxation Requests"]
)

time_relaxation_service = TimeRelaxationRequestService()

@router.post("/", response_model=TimeRelaxationRequest)
def create_time_relaxation_request(request: TimeRelaxationRequestCreate, db: Session = Depends(get_db)):
    return time_relaxation_service.create_time_relaxation_request(db, request)

@router.get("/", response_model=List[TimeRelaxationRequest])
def get_time_relaxation_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return time_relaxation_service.get_all(db, skip, limit)

@router.get("/{request_id}", response_model=TimeRelaxationRequest)
def get_time_relaxation_request(request_id: int, db: Session = Depends(get_db)):
    return time_relaxation_service.get(db, request_id)

@router.patch("/{request_id}/status", response_model=TimeRelaxationRequest)
def update_request_status(request_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    return time_relaxation_service.update_status(db, request_id, status_update.status)

@router.delete("/{request_id}", response_model=DeleteResponse)
def delete_time_relaxation_request(request_id: int, db: Session = Depends(get_db)):
    return time_relaxation_service.delete(db, request_id)



