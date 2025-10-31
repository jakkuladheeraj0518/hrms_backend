from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.request_service import WeekOffRosterRequestService
from app.schemas.request_schema import (
    WeekOffRosterRequest, WeekOffRosterRequestCreate, StatusUpdate, DeleteResponse
)

router = APIRouter(
    prefix="/weekoff-roster-requests",
    tags=["Week Off Roster Requests"]
)

weekoff_service = WeekOffRosterRequestService()

@router.post("/", response_model=WeekOffRosterRequest)
def create_weekoff_roster_request(request: WeekOffRosterRequestCreate, db: Session = Depends(get_db)):
    return weekoff_service.create_weekoff_roster_request(db, request)

@router.get("/", response_model=List[WeekOffRosterRequest])
def get_weekoff_roster_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return weekoff_service.get_all(db, skip, limit)

@router.get("/{request_id}", response_model=WeekOffRosterRequest)
def get_weekoff_roster_request(request_id: int, db: Session = Depends(get_db)):
    return weekoff_service.get(db, request_id)

@router.patch("/{request_id}/status", response_model=WeekOffRosterRequest)
def update_request_status(request_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    return weekoff_service.update_status(db, request_id, status_update.status)

@router.delete("/{request_id}", response_model=DeleteResponse)
def delete_weekoff_roster_request(request_id: int, db: Session = Depends(get_db)):
    return weekoff_service.delete(db, request_id)



