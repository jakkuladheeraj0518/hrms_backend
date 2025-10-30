from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from app.database.session import get_db
from app.models.payroll_models import Employee, SalaryComponent, GratuityRecord, GratuityConfiguration
from app.schemas.payroll_schemas import (
    EmployeeCreate, EmployeeResponse,
    SalaryComponentCreate, SalaryComponentResponse,
    GratuityCalculationRequest, GratuitySummaryResponse, GratuityRecordResponse,
    GratuityConfigurationResponse
)

router = APIRouter(prefix="/api/gratuity", tags=["Gratuity"])

# ============================================================
# 🧑 EMPLOYEES
# ============================================================
@router.post("/employees/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.get("/employees/", response_model=List[EmployeeResponse])
def get_employees(skip: int = 0, limit: int = 100, location: Optional[str] = None, department: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Employee)
    if location and location != "All Locations":
        query = query.filter(Employee.location == location)
    if department and department != "All Departments":
        query = query.filter(Employee.department == department)
    employees = query.offset(skip).limit(limit).all()
    return employees


# ============================================================
# 💰 SALARY COMPONENTS
# ============================================================
@router.post("/salary-components/", response_model=SalaryComponentResponse)
def create_salary_component(salary: SalaryComponentCreate, db: Session = Depends(get_db)):
    data = salary.dict()
    effective_date = data.get("effective_from")
    if effective_date:
        data["month"] = effective_date.strftime("%B")
        data["year"] = effective_date.year
    else:
        raise HTTPException(status_code=400, detail="effective_from is required")

    db_salary = SalaryComponent(**data)
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary


# ============================================================
# 🧾 GRATUITY CALCULATION
# ============================================================
@router.post("/gratuity/calculate", response_model=GratuitySummaryResponse)
def calculate_gratuity_summary(request: GratuityCalculationRequest, db: Session = Depends(get_db)):
    if request.month_days <= request.payable_days:
        raise HTTPException(status_code=400, detail="Month days must be greater than payable days.")

    try:
        month_name, year_str = request.month.split("-")
        year = int(year_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid month format. Use 'Month-YYYY'")

    query = db.query(Employee)
    if request.location and request.location != "All Locations":
        query = query.filter(Employee.location == request.location)
    if request.department and request.department != "All Departments":
        query = query.filter(Employee.department == request.department)
    employees = query.all()

    if not employees:
        return GratuitySummaryResponse(eligible_employees=0, total_payable=0, records=[])

    total_payable = 0.0
    eligible_records = []

    for employee in employees:
        if not employee.joining_date:
            continue

        def years_between(start_date, end_date):
            return (end_date - start_date).days / 365.0

        years = years_between(employee.joining_date, employee.exit_date or datetime.now().date())
        if years < request.min_years:
            continue

        salary = db.query(SalaryComponent).filter(
            SalaryComponent.employee_id == employee.id,
            SalaryComponent.month == month_name,
            SalaryComponent.year == year
        ).first()
        if not salary:
            continue

        normalized_components = []
        for comp in request.salary_components:
            c = comp.lower()
            if "basic" in c:
                normalized_components.append("basic_salary")
            elif "hra" in c or "rent" in c:
                normalized_components.append("house_rent_allowance")
            elif "special" in c:
                normalized_components.append("special_allowance")
            elif "medical" in c:
                normalized_components.append("medical_allowance")
            elif "conveyance" in c:
                normalized_components.append("conveyance_allowance")
            elif "telephone" in c:
                normalized_components.append("telephone_allowance")

        base_salary = sum([float(getattr(salary, attr, 0) or 0) for attr in normalized_components]) or float(salary.basic_salary or 0)
        if base_salary <= 0:
            continue

        gratuity_amount = round((base_salary * request.payable_days * years) / request.month_days, 2)
        record = GratuityRecord(
            employee_id=employee.id,
            years_of_service=years,
            last_drawn_salary=base_salary,
            gratuity_amount=gratuity_amount,
            calculation_date=datetime.utcnow().date(),
            status="pending",
            month=month_name,
            year=year
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        eligible_records.append(
            GratuityRecordResponse(
                id=record.id,
                employee_id=employee.id,
                employee_name=employee.name,
                base_salary=base_salary,
                years_in_service=years,
                gratuity_amount=gratuity_amount,
                status="pending",
                month=month_name,
                year=year,
                is_processed=False
            )
        )
        total_payable += gratuity_amount

    return GratuitySummaryResponse(
        eligible_employees=len(eligible_records),
        total_payable=round(total_payable, 2),
        records=eligible_records
    )


# ============================================================
# ⚙️ CONFIGURATION
# ============================================================
@router.get("/configuration/", response_model=GratuityConfigurationResponse)
def get_configuration(db: Session = Depends(get_db)):
    config = db.query(GratuityConfiguration).first()
    if not config:
        config = GratuityConfiguration()
        db.add(config)
        db.commit()
        db.refresh(config)
    return config


@router.put("/configuration/")
def update_configuration(
    min_years: Optional[float] = None,
    payable_days: Optional[int] = None,
    month_days: Optional[int] = None,
    exit_only: Optional[bool] = None,
    year_rounding: Optional[str] = None,
    salary_components: Optional[str] = None,
    db: Session = Depends(get_db)
):
    config = db.query(GratuityConfiguration).first()
    if not config:
        config = GratuityConfiguration()
        db.add(config)

    if min_years is not None:
        config.min_years = min_years
    if payable_days is not None:
        config.payable_days = payable_days
    if month_days is not None:
        config.month_days = month_days
    if exit_only is not None:
        config.exit_only = exit_only
    if year_rounding is not None:
        config.year_rounding = year_rounding
    if salary_components is not None:
        config.salary_components = salary_components

    config.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Configuration updated successfully"}


# ============================================================
# 📋 RECORDS (GET, PROCESS, DELETE)
# ============================================================
@router.get("/gratuity/records/{month}/{year}", response_model=List[GratuityRecordResponse])
def get_gratuity_records(month: str, year: int, db: Session = Depends(get_db)):
    records = db.query(GratuityRecord).filter(
        GratuityRecord.month == month,
        GratuityRecord.year == year
    ).all()

    if not records:
        raise HTTPException(status_code=404, detail="No records found for this period")

    response = []
    for record in records:
        employee = db.query(Employee).filter(Employee.id == record.employee_id).first()
        response.append(
            GratuityRecordResponse(
                id=record.id,
                employee_id=record.employee_id,
                employee_name=employee.name if employee else "Unknown",
                base_salary=float(record.last_drawn_salary),
                years_in_service=record.years_of_service,
                gratuity_amount=float(record.gratuity_amount),
                status=record.status,
                month=record.month,
                year=record.year,
                is_processed=getattr(record, "is_processed", False)
            )
        )
    return response


@router.post("/gratuity/process/{month}/{year}")
def process_gratuity(month: str, year: int, db: Session = Depends(get_db)):
    records = db.query(GratuityRecord).filter(
        GratuityRecord.month == month,
        GratuityRecord.year == year,
        GratuityRecord.status == "pending"
    ).all()

    if not records:
        raise HTTPException(status_code=404, detail="No unprocessed gratuity records found")

    for record in records:
        record.status = "processed"
        record.processed_at = datetime.utcnow()

    db.commit()
    return {"message": f"Processed {len(records)} gratuity records", "count": len(records)}


@router.delete("/gratuity/records/{month}/{year}")
def delete_gratuity_records(month: str, year: int, db: Session = Depends(get_db)):
    records = db.query(GratuityRecord).filter(
        GratuityRecord.month == month,
        GratuityRecord.year == year
    ).delete()

    db.commit()
    return {"message": f"Deleted {records} gratuity records", "count": records}
