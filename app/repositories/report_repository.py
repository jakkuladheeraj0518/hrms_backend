from sqlalchemy.orm import Session
from app.models.report_models import (
    AIReport, SalaryReport, AttendanceReport, EmployeeReport, StatutoryReport
)

# ----------------------------
# AI
def create_ai_report(db: Session, query: str, response: str):
    report = AIReport(query=query, response=response)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def get_all_ai_reports(db: Session):
    return db.query(AIReport).all()

# ----------------------------
# Salary
def save_salary_report(db: Session, report_type: str, content: str):
    report = SalaryReport(report_type=report_type, content=content)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def fetch_all_salary_reports(db: Session):
    return db.query(SalaryReport).all()

# ----------------------------
# Attendance
def save_attendance_report(db: Session, report_type: str, content: str):
    report = AttendanceReport(report_type=report_type, content=content)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def fetch_all_attendance_reports(db: Session):
    return db.query(AttendanceReport).all()

# ----------------------------
# Employee
def save_employee_report(db: Session, report_type: str, description: str):
    report = EmployeeReport(report_type=report_type, description=description)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def fetch_all_employee_reports(db: Session):
    return db.query(EmployeeReport).all()

# ----------------------------
# Statutory
def save_statutory_report(db: Session, data):
    report = StatutoryReport(**data.dict())
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def fetch_all_statutory_reports(db: Session):
    return db.query(StatutoryReport).all()
