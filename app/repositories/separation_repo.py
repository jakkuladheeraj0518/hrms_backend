from sqlalchemy.orm import Session
from app.models.separation import InitiatedExit, PendingExit, ExEmployee
from app.schemas.separation_schema import InitiatedExitCreate


def create_initiated_exit(db: Session, data: InitiatedExitCreate):
    row = InitiatedExit(
        employee_name=data.employee_name,
        employee_code=data.employee_code,
        resignation_date=data.resignation_date,
        notice_period=data.notice_period,
        last_working_date=data.last_working_date,
        reason_of_exit=data.reason_of_exit,
        remarks=data.remarks,
        trying_to_retain=data.trying_to_retain if data.trying_to_retain is not None else False,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_pending_exits(db: Session):
    # If a separate table is later populated, switch to PendingExit. For now, use InitiatedExit as source.
    return db.query(InitiatedExit).all()


def get_ex_employees(db: Session):
    return db.query(ExEmployee).all()


def get_dashboard_stats(db: Session):
    total = db.query(InitiatedExit).count()
    pending = db.query(InitiatedExit).count()
    completed = db.query(ExEmployee).count()
    return {"total": total, "pending": pending, "completed": completed}


def get_all_exits(db: Session):
    return db.query(InitiatedExit).all()
