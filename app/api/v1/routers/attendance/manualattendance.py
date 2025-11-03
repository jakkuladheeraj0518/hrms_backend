from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.models.attendance import ManualAttendance
from app.schemas.attendance_schema import ManualAttendanceOut, ManualAttendanceCreate

router = APIRouter(
    prefix="/attendance/manual",
    tags=["manualattendance"]
)

@router.post("/", response_model=ManualAttendanceOut, status_code=status.HTTP_201_CREATED)
def create_manual(data: ManualAttendanceCreate, db: Session = Depends(get_db)):
    record = ManualAttendance(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[ManualAttendanceOut])
def get_manuals(db: Session = Depends(get_db)):
    return db.query(ManualAttendance).all()
