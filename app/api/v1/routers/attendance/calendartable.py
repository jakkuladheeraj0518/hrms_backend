from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.models.attendance import CalendarTable
from app.schemas.attendance_schema import CalendarTableCreate, CalendarTableOut

router = APIRouter(
    prefix="/attendance/calendar",
    tags=["calendartable"]
)

@router.post("/", response_model=CalendarTableOut, status_code=status.HTTP_201_CREATED)
def create_calendar_entry(data: CalendarTableCreate, db: Session = Depends(get_db)):
    entry = CalendarTable(**data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.get("/", response_model=List[CalendarTableOut])
def list_calendar_entries(db: Session = Depends(get_db)):
    return db.query(CalendarTable).all()

@router.get("/{id}", response_model=CalendarTableOut)
def get_calendar_entry(id: int, db: Session = Depends(get_db)):
    entry = db.query(CalendarTable).filter_by(id=id).first()
    if not entry:
        raise HTTPException(404, "Entry not found")
    return entry
