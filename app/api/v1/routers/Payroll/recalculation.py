from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, date, time
from typing import Optional, List
from app.database.session import get_db, SessionLocal
from app.models.payroll_models import Employee, AttendanceRecord, RecalculationLog, RecalculationRateLimit
from app.schemas.payroll_schemas import RecalculationRequest, RecalculationResponse, RecalculationStatusResponse, AttendanceDetailResponse, AttendanceRecordResponse, AttendancePostRequest

router = APIRouter(prefix="/api/recalculation", tags=["Recalculation"])

def combine_date_time(d: date, t_str: Optional[str]) -> Optional[datetime]:
    if not t_str:
        return None
    h, m = map(int, t_str.split(":"))
    return datetime.combine(d, time(hour=h, minute=m))

def process_recalculation(recalc_id: int, date_from: date, date_to: date, all_employees: bool, employee_id: Optional[int] = None):
    db = SessionLocal()
    try:
        log = db.query(RecalculationLog).filter(RecalculationLog.id == recalc_id).first()
        if not log:
            return
        employees = db.query(Employee).filter(Employee.is_active == True).all() if all_employees else db.query(Employee).filter(Employee.id == employee_id).all()
        total_employees = len(employees)
        records_processed = 0
        records_updated = 0
        for idx, emp in enumerate(employees, start=1):
            attendance_records = db.query(AttendanceRecord).filter(
                AttendanceRecord.employee_id == emp.id,
                AttendanceRecord.date >= date_from,
                AttendanceRecord.date <= date_to
            ).all()
            for record in attendance_records:
                if record.check_in and record.check_out:
                    diff_hours = (record.check_out - record.check_in).total_seconds() / 3600
                    record.hours_worked = round(diff_hours, 2)
                    record.status = "Present" if diff_hours >= 4 else "Half Day"
                    records_updated += 1
                else:
                    record.hours_worked = 0
                    record.status = "Absent"
                records_processed += 1
            log.progress = int((idx / total_employees) * 100) if total_employees else 100
            db.commit()
        log.status = "completed"
        log.records_processed = records_processed
        log.records_updated = records_updated
        log.progress = 100
        log.completed_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        log.status = f"failed: {str(e)}"
        db.commit()
    finally:
        db.close()

@router.post("/start", response_model=RecalculationResponse)
async def start_recalculation(request: RecalculationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if request.date_from > request.date_to:
        raise HTTPException(status_code=400, detail="Invalid date range")
    if not request.all_employees:
        if not request.employee_id:
            raise HTTPException(status_code=400, detail="Employee ID required")
        employee = db.query(Employee).filter(Employee.id == request.employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
    recalc_log = RecalculationLog(
        date_from=request.date_from,
        date_to=request.date_to,
        employee_id=request.employee_id,
        all_employees=request.all_employees,
        status="started",
        progress=0,
    )
    db.add(recalc_log)
    db.commit()
    db.refresh(recalc_log)
    if request.all_employees:
        db.add(RecalculationRateLimit(all_employees=True))
        db.commit()
    background_tasks.add_task(process_recalculation, recalc_log.id, request.date_from, request.date_to, request.all_employees, request.employee_id)
    return RecalculationResponse(
        id=recalc_log.id,
        status=recalc_log.status,
        progress=recalc_log.progress,
        message="Recalculation started successfully",
        records_processed=0,
        records_updated=0,
    )

@router.get("/attendance/{recalc_id}", response_model=AttendanceDetailResponse)
def get_recalculation_attendance(recalc_id: int, db: Session = Depends(get_db)):
    log = db.query(RecalculationLog).filter(RecalculationLog.id == recalc_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Recalculation log not found")
    employee_ids = [e.id for e in db.query(Employee).filter(Employee.is_active == True).all()] if log.all_employees else [log.employee_id]
    records = db.query(AttendanceRecord).filter(AttendanceRecord.employee_id.in_(employee_ids), AttendanceRecord.date >= log.date_from, AttendanceRecord.date <= log.date_to).all()
    data = []
    for record in records:
        employee = db.query(Employee).filter(Employee.id == record.employee_id).first()
        data.append({
            "id": record.id,
            "employee_id": record.employee_id,
            "employee_name": employee.name if employee else "Unknown",
            "emp_id": employee.employee_id if employee else "N/A",
            "date": record.date,
            "check_in": record.check_in.strftime("%H:%M") if record.check_in else None,
            "check_out": record.check_out.strftime("%H:%M") if record.check_out else None,
            "hours_worked": record.hours_worked,
            "status": record.status,
            "is_manual": record.is_manual
        })
    return {
        "total_records": len(data),
        "records_updated": log.records_updated or 0,
        "employees_count": len(employee_ids),
        "attendance_data": data
    }

@router.post("/", response_model=AttendanceRecordResponse)
def post_attendance(request: AttendancePostRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == request.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    def combine_date_time(d: date, t_str: Optional[str]) -> Optional[datetime]:
        if not t_str: return None
        h, m = map(int, t_str.split(":"))
        return datetime.combine(d, time(hour=h, minute=m))
    record = db.query(AttendanceRecord).filter(AttendanceRecord.employee_id == request.employee_id, AttendanceRecord.date == request.date).first()
    check_in_dt = combine_date_time(request.date, request.check_in)
    check_out_dt = combine_date_time(request.date, request.check_out)
    if not record:
        record = AttendanceRecord(employee_id=request.employee_id, date=request.date, check_in=check_in_dt, check_out=check_out_dt, is_manual=True)
        db.add(record)
    else:
        record.check_in = check_in_dt
        record.check_out = check_out_dt
        record.is_manual = True
    if record.check_in and record.check_out:
        diff_hours = (record.check_out - record.check_in).total_seconds() / 3600
        record.hours_worked = round(diff_hours, 2)
        record.status = "Present" if diff_hours >= 4 else "Half Day"
    else:
        record.hours_worked = 0
        record.status = "Absent"
    db.commit()
    db.refresh(record)
    return {
        "id": record.id,
        "employee_id": record.employee_id,
        "employee_name": employee.name,
        "emp_id": employee.employee_id,
        "date": record.date,
        "check_in": record.check_in.strftime("%H:%M") if record.check_in else None,
        "check_out": record.check_out.strftime("%H:%M") if record.check_out else None,
        "hours_worked": record.hours_worked,
        "status": record.status,
        "is_manual": record.is_manual
    }

@router.get("/status/{recalc_id}", response_model=RecalculationStatusResponse)
def get_recalculation_status(recalc_id: int, db: Session = Depends(get_db)):
    recalc_log = db.query(RecalculationLog).filter(RecalculationLog.id == recalc_id).first()
    if not recalc_log:
        raise HTTPException(status_code=404, detail="Recalculation log not found")
    return recalc_log

@router.get("/history", response_model=List[RecalculationStatusResponse])
def get_recalculation_history(limit: int = 10, db: Session = Depends(get_db)):
    logs = db.query(RecalculationLog).order_by(RecalculationLog.started_at.desc()).limit(limit).all()
    return logs
