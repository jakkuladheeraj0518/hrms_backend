from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from repositories.employee_repository import EmployeeRepository
from schemas.employee import Employee, EmployeeCreate, EmployeeUpdate

class EmployeeService:
    def __init__(self, db: Session):
        self.repository = EmployeeRepository(db)

    def create_employee(self, employee_data: EmployeeCreate) -> Employee:
        # Check if employee_id already exists
        existing_employee = self.repository.get_by_employee_id(employee_data.employee_id)
        if existing_employee:
            raise HTTPException(status_code=400, detail="Employee ID already registered")
        
        # Check if email already exists
        if employee_data.email:
            existing_email = self.repository.get_by_email(employee_data.email)
            if existing_email:
                raise HTTPException(status_code=400, detail="Email already registered")
        
        return self.repository.create(employee_data)

    def get_employee_by_id(self, employee_id: int) -> Employee:
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee

    def get_employees(
        self,
        search: Optional[str] = None,
        department: Optional[str] = None,
        location: Optional[str] = None,
        business_unit: Optional[str] = None,
        cost_center: Optional[str] = None,
        designation: Optional[str] = None,
        is_active: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Employee]:
        return self.repository.get_all(
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

    def update_employee(self, employee_id: int, employee_data: EmployeeUpdate) -> Employee:
        # Check if email is being updated and already exists
        if employee_data.email:
            existing_employee = self.repository.get_by_id(employee_id)
            if existing_employee and employee_data.email != existing_employee.email:
                existing_email = self.repository.get_by_email(employee_data.email)
                if existing_email:
                    raise HTTPException(status_code=400, detail="Email already registered")
        
        updated_employee = self.repository.update(employee_id, employee_data)
        if not updated_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return updated_employee

    def delete_employee(self, employee_id: int) -> dict:
        success = self.repository.delete(employee_id)
        if not success:
            raise HTTPException(status_code=404, detail="Employee not found")
        return {"message": "Employee deleted successfully"}

    def get_filter_options(self):
        return self.repository.get_filter_options()