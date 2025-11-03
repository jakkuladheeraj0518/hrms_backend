from fastapi import APIRouter
from typing import List
from app.schemas import report_schema as rs

router = APIRouter(prefix="/reports/salary", tags=["Salary Reports"])


# Salary Summary
@router.get("/salary_summary", response_model=List[rs.SalarySummaryResponse])
def list_salary_summary():
    return [
        {
            "id": 1,
            "period": "SEP-2025",
            "sn": 1,
            "cost_center": "CC1",
            "employees": "John Doe",
            "pay_days": 26,
            "earnings": 50000.0,
            "deductions": 2000.0,
            "net_salary": 48000.0
        }
    ]


@router.get("/salary_register", response_model=List[rs.SalaryRegisterConfigResponse])
def list_salary_register_configs():
    return [{"id": 1}]


@router.get("/salary_slips", response_model=List[rs.SalarySlipsConfigResponse])
def list_salary_slips_configs():
    return [{"id": 1}]


@router.get("/bank_transfer_letter", response_model=List[rs.BankTransferRowResponse])
def list_bank_transfer_rows():
    return [
        {
            "id": 1,
            "business_unit": "BU1",
            "location": "LOC1",
            "cost_center": "CC1",
            "employee_code": "E001",
            "employee_name": "John",
            "bank_ifsc": "IFSC000",
            "bank_name": "Bank",
            "bank_account": "123",
            "net_amount": 48000.0
        }
    ]


@router.get("/cost_to_company", response_model=List[rs.CostToCompanyResponse])
def list_cost_to_company():
    return [
        {
            "id": 1,
            "sn": 1,
            "location": "LOC1",
            "cost_center": "CC1",
            "employee_code": "E001",
            "employee_name": "John",
            "employer_cost": 600000.0
        }
    ]


@router.get("/variable_salary", response_model=List[rs.VariableSalaryResponse])
def list_variable_salary():
    return [
        {
            "id": 1,
            "sn": 1,
            "location": "LOC1",
            "employee_name": "John",
            "salary_component": "Bonus",
            "amount": 5000.0
        }
    ]


@router.get("/time_salary", response_model=List[rs.VariableSalaryResponse])
def list_time_salary():
    return [
        {
            "id": 2,
            "sn": 1,
            "location": "LOC1",
            "employee_name": "John",
            "salary_component": "Hourly",
            "hours": 10,
            "rate": 200.0,
            "amount": 2000.0
        }
    ]


@router.get("/leave_encashment", response_model=List[rs.LeaveRegisterResponse])
def list_leave_encashment():
    return [
        {"id": 1, "employee_name": "John", "employee_code": "E001", "date": None}
    ]


@router.get("/statutory_bonus", response_model=List[rs.StatutoryBonusResponse])
def list_statutory_bonus():
    return [
        {"id": 1, "employee_name": "John", "bonus": 10000.0}
    ]


@router.get("/salary_deductions", response_model=List[rs.SalaryDeductionResponse])
def list_salary_deductions():
    return [
        {"id": 1, "employee_name": "John", "amount": 2000.0}
    ]


@router.get("/monthly_salary_register", response_model=List[rs.SalarySummaryResponse])
def monthly_salary_register():
    return [
        {"id": 1, "period": "SEP-2025", "employees": "John"}
    ]


@router.get("/employee_loans", response_model=List[rs.EmployeeLoanResponse])
def list_employee_loans():
    return [
        {"id": 1, "employee_name": "John", "loan_amount": 50000.0, "balance": 30000.0}
    ]


@router.get("/sap_export", response_model=List[rs.SAPExportResponse])
def list_sap_export():
    return [
        {"id": 1, "period": "SEP-2025", "format": "XML"}
    ]

