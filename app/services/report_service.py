# app/services/report_service.py

from datetime import datetime

# ============================================================
#  AI REPORTING
# ============================================================

def generate_ai_report(query: str):
    """Mock AI report generator based on query."""
    return {
        "query": query,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "insight": f"AI analyzed data and generated insights for query: {query}",
    }


# ============================================================
# 💰 SALARY REPORTS
# ============================================================

def generate_salary_report(report_type: str):
    """Generate mock salary reports based on report type."""
    report_type = report_type.lower().replace(" ", "_")

    salary_data = {
        "salary_summary": {"total_employees": 120, "total_salary_paid": 5500000},
        "salary_register": {"month": "October", "total_salary": 1000000},
        "salary_slips": [{"employee_id": 101, "salary": 50000}, {"employee_id": 102, "salary": 60000}],
        "bank_transfer_letter": {"bank_name": "HDFC", "transfer_date": "2025-10-30"},
        "cost_to_company": {"employee_id": 101, "ctc": 700000},
        "variable_salary": {"employee_id": 102, "variable_component": 15000},
        "time_salary": {"employee_id": 103, "hours_worked": 160, "amount": 40000},
        "leave_encashment": {"employee_id": 104, "leaves_encashed": 5, "amount": 10000},
        "statutory_bonus": {"employee_id": 105, "bonus": 7500},
        "salary_deductions": {"employee_id": 106, "deductions": 2000},
        "monthly_salary_register": {"month": "September", "total": 970000},
        "employee_loans": {"employee_id": 107, "loan_amount": 50000, "emi": 5000},
        "sap_export": {"file": "salary_data_sap.csv", "status": "exported"},
    }

    return salary_data.get(report_type, {"message": "Invalid salary report type"})


# ============================================================
# ⏰ ATTENDANCE REPORTS
# ============================================================

def generate_attendance_report(report_type: str):
    """Generate mock attendance reports."""
    report_type = report_type.lower().replace(" ", "_")

    attendance_data = {
        "attendance_register": {"total_days": 26, "present": 24, "absent": 2},
        "leave_register": {"total_leaves": 120, "approved": 110, "pending": 10},
        "time_register": {"average_hours": 8.5},
        "strike_register": {"strikes": 0},
        "travel_register": {"official_trips": 15, "total_expense": 240000},
        "time_punches": [{"employee_id": 101, "punch_in": "09:00", "punch_out": "17:00"}],
        "remote_punch_address": {"employee_id": 102, "location": "Hyderabad"},
        "manual_updates": {"updated_records": 12, "approved_by": "HR Manager"},
    }

    return attendance_data.get(report_type, {"message": "Invalid attendance report type"})


# ============================================================
# 👩‍💼 EMPLOYEE REPORTS
# ============================================================

def generate_employee_report(report_type: str):
    """Generate mock employee report data based on report_type."""
    report_type = report_type.lower().replace(" ", "_")

    dummy_data = {
        "employee_register": [
            {"employee_id": 101, "name": "John Doe", "department": "HR", "status": "Active"},
            {"employee_id": 102, "name": "Jane Smith", "department": "IT", "status": "Inactive"},
        ],
        "employee_address": [
            {"employee_id": 101, "address": "Hyderabad", "city": "Hyderabad", "state": "Telangana"},
            {"employee_id": 102, "address": "Chennai", "city": "Chennai", "state": "Tamil Nadu"},
        ],
        "employee_events": [
            {"employee_id": 101, "event": "Promotion", "date": "2024-05-10"},
            {"employee_id": 102, "event": "Transfer", "date": "2023-11-20"},
        ],
        "promoting_ageing": [
            {"employee_id": 101, "years_in_role": 3, "eligible_for_promotion": True},
            {"employee_id": 102, "years_in_role": 1, "eligible_for_promotion": False},
        ],
        "increment_ageing": [
            {"employee_id": 101, "last_increment": "2023-04-01", "due_increment": "2024-04-01"},
            {"employee_id": 102, "last_increment": "2023-07-01", "due_increment": "2024-07-01"},
        ],
        "employee_joinings": [
            {"employee_id": 103, "name": "Rajesh Kumar", "joining_date": "2024-09-15"},
        ],
        "employee_exits": [
            {"employee_id": 104, "name": "Suresh Reddy", "exit_date": "2024-02-28"},
        ],
        "vaccination_status": [
            {"employee_id": 101, "vaccinated": True},
            {"employee_id": 102, "vaccinated": False},
        ],
        "workman_status": [
            {"employee_id": 101, "is_workman": False},
            {"employee_id": 102, "is_workman": True},
        ],
        "employee_assets": [
            {"employee_id": 101, "asset": "Laptop", "issued_date": "2023-09-15"},
        ],
        "employee_relatives": [
            {"employee_id": 101, "relative_name": "Anita Doe", "relation": "Spouse"},
        ],
        "inactive_employees": [
            {"employee_id": 102, "name": "Jane Smith", "status": "Inactive"},
        ],
        "export_records": [
            {"export_id": 1, "file_name": "employee_data.csv", "export_date": "2025-10-30"},
        ],
    }

    return dummy_data.get(report_type, {"message": "Invalid employee report type"})


# ============================================================
# 🧾 STATUTORY REPORTS
# ============================================================

def generate_statutory_report(report_type: str):
    """Generate mock statutory report data."""
    report_type = report_type.lower().replace(" ", "_")

    data = {
        "esi_deduction": {"month": "October", "total_deduction": 52000},
        "esi_coverage": {"total_employees": 80},
        "pf_deduction": {"month": "October", "total_pf": 140000},
        "pf_coverage": {"total_pf_members": 90},
        "over_time_register": {"month": "October", "total_ot_hours": 220},
        "register_of_leaves": {"month": "October", "leaves_taken": 150},
        "it_deduction": {"month": "October", "total_it": 300000},
        "it_declarations": {"employees_submitted": 110},
        "it_computation": {"month": "October", "computed_for": 120},
        "labour_welfare_fund": {"total_amount": 25000},
        "tds_return": {"quarter": "Q2", "status": "Filed"},
        "itform_16": {"generated_for": 120},
    }

    return data.get(report_type, {"message": "Invalid statutory report type"})


# ============================================================
# 📆 ANNUAL REPORTS
# ============================================================

def generate_annual_report(report_type: str):
    """Generate mock annual report data."""
    report_type = report_type.lower().replace(" ", "_")

    data = {
        "annual_salary_summary": {"year": 2025, "total_paid": 65000000},
        "annual_salary_statement": {"year": 2025, "employees": 125, "avg_salary": 520000},
        "annual_attendance": {"year": 2025, "avg_present_days": 250},
        "annual_leaves": {"year": 2025, "total_leaves": 1500},
    }

    return data.get(report_type, {"message": "Invalid annual report type"})


# ============================================================
# 📋 OTHER REPORTS
# ============================================================

def generate_other_report(report_type: str):
    """Generate mock 'other' reports (like activity logs)."""
    report_type = report_type.lower().replace(" ", "_")

    data = {
        "activity_logs": [
            {"user": "Admin", "action": "Login", "timestamp": "2025-10-30 09:00"},
            {"user": "HR", "action": "Generated Report", "timestamp": "2025-10-30 09:30"},
        ]
    }

    return data.get(report_type, {"message": "Invalid report type"})
