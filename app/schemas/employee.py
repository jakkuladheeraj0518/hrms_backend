from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EmployeeBase(BaseModel):
    employee_id: str = Field(..., description="Unique employee identifier")
    name: str = Field(..., min_length=1, max_length=100, description="Employee full name")
    designation: str = Field(..., description="Job designation/title")
    department: str = Field(..., description="Department name")
    location: str = Field(..., description="Work location")
    business_unit: Optional[str] = Field(None, description="Business unit")
    cost_center: Optional[str] = Field(None, description="Cost center code")
    joining_date: datetime = Field(..., description="Date of joining")
    is_active: bool = Field(True, description="Employee active status")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    designation: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    business_unit: Optional[str] = None
    cost_center: Optional[str] = None
    joining_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class Employee(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True