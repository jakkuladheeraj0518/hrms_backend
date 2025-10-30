from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.payroll_models import Employee, HoldSalary
from app.schemas.payroll_schemas import HoldSalaryCreate, HoldSalaryOut, EmployeeResponse

router = APIRouter(prefix="/api/hold-salary", tags=["Hold Salary"])

@router.get("/employees/", response_model=List[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).filter(Employee.is_active == True).all()
    return employees

@router.post("/", response_model=HoldSalaryOut, status_code=status.HTTP_201_CREATED)
def create_hold_salary(request: HoldSalaryCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == request.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    new_record = HoldSalary(employee_id=request.employee_id, hold_from=request.hold_from, hold_reason=request.hold_reason)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return HoldSalaryOut(id=new_record.id, employee_name=employee.name, hold_from=new_record.hold_from, hold_reason=new_record.hold_reason)

@router.get("/", response_model=List[HoldSalaryOut])
def get_all_hold_salaries(db: Session = Depends(get_db)):
    records = db.query(HoldSalary).all()
    response = []
    for rec in records:
        emp = db.query(Employee).filter(Employee.id == rec.employee_id).first()
        response.append(HoldSalaryOut(id=rec.id, employee_name=emp.name if emp else "Unknown", hold_from=rec.hold_from, hold_reason=rec.hold_reason))
    return response

@router.delete("/{hold_id}")
def delete_hold_salary(hold_id: int, db: Session = Depends(get_db)):
    record = db.query(HoldSalary).filter(HoldSalary.id == hold_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(record)
    db.commit()
    return {"message": "Hold salary record deleted successfully"}
