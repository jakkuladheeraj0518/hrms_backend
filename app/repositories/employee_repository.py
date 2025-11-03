from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from models.employee import Employee
from schemas.employee import EmployeeCreate, EmployeeUpdate

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, employee_data: EmployeeCreate) -> Employee:
        db_employee = Employee(**employee_data.dict())
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.id == employee_id).first()

    def get_by_employee_id(self, employee_id: str) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.employee_id == employee_id).first()

    def get_by_email(self, email: str) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.email == email).first()

    def get_all(
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
        query = self.db.query(Employee)
        
        if search:
            query = query.filter(
                or_(
                    Employee.name.ilike(f"%{search}%"),
                    Employee.employee_id.ilike(f"%{search}%")
                )
            )
        
        if department:
            query = query.filter(Employee.department == department)
        if location:
            query = query.filter(Employee.location == location)
        if business_unit:
            query = query.filter(Employee.business_unit == business_unit)
        if cost_center:
            query = query.filter(Employee.cost_center == cost_center)
        if designation:
            query = query.filter(Employee.designation == designation)
        if is_active is not None:
            query = query.filter(Employee.is_active == is_active)
        
        return query.offset(offset).limit(limit).all()

    def update(self, employee_id: int, employee_data: EmployeeUpdate) -> Optional[Employee]:
        employee = self.get_by_id(employee_id)
        if not employee:
            return None
        
        update_data = employee_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(employee, field, value)
        
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def delete(self, employee_id: int) -> bool:
        employee = self.get_by_id(employee_id)
        if not employee:
            return False
        
        self.db.delete(employee)
        self.db.commit()
        return True

    def get_filter_options(self):
        departments = self.db.query(Employee.department).distinct().all()
        locations = self.db.query(Employee.location).distinct().all()
        business_units = self.db.query(Employee.business_unit).distinct().all()
        cost_centers = self.db.query(Employee.cost_center).distinct().all()
        designations = self.db.query(Employee.designation).distinct().all()
        
        return {
            "departments": [d[0] for d in departments if d[0]],
            "locations": [l[0] for l in locations if l[0]],
            "business_units": [b[0] for b in business_units if b[0]],
            "cost_centers": [c[0] for c in cost_centers if c[0]],
            "designations": [d[0] for d in designations if d[0]]
        }