from sqlalchemy.orm import Session
from app.models import datacapture as models
from app.schemas import datacapture_schema as schemas
from datetime import date

def create_salary_variable(db: Session, salary: schemas.SalaryVariableCreate):
    db_salary = models.SalaryVariable(**salary.dict())
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary

def get_salary_variables(db: Session):
    return db.query(models.SalaryVariable).all()

def update_salary_variable(db: Session, salary_id: int, salary: schemas.SalaryVariableCreate):
    db_salary = db.query(models.SalaryVariable).filter(models.SalaryVariable.id == salary_id).first()
    if not db_salary:
        return None
    for key, value in salary.dict().items():
        setattr(db_salary, key, value)
    db.commit()
    db.refresh(db_salary)
    return db_salary

def delete_salary_variable(db: Session, salary_id: int):
    db_salary = db.query(models.SalaryVariable).filter(models.SalaryVariable.id == salary_id).first()
    if not db_salary:
        return None
    db.delete(db_salary)
    db.commit()
    return db_salary

def create_deduction_variable(db: Session, deduction: schemas.DeductionVariableCreate):
    db_deduction = models.DeductionVariable(**deduction.dict())
    db.add(db_deduction)
    db.commit()
    db.refresh(db_deduction)
    return db_deduction

def get_deduction_variables(db: Session):
    return db.query(models.DeductionVariable).all()

def update_deduction_variable(db: Session, deduction_id: int, deduction: schemas.DeductionVariableCreate):
    db_deduction = db.query(models.DeductionVariable).filter(models.DeductionVariable.id == deduction_id).first()
    if not db_deduction:
        return None
    for key, value in deduction.dict().items():
        setattr(db_deduction, key, value)
    db.commit()
    db.refresh(db_deduction)
    return db_deduction

def delete_deduction_variable(db: Session, deduction_id: int):
    db_deduction = db.query(models.DeductionVariable).filter(models.DeductionVariable.id == deduction_id).first()
    if not db_deduction:
        return None
    db.delete(db_deduction)
    db.commit()
    return db_deduction

def create_tds_challan(db: Session, challan: schemas.TDSChallanCreate):
    db_challan = models.TDSChallan(**challan.dict())
    db.add(db_challan)
    db.commit()
    db.refresh(db_challan)
    return db_challan

def get_tds_challans(db: Session):
    return db.query(models.TDSChallan).all()

def get_tds_challan_by_id(db: Session, challan_id: int):
    return db.query(models.TDSChallan).filter(models.TDSChallan.id == challan_id).first()

def update_tds_challan(db: Session, challan_id: int, updated: schemas.TDSChallanCreate):
    db_challan = db.query(models.TDSChallan).filter(models.TDSChallan.id == challan_id).first()
    if not db_challan:
        return None
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(db_challan, key, value)
    db.commit()
    db.refresh(db_challan)
    return db_challan

def delete_tds_challan(db: Session, challan_id: int):
    db_challan = db.query(models.TDSChallan).filter(models.TDSChallan.id == challan_id).first()
    if db_challan:
        db.delete(db_challan)
        db.commit()
    return db_challan

def create_deduction_tds(db: Session, deduction_tds: schemas.DeductionTDSCreate):
    data = deduction_tds.dict()
    data["netsalary"] = data.get("grosssalary", 0) - data.get("calculatedexemptions", 0) - data.get("additionalexemptions", 0)
    db_deduction_tds = models.DeductionTDS(**data)
    db.add(db_deduction_tds)
    db.commit()
    db.refresh(db_deduction_tds)
    return db_deduction_tds

def get_deduction_tds(db: Session):
    return db.query(models.DeductionTDS).all()

def create_income_tax_tds(db: Session, income_tds: schemas.IncomeTaxTDSCreate):
    db_record = models.IncomeTaxTDS(
        employee_id=income_tds.employee_id,
        employee_name=income_tds.employee_name,
        designation=income_tds.designation,
        status=income_tds.status or "Enabled",
        tds_amount=income_tds.tds_amount or 0,
        month=income_tds.month,
        created_date=income_tds.created_date or date.today()
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_all_income_tax_tds(db: Session):
    return db.query(models.IncomeTaxTDS).all()

def get_income_tax_tds_by_id(db: Session, id: int):
    return db.query(models.IncomeTaxTDS).filter(models.IncomeTaxTDS.id == id).first()

def update_income_tax_tds(db: Session, id: int, income_tds: schemas.IncomeTaxTDSCreate):
    record = db.query(models.IncomeTaxTDS).filter(models.IncomeTaxTDS.id == id).first()
    if not record:
        return None
    record.employee_id = income_tds.employee_id
    record.employee_name = income_tds.employee_name
    record.designation = income_tds.designation
    record.status = income_tds.status or "Enabled"
    record.tds_amount = income_tds.tds_amount or 0
    record.month = income_tds.month
    record.created_date = income_tds.created_date or record.created_date
    db.commit()
    db.refresh(record)
    return record

def delete_income_tax_tds(db: Session, id: int):
    record = db.query(models.IncomeTaxTDS).filter(models.IncomeTaxTDS.id == id).first()
    if not record:
        return False
    db.delete(record)
    db.commit()
    return True

def create_extra_days(db: Session, extra_days: schemas.ExtraDaysCreate):
    db_extra_days = models.ExtraDays(**extra_days.dict())
    db.add(db_extra_days)
    db.commit()
    db.refresh(db_extra_days)
    return db_extra_days

def get_extra_days(db: Session):
    return db.query(models.ExtraDays).all()

def create_extra_hours(db: Session, extra_hours: schemas.ExtraHoursCreate):
    db_extra_hours = models.ExtraHours(**extra_hours.dict())
    db.add(db_extra_hours)
    db.commit()
    db.refresh(db_extra_hours)
    return db_extra_hours

def get_extra_hours(db: Session):
    return db.query(models.ExtraHours).all()

def create_loan(db: Session, loan: schemas.LoanCreate):
    db_loan = models.Loan(**loan.dict())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def get_loans(db: Session):
    return db.query(models.Loan).all()

def get_loan_by_id(db: Session, loan_id: int):
    return db.query(models.Loan).filter(models.Loan.id == loan_id).first()

def update_loan(db: Session, loan_id: int, loan_update: schemas.LoanCreate):
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not db_loan:
        return None
    for key, value in loan_update.dict().items():
        setattr(db_loan, key, value)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def delete_loan(db: Session, loan_id: int):
    db_loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not db_loan:
        return False
    db.delete(db_loan)
    db.commit()
    return True

def create_data_capture_loan(db: Session, loan: schemas.DataCaptureLoanCreate):
    db_loan = models.DataCaptureLoan(**loan.dict())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def get_data_capture_loans(db: Session):
    return db.query(models.DataCaptureLoan).all()

def get_data_capture_loan_by_id(db: Session, loan_id: int):
    return db.query(models.DataCaptureLoan).filter(models.DataCaptureLoan.id == loan_id).first()

def update_data_capture_loan(db: Session, loan_id: int, loan_update: schemas.DataCaptureLoanCreate):
    db_loan = db.query(models.DataCaptureLoan).filter(models.DataCaptureLoan.id == loan_id).first()
    if not db_loan:
        return None
    for key, value in loan_update.dict().items():
        setattr(db_loan, key, value)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def delete_data_capture_loan(db: Session, loan_id: int):
    db_loan = db.query(models.DataCaptureLoan).filter(models.DataCaptureLoan.id == loan_id).first()
    if not db_loan:
        return False
    db.delete(db_loan)
    db.commit()
    return True

def create_it_declaration(db: Session, declaration: schemas.ITDeclarationCreate):
    db_declaration = models.ITDeclaration(**declaration.dict())
    db.add(db_declaration)
    db.commit()
    db.refresh(db_declaration)
    return db_declaration

def get_it_declarations(db: Session):
    return db.query(models.ITDeclaration).all()

def get_it_declaration_by_employee(db: Session, employee_code: str, financial_year: str):
    return db.query(models.ITDeclaration).filter(
        models.ITDeclaration.employee_code == employee_code,
        models.ITDeclaration.financial_year == financial_year
    ).first()

def update_it_declaration(db: Session, declaration_id: int, declaration_update: schemas.ITDeclarationCreate):
    db_declaration = db.query(models.ITDeclaration).filter(models.ITDeclaration.id == declaration_id).first()
    if not db_declaration:
        return None
    for key, value in declaration_update.dict().items():
        setattr(db_declaration, key, value)
    db.commit()
    db.refresh(db_declaration)
    return db_declaration

def delete_it_declaration(db: Session, declaration_id: int):
    db_declaration = db.query(models.ITDeclaration).filter(models.ITDeclaration.id == declaration_id).first()
    if not db_declaration:
        return False
    db.delete(db_declaration)
    db.commit()
    return True

def create_tds_return(db: Session, tds_return: schemas.TDSReturnCreate):
    db_tds_return = models.TDSReturn(**tds_return.dict())
    db.add(db_tds_return)
    db.commit()
    db.refresh(db_tds_return)
    return db_tds_return

def get_tds_returns(db: Session):
    return db.query(models.TDSReturn).all()

def get_tds_return_by_quarter(db: Session, financial_year: str, quarter: str):
    return db.query(models.TDSReturn).filter(
        models.TDSReturn.financial_year == financial_year,
        models.TDSReturn.quarter == quarter
    ).first()

def update_tds_return(db: Session, tds_return_id: int, tds_return_update: schemas.TDSReturnCreate):
    db_tds_return = db.query(models.TDSReturn).filter(models.TDSReturn.id == tds_return_id).first()
    if not db_tds_return:
        return None
    for key, value in tds_return_update.dict().items():
        setattr(db_tds_return, key, value)
    db.commit()
    db.refresh(db_tds_return)
    return db_tds_return

def delete_tds_return(db: Session, tds_return_id: int):
    db_tds_return = db.query(models.TDSReturn).filter(models.TDSReturn.id == tds_return_id).first()
    if not db_tds_return:
        return False
    db.delete(db_tds_return)
    db.commit()
    return True


