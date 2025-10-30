from sqlalchemy.orm import Session
from app.models.payroll_models import PayrollPeriod
from app.schemas.payroll_schemas import PayrollPeriodCreate

def get_all_periods(db: Session):
    return db.query(PayrollPeriod).all()

def create_period(db: Session, period: PayrollPeriodCreate):
    new_period = PayrollPeriod(**period.dict())
    db.add(new_period)
    db.commit()
    db.refresh(new_period)
    return new_period
