from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
from typing import Optional, List
from datetime import date, datetime
from app.api.deps import get_db
from app.models.attendance import DailyPunch
from app.schemas.attendance_schema import DailyPunchOut

router = APIRouter(
    prefix="/attendance/punch",
    tags=["dailypunch"]
)

@router.get("/", response_model=List[DailyPunchOut])
def get_punches(date_str: date = Query(...), employee_code: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(DailyPunch).filter(cast(DailyPunch.punch_time, Date) == date_str)
    if employee_code:
        query = query.filter(DailyPunch.employee_code == employee_code)
    punches = query.all()
    return [
        {
            **p.__dict__,
            "formatted_punch_time": p.punch_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for p in punches
    ]

@router.post("/", response_model=DailyPunchOut, status_code=status.HTTP_201_CREATED)
def create_punch(employee_code: str = Query(...),
                 punch_time: datetime = Query(...),
                 punch_type: Optional[str] = None,
                 remarks: Optional[str] = None,
                 db: Session = Depends(get_db)):
    punch = DailyPunch(employee_code=employee_code, punch_time=punch_time, punch_type=punch_type, remarks=remarks)
    db.add(punch)
    db.commit()
    db.refresh(punch)
    return {
        **punch.__dict__,
        "formatted_punch_time": punch.punch_time.strftime("%Y-%m-%d %H:%M:%S"),
    }
