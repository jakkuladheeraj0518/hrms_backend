from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.models.attendance import AttendanceEmployee
from app.schemas.attendance_schema import (
    AttendanceEmployeeOut,
    AttendanceEmployeeCreate,
    AttendanceEmployeeUpdate,
)

router = APIRouter(
    prefix="/attendance/employee",
    tags=["attendanceemployee"]
)

@router.post("/", response_model=AttendanceEmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(employee: AttendanceEmployeeCreate, db: Session = Depends(get_db)):
    new_emp = AttendanceEmployee(**employee.model_dump())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

@router.get("/", response_model=List[AttendanceEmployeeOut])
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(AttendanceEmployee).all()

@router.get("/{employee_code}", response_model=AttendanceEmployeeOut)
def get_employee(employee_code: str, db: Session = Depends(get_db)):
    emp = db.query(AttendanceEmployee).filter_by(employee_code=employee_code).first()
    if not emp:
        raise HTTPException(404, "Employee not found")
    return emp

@router.put("/{employee_code}", response_model=AttendanceEmployeeOut)
def update_employee(employee_code: str, data: AttendanceEmployeeUpdate, db: Session = Depends(get_db)):
    emp = db.query(AttendanceEmployee).filter_by(employee_code=employee_code).first()
    if not emp:
        raise HTTPException(404, "Employee not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(emp, k, v)
    db.commit()
    db.refresh(emp)
    return emp

@router.delete("/{employee_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_code: str, db: Session = Depends(get_db)):
    emp = db.query(AttendanceEmployee).filter_by(employee_code=employee_code).first()
    if not emp:
        raise HTTPException(404, "Employee not found")
    db.delete(emp)
    db.commit()
