from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.request_service import ShiftRosterService
from app.schemas.request_schema import (
    ShiftRoster, ShiftRosterCreate, DeleteResponse
)

router = APIRouter(
    prefix="/shift-rosters",
    tags=["Shift Rosters"]
)

shift_roster_service = ShiftRosterService()

@router.post("/", response_model=ShiftRoster)
def create_shift_roster(request: ShiftRosterCreate, db: Session = Depends(get_db)):
    return shift_roster_service.create_shift_roster(db, request)

@router.get("/", response_model=List[ShiftRoster])
def get_shift_rosters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return shift_roster_service.get_all(db, skip, limit)

@router.get("/{roster_id}", response_model=ShiftRoster)
def get_shift_roster(roster_id: int, db: Session = Depends(get_db)):
    return shift_roster_service.get(db, roster_id)

@router.delete("/{roster_id}", response_model=DeleteResponse)
def delete_shift_roster(roster_id: int, db: Session = Depends(get_db)):
    return shift_roster_service.delete(db, roster_id)



