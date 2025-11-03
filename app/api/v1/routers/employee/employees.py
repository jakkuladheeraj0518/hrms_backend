from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from schemas.employee import Employee, EmployeeCreate, EmployeeUpdate
from services.employee_service import EmployeeService
from dependencies.database import get_db

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=Employee)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.create_employee(employee)

@router.get("/", response_model=List[Employee])
def get_employees(
    search: Optional[str] = Query(None, description="Search by name or employee ID"),
    department: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    business_unit: Optional[str] = Query(None),
    cost_center: Optional[str] = Query(None),
    designation: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)
    return service.get_employees(
        search=search,
        department=department,
        location=location,
        business_unit=business_unit,
        cost_center=cost_center,
        designation=designation,
        is_active=is_active,
        limit=limit,
        offset=offset
    )

@router.get("/{employee_id}", response_model=Employee)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.get_employee_by_id(employee_id)

@router.put("/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, employee_update: EmployeeUpdate, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.update_employee(employee_id, employee_update)

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.delete_employee(employee_id)

@router.get("/search/filters")
def get_filter_options(db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.get_filter_options()