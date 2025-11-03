from fastapi import APIRouter
from typing import List
from app.schemas import report_schema as rs
from datetime import date

router = APIRouter(prefix="/reports/statutory", tags=["Statutory Reports"])


@router.get("/esi_deduction", response_model=List[rs.ESIDeductionResponse])
def list_esi_deduction():
    return [{"id": 1, "employee_name": "John", "esi_amount": 500.0}]


@router.get("/esi_coverage", response_model=List[rs.ESICoverageResponse])
def list_esi_coverage():
    return [{"id": 1, "employee_name": "John", "coverage_start": None, "coverage_end": None}]


@router.get("/pf_deduction", response_model=List[rs.PFDeductionResponse])
def list_pf_deduction():
    return [{"id": 1, "employee_name": "John", "pf_amount": 1500.0}]


@router.get("/pf_coverage", response_model=List[rs.PFCoverageResponse])
def list_pf_coverage():
    return [{"id": 1, "employee_name": "John"}]


@router.get("/overtime_register", response_model=List[rs.OvertimeRegisterResponse])
def list_overtime_register():
    return [{"id": 1, "employee_name": "John", "ot_hours": 2.5}]


@router.get("/register_of_leaves", response_model=List[rs.RegisterOfLeavesResponse])
def list_register_of_leaves():
    return [{"id": 1, "location": "LOC1", "year": 2025}]


@router.get("/it_declarations", response_model=List[rs.IncomeTaxDeclarationResponse])
def list_it_declarations():
    return [{"id": 1, "employee_name": "John", "pan_no": "ABCDE1234F"}]


@router.get("/it_computation", response_model=List[rs.IncomeTaxComputationResponse])
def list_it_computation():
    return [{"id": 1, "description": "Computation run", "download_status": "Pending"}]


@router.get("/labour_welfare_fund", response_model=List[rs.LabourWelfareFundResponse])
def list_labour_welfare_fund():
    return [{"id": 1, "employee_name": "John", "contribution": 100.0}]


@router.get("/tds_return", response_model=List[rs.TDSReturnResponse])
def list_tds_return():
    return [{"id": 1, "return_period_year": 2025, "return_period_quarter": "Q2"}]


@router.get("/form16", response_model=List[rs.Form16Response])
def list_form16():
    return [{"id": 1, "financial_year": "2024-25", "employee_id": 1}]
