from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from app.database.session import get_db
from app.models.payroll_models import PayrollRun
from app.schemas.payroll_schemas import PayrollRunCreate, PayrollRunResponse, PayrollChartResponse
from app.utils.helpers import log_message,generate_chart_data


router = APIRouter(prefix="/api/runpayroll", tags=["Run Payroll"])


# ============================================================
# 📊 PAYROLL CHART DATA
# ============================================================
@router.get("/chart", response_model=PayrollChartResponse)
async def get_chart_data(db: Session = Depends(get_db)):
    """Generate payroll chart data"""
    runs = db.query(PayrollRun).order_by(PayrollRun.run_date).all()
    return generate_chart_data(runs)


# ============================================================
# 🧾 DOWNLOAD LOGS
# ============================================================
@router.get("/logs/{period}")
async def get_logs(period: str):
    """Simulate payroll log download"""
    log_message(f"Log requested for {period}")
    return {"message": f"Logs downloaded for {period}"}


# ============================================================
# 🧾 CREATE A NEW PAYROLL RUN
# ============================================================
@router.post("/", response_model=PayrollRunResponse)
def create_run(run_in: PayrollRunCreate, db: Session = Depends(get_db)):
    """Create a new payroll run"""
    run = PayrollRun(
        period=run_in.period,
        run_date=datetime.utcnow(),
        runtime="manual",
        result="success",
        total_net_payroll=run_in.total_net_payroll,
        status="completed"
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


# ============================================================
# 📋 LIST ALL PAYROLL RUNS
# ============================================================
@router.get("/", response_model=List[PayrollRunResponse])
def list_runs(db: Session = Depends(get_db)):
    """List all payroll runs (latest first)"""
    return db.query(PayrollRun).order_by(PayrollRun.id.desc()).all()


# ============================================================
# 🔍 GET PAYROLL RUN DETAILS
# ============================================================
@router.get("/{run_id}", response_model=PayrollRunResponse)
def get_run(run_id: int, db: Session = Depends(get_db)):
    """Get payroll run details by ID"""
    run = db.query(PayrollRun).filter(PayrollRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run
