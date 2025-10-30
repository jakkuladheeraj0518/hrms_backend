from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database.session import get_db
from app.models.payroll_models import Location, Department, CostCenter, Employee, LeaveType, LeaveBalance, LeaveEncashment
from app.schemas.payroll_schemas import (
    LocationSchema, DepartmentSchema, CostCenterSchema,
    EmployeeSchema, EmployeeCreate, EmployeeResponse,
    LeaveTypeSchema, LeaveBalanceSchema,
    LeaveEncashmentSchema, GenerateEncashmentRequest
)
router = APIRouter(prefix="/api/leave-encashment", tags=["Leave Encashment"])

@router.get("/locations", response_model=List[LocationSchema])
def get_locations(db: Session = Depends(get_db)):
    return db.query(Location).all()

@router.post("/locations", response_model=LocationSchema)
def create_location(location: LocationSchema, db: Session = Depends(get_db)):
    loc = Location(name=location.name)
    db.add(loc)
    db.commit()
    db.refresh(loc)
    return loc

@router.get("/departments", response_model=List[DepartmentSchema])
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()

@router.post("/departments", response_model=DepartmentSchema)
def create_department(department: DepartmentSchema, db: Session = Depends(get_db)):
    dept = Department(name=department.name)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept

@router.get("/cost-centers", response_model=List[CostCenterSchema])
def get_cost_centers(db: Session = Depends(get_db)):
    return db.query(CostCenter).all()

@router.post("/cost-centers", response_model=CostCenterSchema)
def create_cost_center(cost_center: CostCenterSchema, db: Session = Depends(get_db)):
    cc = CostCenter(name=cost_center.name)
    db.add(cc)
    db.commit()
    db.refresh(cc)
    return cc

@router.get("/employees", response_model=List[EmployeeResponse])
def get_employees(location_id: Optional[int] = None, department_id: Optional[int] = None, cost_center_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Employee)
    if location_id:
        query = query.filter(Employee.location_id == location_id)
    if department_id:
        query = query.filter(Employee.department_id == department_id)
    if cost_center_id:
        query = query.filter(Employee.cost_center_id == cost_center_id)
    return query.all()

@router.post("/employees", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    emp = Employee(**employee.dict())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

@router.get("/leave-types", response_model=List[LeaveTypeSchema])
def get_leave_types(db: Session = Depends(get_db)):
    return db.query(LeaveType).all()

@router.post("/leave-types", response_model=LeaveTypeSchema)
def create_leave_type(leave_type: LeaveTypeSchema, db: Session = Depends(get_db)):
    lt = LeaveType(**leave_type.dict())
    db.add(lt)
    db.commit()
    db.refresh(lt)
    return lt

@router.post("/leave-balances", response_model=LeaveBalanceSchema)
def create_leave_balance(balance: LeaveBalanceSchema, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == balance.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee {balance.employee_id} does not exist")
    leave_type = db.query(LeaveType).filter(LeaveType.id == balance.leave_type_id).first()
    if not leave_type:
        raise HTTPException(status_code=404, detail=f"Leave type {balance.leave_type_id} does not exist")
    lb = LeaveBalance(**balance.dict())
    db.add(lb)
    db.commit()
    db.refresh(lb)
    return lb

@router.post("/generate")
def generate_encashment_summary(request: GenerateEncashmentRequest, db: Session = Depends(get_db)):
    query = db.query(Employee)
    if request.location_ids:
        query = query.filter(Employee.location_id.in_(request.location_ids))
    if request.department_ids:
        query = query.filter(Employee.department_id.in_(request.department_ids))
    if request.cost_center_ids:
        query = query.filter(Employee.cost_center_id.in_(request.cost_center_ids))

    employees = query.all()
    encashments = []
    total_payable = 0

    for emp in employees:
        lb = db.query(LeaveBalance).filter(
            LeaveBalance.employee_id == emp.id,
            LeaveBalance.leave_type_id == request.leave_type_id,
            LeaveBalance.balance_as_on <= request.balance_as_on
        ).order_by(LeaveBalance.balance_as_on.desc()).first()

        if lb and lb.balance_days > request.balance_above:
            encash_days = lb.balance_days - request.balance_above
            encash_amt = encash_days * emp.daily_salary
            total_payable += encash_amt

            enc = LeaveEncashment(
                employee_id=emp.id,
                leave_type_id=request.leave_type_id,
                payment_period=request.payment_period,
                leave_balance=lb.balance_days,
                daily_salary=emp.daily_salary,
                encashment_days=encash_days,
                encashment_amount=encash_amt
            )
            db.add(enc)
            encashments.append(enc)

    db.commit()

    return {
        "eligible_employees": len(encashments),
        "total_payable": total_payable,
        "encashments": [
            {
                "employee_id": e.employee_id,
                "leave_balance": e.leave_balance,
                "daily_salary": e.daily_salary,
                "encashment_days": e.encashment_days,
                "encashment_amount": e.encashment_amount
            } for e in encashments
        ]
    }

@router.post("/process")
def process_encashment(payment_period: date, db: Session = Depends(get_db)):
    encs = db.query(LeaveEncashment).filter(
        LeaveEncashment.payment_period == payment_period,
        LeaveEncashment.processed == False
    ).all()

    for e in encs:
        e.processed = True

    db.commit()
    return {"message": "Encashment processed successfully", "processed_count": len(encs)}
