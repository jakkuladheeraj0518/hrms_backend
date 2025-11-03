from sqlalchemy.orm import Session
from app.repositories import separation_repo
from app.schemas import separation_schema


def initiate_exit(db: Session, data: separation_schema.InitiatedExitCreate):
    """Create a new initiated exit record."""
    return separation_repo.create_initiated_exit(db, data)


def fetch_pending_exits(db: Session):
    """
    Retrieve all pending exit requests that are not yet approved or completed.
    """
    rows = separation_repo.get_pending_exits(db)
    return [
        separation_schema.PendingExitItem(
            id=r.id,
            employee_name=r.employee_name,
            exit_date=None,
            exit_reason=r.reason_of_exit,
            status="Pending",
        )
        for r in rows
    ]


def fetch_ex_employees(db: Session):
    """
    Retrieve all employees who have completed their exit process.
    """
    rows = separation_repo.get_ex_employees(db)
    return [
        separation_schema.ExEmployeeItem(
            id=r.id,
            employee_name=r.employee_name,
            employee_code=r.employee_code,
            exit_date=r.exit_date,
            reason_of_exit=r.reason_of_exit,
            remarks=r.remarks,
        )
        for r in rows
    ]


def dashboard_data(db: Session):
    """
    Fetch summarized data for the separation dashboard,
    including total separations, pending exits, and completed exits.
    """
    return separation_repo.get_dashboard_stats(db)


def fetch_all_exits(db: Session):
    """
    Retrieve all exit records (pending + completed).
    Useful for admin-level views or reports.
    """
    return separation_repo.get_all_exits(db)


def get_all_exits(db: Session):
    """Alias used by router; returns all exit records."""
    return separation_repo.get_all_exits(db)