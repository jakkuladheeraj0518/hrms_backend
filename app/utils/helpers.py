import os
import uuid
import logging
from math import floor, ceil
from datetime import datetime, timedelta, date
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.payroll_models import SalaryComponent, RecalculationRateLimit


# ----------------------#
#  Logging Configuration
# ----------------------#
logging.basicConfig(
    filename="payroll.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_message(message: str):
    """Log messages to payroll.log file."""
    logging.info(message)


# ----------------------#
#  Payroll Calculations
# ----------------------#
def check_rate_limit(db: Session, all_employees: bool) -> bool:
    """
    Prevents recalculating all employees' payroll more than 3 times within 30 minutes.
    """
    if not all_employees:
        return True

    cutoff = datetime.utcnow() - timedelta(minutes=30)
    count = db.query(RecalculationRateLimit).filter(
        RecalculationRateLimit.all_employees.is_(True),
        RecalculationRateLimit.created_at >= cutoff
    ).count()
    return count < 3


def calculate_years_of_service(joining_date: date, exit_date: date, rounding: str = "Round Down") -> float:
    """
    Calculate years of service between joining and exit dates with rounding options.
    """
    if not joining_date or not exit_date:
        return 0.0

    days_diff = (exit_date - joining_date).days
    years = days_diff / 365

    rounding = rounding.lower().strip()
    if rounding == "round down":
        return floor(years)
    elif rounding == "round up":
        return ceil(years)
    elif rounding == "round nearest":
        return round(years)
    else:
        return round(years, 2)


def calculate_gratuity(base_salary: float, years: float, payable_days: int, month_days: int = 26) -> float:
    """
    Calculate gratuity based on base salary, years of service, and payable days.
    """
    if base_salary <= 0 or years <= 0:
        return 0.0
    gratuity_amount = (base_salary * payable_days * years) / month_days
    return round(gratuity_amount, 2)


def get_base_salary(salary_component: SalaryComponent, selected_components: List[str]) -> float:
    """
    Extract base salary from selected components in SalaryComponent model.
    """
    component_map = {
        "basic_salary": salary_component.basic_salary,
        "basic": salary_component.basic_salary,
        "hra": salary_component.hra,
        "house_rent_allowance": salary_component.hra,
        "special_allowance": salary_component.special_allowance,
        "special": salary_component.special_allowance,
        "medical_allowance": salary_component.medical_allowance,
        "conveyance_allowance": salary_component.conveyance_allowance,
        "telephone_allowance": salary_component.telephone_allowance,
    }

    base_salary = 0.0
    for component in selected_components:
        key = component.strip().lower()
        value = component_map.get(key)
        if value is not None:
            base_salary += float(value)
    return round(base_salary, 2)


# ----------------------#
#  Chart Data Generation
# ----------------------#
def generate_chart_data(runs: List):
    """
    Generate chart labels and values for payroll analytics dashboard.
    """
    labels = [r.period for r in runs]
    values = [r.total_net_payroll for r in runs]
    return {"labels": labels, "values": values}


# ----------------------#
#  File Upload Handling
# ----------------------#
def ensure_upload_dir(path: str = "./uploads") -> str:
    """
    Ensures that upload directory exists.
    """
    os.makedirs(path, exist_ok=True)
    return path


def save_upload_file(upload_dir: str, filename: str, data: bytes) -> str:
    """
    Saves uploaded file with a unique name to the specified directory.
    """
    os.makedirs(upload_dir, exist_ok=True)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    path = os.path.join(upload_dir, unique_filename)
    with open(path, "wb") as f:
        f.write(data)
    return path


# ----------------------#
#  Date Parsing Utility
# ----------------------#
def parse_date(value: str, required: bool = False, field_name: str = "date") -> date | None:
    """
    Parses a date string in multiple formats safely.
    """
    if not value:
        if required:
            raise HTTPException(status_code=422, detail=f"{field_name} is required")
        return None

    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    if required:
        raise HTTPException(status_code=422, detail=f"Invalid date format for {field_name}")
    return None
