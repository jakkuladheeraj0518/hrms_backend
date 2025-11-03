from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.models.attendance import DailyAttendance
from app.schemas.attendance_schema import DailyAttendanceOut, DailyAttendanceCreate, DailyAttendanceUpdate

router = APIRouter(
    prefix="/attendance/daily",
    tags=["dailyattendance"]
)

@router.post("/", response_model=DailyAttendanceOut, status_code=status.HTTP_201_CREATED)
def create_daily_attendance(data: DailyAttendanceCreate, db: Session = Depends(get_db)):
    record = DailyAttendance(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[DailyAttendanceOut])
def get_all_attendance(db: Session = Depends(get_db)):
    return db.query(DailyAttendance).all()

@router.get("/{employee_code}", response_model=List[DailyAttendanceOut])
def get_employee_attendance(employee_code: str, db: Session = Depends(get_db)):
    return db.query(DailyAttendance).filter_by(employee_code=employee_code).all()

@router.put("/{id}", response_model=DailyAttendanceOut)
def update_attendance(id: int, data: DailyAttendanceUpdate, db: Session = Depends(get_db)):
    record = db.query(DailyAttendance).filter_by(id=id).first()
    if not record:
        raise HTTPException(404, "Record not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(record, k, v)
    db.commit()
    db.refresh(record)
    return record
