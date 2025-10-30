from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database.session import get_db
from app.models.payroll_models import Employee, SalaryComponent, BonusConfiguration, BonusRecord, BonusSummary
from app.schemas.payroll_schemas import BonusConfigurationBase, BonusGenerateRequest, BonusRecordResponse, BonusSummaryResponse, BonusProcessResponse

router = APIRouter(prefix="/api/bonus", tags=["Bonus"])

VALID_COMPONENTS = ["basic", "hra", "sa", "mda", "conveyance", "telephone"]

def calculate_base_salary(salary: SalaryComponent, components: dict) -> float:
    base_salary = 0.0
    if not salary:
        return base_salary
    for comp in VALID_COMPONENTS:
        if components.get(comp, False):
            if comp == "basic":
                base_salary += float(salary.basic_salary or 0)
            elif comp == "hra":
                base_salary += float(salary.hra or 0)
            elif comp == "sa":
                base_salary += float(salary.special_allowance or 0)
            elif comp == "mda":
                base_salary += float(salary.medical_allowance or 0)
            elif comp == "conveyance":
                base_salary += float(salary.conveyance_allowance or 0)
            elif comp == "telephone":
                base_salary += float(salary.telephone_allowance or 0)
    return base_salary

def calculate_bonus_amount(base_salary: float, bonus_config: BonusConfigurationBase) -> float:
    calculation_base = min(base_salary, bonus_config.eligibility_cutoff)
    calculation_base = max(calculation_base, bonus_config.min_wages)
    bonus = round(calculation_base * (bonus_config.bonus_rate / 100), 2)
    if bonus < bonus_config.min_bonus:
        bonus = bonus_config.min_bonus
    if bonus_config.max_bonus > 0 and bonus > bonus_config.max_bonus:
        bonus = bonus_config.max_bonus
    return bonus

@router.get("/configuration", response_model=BonusConfigurationBase)
def get_bonus_configuration(db: Session = Depends(get_db)):
    config = db.query(BonusConfiguration).filter(BonusConfiguration.is_active == True).first()
    if not config:
        config = BonusConfiguration(bonus_rate=8.33, eligibility_cutoff=21000, min_wages=7000, min_bonus=100, max_bonus=0, is_active=True)
        db.add(config)
        db.commit()
        db.refresh(config)
    return config

@router.post("/configuration", response_model=BonusConfigurationBase)
def update_bonus_configuration(config_in: BonusConfigurationBase, db: Session = Depends(get_db)):
    db.query(BonusConfiguration).update({"is_active": False})
    db.commit()
    new_config = BonusConfiguration(**config_in.dict(), is_active=True)
    db.add(new_config)
    db.commit()
    db.refresh(new_config)
    return new_config

@router.post("/generate", response_model=BonusSummaryResponse)
def generate_bonus(request: BonusGenerateRequest, db: Session = Depends(get_db)):
    query = db.query(Employee).filter(Employee.is_active == True)
    if request.location_id: query = query.filter(Employee.location_id == request.location_id)
    if request.department_id: query = query.filter(Employee.department_id == request.department_id)
    if request.cost_center_id: query = query.filter(Employee.cost_center_id == request.cost_center_id)
    if request.employee_search:
        query = query.filter((Employee.name.ilike(f"%{request.employee_search}%")) | (Employee.employee_id.ilike(f"%{request.employee_search}%")))
    employees = query.all()
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found with given filters")
    db.query(BonusRecord).filter(BonusRecord.payment_period == request.payment_period, BonusRecord.status == "pending").delete()
    db.commit()
    bonus_records: List[BonusRecordResponse] = []
    total_payable = 0.0
    for emp in employees:
        salary = db.query(SalaryComponent).filter(SalaryComponent.employee_id == emp.id, SalaryComponent.is_current == True).first()
        if request.basic_salary:
            base_salary = request.basic_salary
        elif salary:
            base_salary = calculate_base_salary(salary, request.components.dict())
        else:
            continue
        bonus_amount = calculate_bonus_amount(base_salary, request.bonus_config)
        bonus_rec = BonusRecord(employee_id=emp.id, payment_period=request.payment_period, base_salary=base_salary, bonus_amount=bonus_amount, status="pending")
        db.add(bonus_rec)
        bonus_records.append(BonusRecordResponse(id=0, employee_id=emp.id, employee_name=emp.name, payment_period=request.payment_period, base_salary=base_salary, bonus_amount=bonus_amount, status="pending"))
        total_payable += bonus_amount
    db.commit()
    summary = BonusSummary(payment_period=request.payment_period, location_id=request.location_id, department_id=request.department_id, cost_center_id=request.cost_center_id, total_employees=len(employees), eligible_employees=len(bonus_records), total_payable=total_payable, status="generated")
    db.add(summary)
    db.commit()
    return BonusSummaryResponse(eligible_employees=len(bonus_records), total_payable=total_payable, records=bonus_records)

@router.get("/summary/{payment_period}", response_model=BonusSummaryResponse)
def get_bonus_summary(payment_period: str, db: Session = Depends(get_db)):
    records = db.query(BonusRecord).filter(BonusRecord.payment_period == payment_period).all()
    if not records:
        return BonusSummaryResponse(eligible_employees=0, total_payable=0, records=[])
    records_resp = []
    total = 0.0
    for r in records:
        emp = db.query(Employee).filter(Employee.id == r.employee_id).first()
        records_resp.append(BonusRecordResponse(id=r.id, employee_id=r.employee_id, employee_name=emp.name if emp else "Unknown", payment_period=r.payment_period, base_salary=float(r.base_salary), bonus_amount=float(r.bonus_amount), status=r.status))
        total += float(r.bonus_amount)
    return BonusSummaryResponse(eligible_employees=len(records_resp), total_payable=total, records=records_resp)

@router.post("/process/{payment_period}", response_model=BonusProcessResponse)
def process_bonus(payment_period: str, db: Session = Depends(get_db)):
    records = db.query(BonusRecord).filter(BonusRecord.payment_period == payment_period, BonusRecord.status == "pending").all()
    if not records:
        raise HTTPException(status_code=404, detail="No pending bonus records found")
    total_amount = 0.0
    count = 0
    for r in records:
        r.status = "processed"
        r.processed_at = datetime.utcnow()
        total_amount += float(r.bonus_amount)
        count += 1
    summary = db.query(BonusSummary).filter(BonusSummary.payment_period == payment_period).first()
    if summary:
        summary.status = "processed"
        summary.processed_at = datetime.utcnow()
    db.commit()
    return BonusProcessResponse(message=f"Successfully processed bonus for {count} employees", processed_count=count, total_amount=total_amount, status="success")

@router.delete("/delete/{payment_period}")
def delete_bonus(payment_period: str, db: Session = Depends(get_db)):
    deleted_count = db.query(BonusRecord).filter(BonusRecord.payment_period == payment_period, BonusRecord.status == "pending").delete()
    summary = db.query(BonusSummary).filter(BonusSummary.payment_period == payment_period).first()
    if summary and summary.status == "generated":
        summary.status = "deleted"
        summary.deleted_at = datetime.utcnow()
    db.commit()
    return {"message": f"Deleted {deleted_count} pending bonus records", "payment_period": payment_period}
