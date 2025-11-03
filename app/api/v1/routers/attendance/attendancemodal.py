from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.models.attendance import AttendanceModal
from app.schemas.attendance_schema import AttendanceModalOut, AttendanceModalCreate

router = APIRouter(
    prefix="/attendance/modal",
    tags=["attendancemodal"]
)

@router.post("/", response_model=AttendanceModalOut, status_code=status.HTTP_201_CREATED)
def create_modal(data: AttendanceModalCreate, db: Session = Depends(get_db)):
    modal = AttendanceModal(**data.model_dump())
    db.add(modal)
    db.commit()
    db.refresh(modal)
    return modal

@router.get("/", response_model=List[AttendanceModalOut])
def get_all_modals(db: Session = Depends(get_db)):
    return db.query(AttendanceModal).all()

@router.get("/{employee_code}/{year}/{month}", response_model=List[AttendanceModalOut])
def get_modals_by_employee(employee_code: str, year: int, month: int, db: Session = Depends(get_db)):
    return (
        db.query(AttendanceModal)
        .filter(AttendanceModal.employee_code == employee_code)
        .filter(db.extract("year", AttendanceModal.date) == year)
        .filter(db.extract("month", AttendanceModal.date) == month)
        .all()
    )
