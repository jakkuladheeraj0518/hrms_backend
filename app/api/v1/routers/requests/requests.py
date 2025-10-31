from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.request_service import EmployeeService
from app.schemas.request_schema import Employee, EmployeeCreate, DeleteResponse

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

employee_service = EmployeeService()

@router.post("/", response_model=Employee)
def create_employee(request: EmployeeCreate, db: Session = Depends(get_db)):
    return employee_service.create_employee(db, request)

@router.get("/", response_model=List[Employee])
def get_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return employee_service.get_all(db, skip, limit)

@router.get("/{employee_id}", response_model=Employee)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    return employee_service.get(db, employee_id)

@router.delete("/{employee_id}", response_model=DeleteResponse)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    return employee_service.delete(db, employee_id)



