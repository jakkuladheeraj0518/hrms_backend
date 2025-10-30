from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from math import floor, ceil
from typing import List
import logging
from app.models.payroll_models import SalaryComponent, RecalculationRateLimit

def check_rate_limit(db: Session, all_employees: bool):
    if not all_employees:
        return True
    cutoff = datetime.utcnow() - timedelta(minutes=30)
    count = db.query(RecalculationRateLimit).filter(
        RecalculationRateLimit.all_employees.is_(True),
        RecalculationRateLimit.created_at >= cutoff
    ).count()
    return count < 3

def calculate_years_of_service(joining_date: date, exit_date: date, rounding: str) -> float:
    if not joining_date or not exit_date:
        return 0.0
    days_diff = (exit_date - joining_date).days
    years = days_diff / 365
    if rounding == "Round Down":
        return floor(years)
    elif rounding == "Round Up":
        return ceil(years)
    elif rounding == "Round Nearest":
        return round(years)
    else:
        return round(years, 2)

def calculate_gratuity(base_salary: float, years: float, payable_days: int, month_days: int) -> float:
    if base_salary <= 0 or years <= 0:
        return 0.0
    gratuity_amount = (base_salary * payable_days * years) / month_days
    return round(gratuity_amount, 2)

def get_base_salary(salary_component: SalaryComponent, selected_components: List[str]) -> float:
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

logging.basicConfig(
    filename="payroll.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_message(message: str):
    logging.info(message)

def generate_chart_data(runs: List):
    labels = [r.period for r in runs]
    values = [r.total_net_payroll for r in runs]
    return {"labels": labels, "values": values}

import logging
from datetime import datetime
from typing import List

# Setup logger
logging.basicConfig(
    filename="payroll.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_message(message: str):
    """Log info messages into payroll.log"""
    logging.info(message)

def generate_chart_data(runs: List):
    """Generate labels and values for chart from PayrollRun records"""
    labels = [r.period for r in runs]
    values = [r.total_net_payroll for r in runs]
    return {"labels": labels, "values": values}
