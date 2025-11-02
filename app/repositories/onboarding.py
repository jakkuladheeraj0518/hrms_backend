from sqlalchemy.orm import Session
from app.models.onboarding import Employees, Candidate, BulkCandidate, OfferLetter, OnboardingCandidate, OnboardingForm, OfferLetterForm, OfferLetterTemplate, FinalizedForm
from app.schemas.onboarding import EmployeeCreate, EmployeeUpdate

def create_employee(db: Session, payload: EmployeeCreate):
    emp = Employees(**payload.dict())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

def get_employee_by_email(db: Session, email: str):
    return db.query(Employees).filter(Employees.email == email).first()

def get_employee(db: Session, emp_id: int):
    return db.query(Employees).filter(Employees.id == emp_id).first()

def list_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Employees).offset(skip).limit(limit).all()

def update_employee(db: Session, emp_id: int, changes: EmployeeUpdate):
    emp = get_employee(db, emp_id)
    if not emp:
        return None
    for k, v in changes.dict(exclude_unset=True).items():
        setattr(emp, k, v)
    db.commit()
    db.refresh(emp)
    return emp

def approve_employee(db: Session, emp):
    emp.approved = True
    db.commit()
    db.refresh(emp)
    return emp

# Candidate CRUD (simplified)
def create_candidate(db: Session, payload):
    c = Candidate(**payload.dict())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

def get_candidate(db: Session, candidate_id: int):
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()

def list_bulk_candidates(db: Session):
    return db.query(BulkCandidate).order_by(BulkCandidate.created_at.desc()).all()
