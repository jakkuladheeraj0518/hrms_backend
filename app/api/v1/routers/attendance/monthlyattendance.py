from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.models.attendance import MonthlyAttendance
from app.schemas.attendance_schema import MonthlyAttendanceOut, MonthlyAttendanceCreate

router = APIRouter(
    prefix="/attendance/monthly",
    tags=["monthlyattendance"]
)

@router.post("/", response_model=MonthlyAttendanceOut, status_code=status.HTTP_201_CREATED)
def create_monthly(data: MonthlyAttendanceCreate, db: Session = Depends(get_db)):
    record = MonthlyAttendance(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[MonthlyAttendanceOut])
def get_all_monthly(db: Session = Depends(get_db)):
    return db.query(MonthlyAttendance).all()
