from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.onboarding import OnboardingEmployee as Employees
from app.utils.helpers import parse_date
import datetime

router = APIRouter(prefix="/approve", tags=["Approve Additions"])

# parse_date now reused from app.utils.helpers
# ✅ Get employees pending approval
@router.get("/pending")
def get_pending_employees(db: Session = Depends(get_db)):
    return db.query(Employees).filter(Employees.approved == False).all()


# ✅ Update employee (form-data)
@router.put("/{employee_id}")
def update_employee(
    employee_id: int,
    first_name: str = Form(...),
    middle_name: str = Form(""),
    last_name: str = Form(""),
    joining_date: str = Form(...),
    confirmation_date: str = Form(None),
    dob: str = Form(None),
    gender: str = Form(...),
    employee_code: str = Form(...),
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
    # ✅ Fetch employee by ID
    emp = db.query(Employees).filter(Employees.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    # ✅ Parse all dates safely
    emp.joining_date = parse_date(joining_date)
    emp.confirmation_date = parse_date(confirmation_date)
    emp.dob = parse_date(dob)

    # ✅ Update fields
    emp.first_name = first_name
    emp.middle_name = middle_name
    emp.last_name = last_name
    emp.gender = gender
    emp.employee_code = employee_code
    emp.biometric_code = biometric_code
    emp.mobile = mobile
    emp.email = email
    emp.send_mobile_login = send_mobile_login
    emp.send_web_login = send_web_login
    emp.location = location
    emp.cost_center = cost_center
    emp.department = department
    emp.grade = grade
    emp.designation = designation
    emp.shift_policy = shift_policy
    emp.week_off_policy = week_off_policy

    # ✅ Commit changes
    db.commit()
    db.refresh(emp)

    # ✅ Return a clean response including employee_code
    return {
        "message": "Employee updated successfully",
        "employee_code": emp.employee_code,
        "employee": emp
    }


# Delete employee
@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employees).filter(Employees.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(emp)
    db.commit()
    return {"detail": "Employee deleted successfully"}


# Approve employee
@router.put("/{employee_id}/approve")
def approve_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employees).filter(Employees.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    emp.approved = True
    db.commit()
    db.refresh(emp)
    return emp
