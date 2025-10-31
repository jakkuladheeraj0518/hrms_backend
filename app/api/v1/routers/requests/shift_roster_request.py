from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.request_service import ShiftRosterRequestService
from app.schemas.request_schema import (
    ShiftRosterRequest, ShiftRosterRequestCreate, StatusUpdate, DeleteResponse
)

router = APIRouter(
    prefix="/shift-roster-requests",
    tags=["Shift Roster Requests"]
)

shift_roster_service = ShiftRosterRequestService()

@router.post("/", response_model=ShiftRosterRequest)
def create_shift_roster_request(request: ShiftRosterRequestCreate, db: Session = Depends(get_db)):
    return shift_roster_service.create_shift_roster_request(db, request)

@router.get("/", response_model=List[ShiftRosterRequest])
def get_shift_roster_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return shift_roster_service.get_all(db, skip, limit)

@router.get("/{request_id}", response_model=ShiftRosterRequest)
def get_shift_roster_request(request_id: int, db: Session = Depends(get_db)):
    return shift_roster_service.get(db, request_id)

@router.patch("/{request_id}/status", response_model=ShiftRosterRequest)
def update_request_status(request_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
    return shift_roster_service.update_status(db, request_id, status_update.status)

@router.delete("/{request_id}", response_model=DeleteResponse)
def delete_shift_roster_request(request_id: int, db: Session = Depends(get_db)):
    return shift_roster_service.delete(db, request_id)



