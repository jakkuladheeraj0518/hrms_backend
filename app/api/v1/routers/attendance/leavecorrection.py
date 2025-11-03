from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.models.attendance import LeaveCorrection
from app.schemas.attendance_schema import LeaveCorrectionOut, LeaveCorrectionCreate

router = APIRouter(
    prefix="/attendance/leavecorrection",
    tags=["leavecorrection"]
)

@router.post("/", response_model=LeaveCorrectionOut, status_code=status.HTTP_201_CREATED)
def create_leave(data: LeaveCorrectionCreate, db: Session = Depends(get_db)):
    leave = LeaveCorrection(**data.model_dump())
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave

@router.get("/", response_model=List[LeaveCorrectionOut])
def get_leaves(db: Session = Depends(get_db)):
    return db.query(LeaveCorrection).all()

@router.put("/{id}", response_model=LeaveCorrectionOut)
def update_leave(id: int, data: LeaveCorrectionCreate, db: Session = Depends(get_db)):
    leave = db.query(LeaveCorrection).filter_by(id=id).first()
    if not leave:
        raise HTTPException(404, "Leave not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(leave, k, v)
    db.commit()
    db.refresh(leave)
    return leave
