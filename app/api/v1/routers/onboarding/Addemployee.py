from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.onboarding import EmployeeCreate, EmployeeResponse
from app.services.onboarding import add_employee, get_all


from datetime import datetime
from app.utils.helpers import parse_date
from app.database.session import get_db
from app.models.onboarding import OnboardingEmployee as Employees

router = APIRouter(prefix="/addemployee", tags=["Add Employee"])

# Helper: Generate next sequential employee code (EMP001, EMP002, etc.)
def generate_employee_code(db: Session):
    last_emp = (
        db.query(Employees)
        .filter(Employees.employee_code.like("EMP%"))
        .order_by(Employees.id.desc())
        .first()
    )
    if not last_emp or not last_emp.employee_code:
        return "EMP001"

    try:
        num = int(last_emp.employee_code.replace("EMP", ""))
        next_num = num + 1
        return f"EMP{next_num:03d}"
    except Exception:
        return "EMP001"

# date parsing provided by app.utils.helpers.parse_date

# Add Employee
@router.post("/")
def add_employee(
    first_name: str = Form(...),
    middle_name: str = Form(""),
    last_name: str = Form(""),
    joining_date: str = Form(...),
    confirmation_date: str = Form(None),
    dob: str = Form(None),
    gender: str = Form(...),
    employee_code: str = Form(None),
    biometric_code: str = Form(""),
    mobile: str = Form(...),
    email: str = Form(...),
    send_mobile_login: bool = Form(False),
    send_web_login: bool = Form(True),
    location: str = Form(""),
    cost_center: str = Form(""),
    department: str = Form(""),
    grade: str = Form(""),
    designation: str = Form(""),
    shift_policy: str = Form(""),
    week_off_policy: str = Form(""),
    db: Session = Depends(get_db)
):
    # Auto-generate employee code if not provided
    if not employee_code:
        employee_code = generate_employee_code(db)

    # Check for duplicate employee code
    existing = db.query(Employees).filter(Employees.employee_code == employee_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee code already exists")

    # Parse and validate dates
    joining_date_parsed = parse_date(joining_date, required=True, field_name="joining_date")
    confirmation_date_parsed = parse_date(confirmation_date, field_name="confirmation_date")
    dob_parsed = parse_date(dob, field_name="dob")

    db_employee = Employees(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        joining_date=joining_date_parsed,
        confirmation_date=confirmation_date_parsed,
        dob=dob_parsed,
        gender=gender,
        employee_code=employee_code,
        biometric_code=biometric_code,
        mobile=mobile,
        email=email,
        send_mobile_login=send_mobile_login,
        send_web_login=send_web_login,
        location=location,
        cost_center=cost_center,
        department=department,
        grade=grade,
        designation=designation,
        shift_policy=shift_policy,
        week_off_policy=week_off_policy,
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    # Return structured response
    return {
        "message": "Employee added successfully",
        "employee_code": db_employee.employee_code,
        "employee": {
            "id": db_employee.id,
            "first_name": db_employee.first_name,
            "middle_name": db_employee.middle_name,
            "last_name": db_employee.last_name,
            "employee_code": db_employee.employee_code,
            "gender": db_employee.gender,
            "dob": db_employee.dob.strftime("%Y-%m-%d") if db_employee.dob else None,
            "joining_date": db_employee.joining_date.strftime("%Y-%m-%d"),
            "confirmation_date": db_employee.confirmation_date.strftime("%Y-%m-%d") if db_employee.confirmation_date else None,
            "mobile": db_employee.mobile,
            "email": db_employee.email,
            "biometric_code": db_employee.biometric_code,
            "send_mobile_login": db_employee.send_mobile_login,
            "send_web_login": db_employee.send_web_login,
            "location": db_employee.location,
            "cost_center": db_employee.cost_center,
            "department": db_employee.department,
            "grade": db_employee.grade,
            "designation": db_employee.designation,
            "shift_policy": db_employee.shift_policy,
            "week_off_policy": db_employee.week_off_policy,
            "approved": db_employee.approved,
        }
    }

# Get all employees
@router.get("/")
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employees).all()
