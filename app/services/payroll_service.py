from sqlalchemy.orm import Session
from app.repositories.payroll_repository import create_period

def create_payroll_period(db: Session, period):
    return create_period(db, period)
