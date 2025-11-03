from fastapi import APIRouter
from typing import List
from app.schemas import report_schema as rs

router = APIRouter(prefix="/reports/employee", tags=["Employee Reports"])


@router.get("/employee_register", response_model=List[rs.EmployeeResponse])
def list_employees():
    return [{"id": 1, "employee_code": "E001", "employee_name": "John"}]


@router.get("/employee_address", response_model=List[rs.EmployeeAddressResponse])
def list_employee_addresses():
    return [{"id": 1, "employee_id": 1, "address_line_1": "123 Main St"}]


@router.get("/employee_events", response_model=List[rs.EmployeeEventResponse])
def list_employee_events():
    return [{"id": 1, "employee_id": 1, "event_type": "Birthday"}]


@router.get("/promotion_ageing", response_model=List[rs.PromotionAgeingResponse])
def list_promotion_ageing():
    return [{"id": 1, "employee_id": 1, "ageing": "2 years"}]


@router.get("/increment_ageing", response_model=List[rs.IncrementAgeingResponse])
def list_increment_ageing():
    return [{"id": 1, "employee_id": 1, "ageing": "1 year"}]


@router.get("/employee_joinings", response_model=List[rs.EmployeeJoiningResponse])
def list_employee_joinings():
    return [{"id": 1, "employee_id": 1, "joining_date": None}]


@router.get("/employee_exits", response_model=List[rs.EmployeeExitResponse])
def list_employee_exits():
    return [{"id": 1, "employee_id": 1, "reason_of_exit": "Resigned"}]


@router.get("/vaccination_status", response_model=List[rs.VaccinationStatusResponse])
def list_vaccination_status():
    return [{"id": 1, "employee_name": "John", "vaccine_name": "Covishield"}]


@router.get("/workman_status", response_model=List[rs.WorkmanStatusResponse])
def list_workman_status():
    return [{"id": 1, "employee_name": "John", "workman_type": "TypeA"}]


@router.get("/employee_assets", response_model=List[rs.EmployeeAssetsResponse])
def list_employee_assets():
    return [{"id": 1, "employee_name": "John", "asset_name": "Laptop"}]


@router.get("/employee_relatives", response_model=List[rs.EmployeeRelativesResponse])
def list_employee_relatives():
    return [{"id": 1, "employee_name": "John", "relation_name": "Jane"}]


@router.get("/inactive_employees", response_model=List[rs.InactiveEmployeesResponse])
def list_inactive_employees():
    return [{"id": 1, "employee_name": "John", "reason": "Left"}]


@router.get("/export_records", response_model=List[rs.ActivityLogResponse])
def list_export_records():
    return [{"id": 1, "user_name": "admin", "action": "export"}]
