from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from database.connection import Base
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    designation = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    business_unit = Column(String(100), nullable=True)
    cost_center = Column(String(50), nullable=True)
    joining_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    email = Column(String(100), unique=True, nullable=True)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Employee(id={self.id}, employee_id='{self.employee_id}', name='{self.name}')>"