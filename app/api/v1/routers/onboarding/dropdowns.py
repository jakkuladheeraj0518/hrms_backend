from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.onboarding import (
    Location,
    Department,
    CostCenter,
    Grade,
    Designation,
    ShiftPolicy,
    WeekOffPolicy,
)
from app.schemas.onboarding import (
    LocationBase,
    DepartmentBase,
    CostCenterBase,
    GradeBase,
    DesignationBase,
    ShiftPolicyBase,
    WeekOffPolicyBase,
)

router = APIRouter(prefix="/dropdowns", tags=["Dropdowns"])

@router.get("/locations", response_model=list[LocationBase])
def get_locations(db: Session = Depends(get_db)):
    return db.query(Location).all()

@router.get("/departments", response_model=list[DepartmentBase])
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()

@router.get("/costcenters", response_model=list[CostCenterBase])
def get_costcenters(db: Session = Depends(get_db)):
    return db.query(CostCenter).all()

@router.get("/grades", response_model=list[GradeBase])
def get_grades(db: Session = Depends(get_db)):
    return db.query(Grade).all()

@router.get("/designations", response_model=list[DesignationBase])
def get_designations(db: Session = Depends(get_db)):
    return db.query(Designation).all()

@router.get("/shiftpolicies", response_model=list[ShiftPolicyBase])
def get_shiftpolicies(db: Session = Depends(get_db)):
    return db.query(ShiftPolicy).all()

@router.get("/weekoffpolicies", response_model=list[WeekOffPolicyBase])
def get_weekoffpolicies(db: Session = Depends(get_db)):
    return db.query(WeekOffPolicy).all()
