# app/utils/report_util.py
from datetime import datetime, timedelta
import random

# ==============================================================
# 🧠 1️⃣ AI REPORT UTILITIES
# ==============================================================

def generate_ai_response(query: str) -> str:
    """
    Simulate AI-generated responses for analytics or HR queries.
    """
    query = query.lower()

    if "revenue" in query:
        return "📈 The total revenue for this quarter increased by 15%."
    elif "employee" in query:
        return "👨‍💼 The total number of employees increased by 8% this year."
    elif "attendance" in query:
        return "🕒 The overall attendance rate this month is 92%."
    elif "salary" in query:
        return "💰 The average salary increased by 10% this financial year."
    elif "hostel" in query:
        return "🏢 All hostels are operating at around 90% occupancy."
    else:
        return f"🤖 AI could not find relevant data for query: '{query}'."


# ==============================================================
# 💰 2️⃣ SALARY REPORT UTILITIES
# ==============================================================

def generate_salary_report_content(report_type: str):
    """
    Generate mock salary-related reports for HR analytics.
    """
    month = datetime.now().strftime("%B %Y")
    report_type = report_type.lower()

    if report_type == "summary":
        return {
            "report_name": "Salary Summary Report",
            "period": month,
            "total_employees": 3,
            "total_salary_paid": 180000,
            "average_salary": 60000,
        }

    elif report_type == "register":
        return {
            "report_name": "Salary Register",
            "period": month,
            "employees": [
                {"name": "John", "gross_salary": 50000, "net_salary": 45000},
                {"name": "Sara", "gross_salary": 60000, "net_salary": 54000},
                {"name": "Kiran", "gross_salary": 70000, "net_salary": 63000},
            ],
        }

    elif report_type == "deductions":
        return {
            "report_name": "Salary Deductions Report",
            "period": month,
            "employees": [
                {"name": "John", "pf": 1800, "esi": 500, "tax": 2000},
                {"name": "Sara", "pf": 2000, "esi": 600, "tax": 2500},
                {"name": "Kiran", "pf": 2200, "esi": 700, "tax": 2700},
            ],
        }

    elif report_type == "ctc":
        return {
            "report_name": "Cost to Company (CTC)",
            "employees": [
                {"name": "John", "ctc": 600000},
                {"name": "Sara", "ctc": 720000},
                {"name": "Kiran", "ctc": 850000},
            ],
        }

    else:
        return {"message": f"No salary report generator found for: {report_type}"}


# ==============================================================
# 🕒 3️⃣ ATTENDANCE REPORT UTILITIES
# ==============================================================

def generate_attendance_report_content(report_type: str):
    """
    Generate mock attendance data for daily, weekly, or monthly reports.
    """
    today = datetime.today()
    report_type = report_type.lower()

    if report_type == "daily":
        days = [today]
    elif report_type == "weekly":
        days = [today - timedelta(days=i) for i in range(7)]
    else:
        days = [today - timedelta(days=i) for i in range(30)]

    records = []
    for date in days:
        records.append({
            "date": date.strftime("%Y-%m-%d"),
            "present": random.randint(80, 100),
            "absent": random.randint(0, 10),
            "on_leave": random.randint(0, 5),
        })

    return {
        "report_name": f"{report_type.capitalize()} Attendance Report",
        "period_start": days[-1].strftime("%Y-%m-%d"),
        "period_end": days[0].strftime("%Y-%m-%d"),
        "summary": {
            "avg_present": round(sum(r["present"] for r in records) / len(records), 2),
            "avg_absent": round(sum(r["absent"] for r in records) / len(records), 2),
            "avg_on_leave": round(sum(r["on_leave"] for r in records) / len(records), 2),
        },
        "records": records,
    }


# ==============================================================
# 👨‍💼 4️⃣ EMPLOYEE REPORT UTILITIES
# ==============================================================

def generate_employee_report(report_type: str):
    """
    Generate mock employee-related reports (performance, headcount, etc.)
    """
    report_type = report_type.lower()

    if report_type == "headcount":
        return {
            "report_name": "Employee Headcount Report",
            "total_employees": 150,
            "departments": {
                "HR": 10,
                "Finance": 15,
                "Engineering": 100,
                "Support": 25,
            },
        }

    elif report_type == "performance":
        return {
            "report_name": "Employee Performance Summary",
            "high_performers": 25,
            "average_performers": 100,
            "low_performers": 25,
            "remarks": "Overall employee performance has improved by 7% this quarter.",
        }

    elif report_type == "attrition":
        return {
            "report_name": "Attrition Report",
            "period": datetime.now().strftime("%B %Y"),
            "total_exits": 5,
            "exit_reasons": {
                "Better Opportunity": 3,
                "Relocation": 1,
                "Personal": 1,
            },
        }

    else:
        return {"message": f"No employee report generator found for: {report_type}"}


# ==============================================================
# 🧾 5️⃣ STATUTORY REPORT UTILITIES
# ==============================================================

def generate_statutory_summary(category: str):
    """
    Generate mock statutory report summary for PF, ESI, TDS, etc.
    """
    category = category.lower()
    employees = random.randint(50, 200)

    if category == "pf":
        return {
            "category": "Provident Fund (PF)",
            "total_employees": employees,
            "pf_detected": employees - random.randint(0, 10),
            "description": "Monthly PF contribution compliance summary.",
        }

    elif category == "esi":
        return {
            "category": "Employee State Insurance (ESI)",
            "total_employees": employees,
            "pf_detected": employees - random.randint(0, 20),
            "description": "ESI deduction and submission report for the current month.",
        }

    elif category == "tds":
        return {
            "category": "Tax Deducted at Source (TDS)",
            "total_employees": employees,
            "pf_detected": employees - random.randint(0, 5),
            "description": "Summary of TDS deductions submitted to Income Tax department.",
        }

    else:
        return {"message": f"No statutory report generator found for: {category}"}
