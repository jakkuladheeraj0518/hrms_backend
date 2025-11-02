from sqlalchemy.orm import Session
from app.repositories.onboarding import create_employee, get_employee_by_email, get_employee, list_employees, update_employee, approve_employee
from app.schemas.onboarding import EmployeeCreate, EmployeeUpdate
from app.utils.mailer import send_onboarding_email
from app.utils.sms import send_sms
from app.config import settings

def add_employee(db: Session, payload: EmployeeCreate):
    if get_employee_by_email(db, payload.email):
        raise ValueError("Employee with this email already exists")
    employee = create_employee(db, payload)
    form_link = f"{settings.PROJECT_NAME}://{settings.UPLOAD_DIR}/onboarding/form/{employee.id}"
    # try send notifications (stubbed)
    send_onboarding_email(employee.first_name, employee.email, form_link)
    send_sms(employee.mobile, f"Please complete onboarding: {form_link}")
    return employee

def get_all(db: Session, skip: int = 0, limit: int = 100):
    return list_employees(db, skip, limit)

def approve(db: Session, emp_id: int):
    emp = get_employee(db, emp_id)
    if not emp:
        raise ValueError("Employee not found")
    return approve_employee(db, emp)
