from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.payroll_models import PayrollPeriod
from app.schemas.payroll_schemas import PayrollPeriodCreate, PayrollPeriodUpdate, PayrollPeriodResponse

router = APIRouter(prefix="/api/payroll-periods", tags=["Payroll Periods"])

@router.get("/", response_model=List[PayrollPeriodResponse])
def get_periods(db: Session = Depends(get_db)):
    return db.query(PayrollPeriod).order_by(PayrollPeriod.id.desc()).all()

@router.get("/{period_id}", response_model=PayrollPeriodResponse)
def get_period(period_id: int, db: Session = Depends(get_db)):
    period = db.query(PayrollPeriod).filter(PayrollPeriod.id == period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    return period

@router.post("/", response_model=PayrollPeriodResponse, status_code=status.HTTP_201_CREATED)
def create_period(period: PayrollPeriodCreate, db: Session = Depends(get_db)):
    existing = db.query(PayrollPeriod).filter(PayrollPeriod.name == period.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Payroll period with this name already exists")
    db_period = PayrollPeriod(**period.dict())
    db.add(db_period)
    db.commit()
    db.refresh(db_period)
    return db_period

@router.put("/{period_id}", response_model=PayrollPeriodResponse)
def update_period(period_id: int, period_update: PayrollPeriodUpdate, db: Session = Depends(get_db)):
    period = db.query(PayrollPeriod).filter(PayrollPeriod.id == period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    for key, value in period_update.dict(exclude_unset=True).items():
        setattr(period, key, value)
    db.commit()
    db.refresh(period)
    return period

@router.delete("/{period_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_period(period_id: int, db: Session = Depends(get_db)):
    period = db.query(PayrollPeriod).filter(PayrollPeriod.id == period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    db.delete(period)
    db.commit()
    return None

@router.patch("/{period_id}/reporting", response_model=PayrollPeriodResponse)
def toggle_reporting(period_id: int, db: Session = Depends(get_db)):
    period = db.query(PayrollPeriod).filter(PayrollPeriod.id == period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    period.is_reporting_enabled = not period.is_reporting_enabled
    db.commit()
    db.refresh(period)
    return period

@router.patch("/{period_id}/status", response_model=PayrollPeriodResponse)
def update_status(period_id: int, status: str, db: Session = Depends(get_db)):
    period = db.query(PayrollPeriod).filter(PayrollPeriod.id == period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Period not found")
    period.status = status
    db.commit()
    db.refresh(period)
    return period
