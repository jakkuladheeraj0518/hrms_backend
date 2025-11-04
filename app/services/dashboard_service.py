"""
Dashboard service layer
Contains business logic for dashboard operations
"""
from typing import Optional
from datetime import date, timedelta
import json
from sqlalchemy.orm import Session

from models.employee import Employee, Birthday
from models.attendance import AttendanceRecord, FlightRiskAssessment
from models.lead import Lead
from models.subscription import Subscription
from models.notification import Notification, Activity, OpenRequest


class DashboardService:
    """Dashboard service for handling dashboard business logic"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_overview_data(self):
        """Get overview dashboard data"""
        # Get employee statistics
        total_employees = self.db.query(Employee).count()
        active_employees = self.db.query(Employee).filter(Employee.is_active == True).count()
        inactive_employees = total_employees - active_employees
        active_mobile_users = self.db.query(Employee).filter(Employee.is_mobile_user == True).count()
        
        # Get subscription info
        subscription = self.db.query(Subscription).filter(Subscription.status == "Active").first()
        subscription_status = "Active" if subscription else "Inactive"
        subscription_due_date = subscription.end_date.strftime("%b %d, %Y") if subscription else None
        
        stats = {
            "total_employees": total_employees,
            "active_employees": active_employees,
            "inactive_employees": inactive_employees,
            "active_mobile_users": active_mobile_users,
            "subscription_status": subscription_status,
            "subscription_due_date": subscription_due_date
        }
        
        # Enhanced card data for frontend
        summary_cards = [
            {
                "title": "Employees",
                "value": total_employees,
                "subtitle": f"{active_employees} of {total_employees} active ({inactive_employees} inactive)",
                "icon": "bi-people",
                "color": "success",
                "progress": int((active_employees / total_employees * 100)) if total_employees > 0 else 0
            },
            {
                "title": "ACTIVE MOBILE USERS", 
                "value": active_mobile_users,
                "subtitle": f"{active_mobile_users} of {total_employees} active ({total_employees - active_mobile_users} inactive)",
                "icon": "bi-phone",
                "color": "info",
                "progress": int((active_mobile_users / total_employees * 100)) if total_employees > 0 else 0
            },
            {
                "title": "SUBSCRIPTION",
                "value": subscription.total_employees if subscription else 0,
                "subtitle": f"Due by {subscription_due_date}" if subscription_due_date else "No active subscription",
                "icon": "bi-hourglass-split",
                "color": "warning",
                "progress": 90 if subscription else 0
            }
        ]
        
        # Get attendance trend data for the year
        attendance_trend = []
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        for i, month in enumerate(months, 1):
            # Calculate attendance for each month
            month_start = date(2025, i, 1)
            if i == 12:
                month_end = date(2025, 12, 31)
            else:
                month_end = date(2025, i + 1, 1) - timedelta(days=1)
            
            presents = self.db.query(AttendanceRecord).filter(
                AttendanceRecord.date >= month_start,
                AttendanceRecord.date <= month_end,
                AttendanceRecord.status == "Present"
            ).count()
            
            absents = self.db.query(AttendanceRecord).filter(
                AttendanceRecord.date >= month_start,
                AttendanceRecord.date <= month_end,
                AttendanceRecord.status == "Absent"
            ).count()
            
            leaves = self.db.query(AttendanceRecord).filter(
                AttendanceRecord.date >= month_start,
                AttendanceRecord.date <= month_end,
                AttendanceRecord.status == "Leave"
            ).count()
            
            attendance_trend.append({
                "month": month,
                "presents": presents,
                "absents": absents,
                "leaves": leaves
            })
        
        # Get open requests data from database
        open_requests_db = self.db.query(OpenRequest).all()
        open_requests = []
        for req in open_requests_db:
            open_requests.append({
                "type": req.request_type,
                "count": req.count,
                "icon": req.icon,
                "color": req.color
            })
        
        # Fallback to hardcoded data if no database records
        if not open_requests:
            open_requests = [
                {"type": "Miscellaneous", "count": 20, "icon": "ti-calendar", "color": "danger"},
                {"type": "Time Relaxation", "count": 10, "icon": "ti-clock", "color": "info"},
                {"type": "Comp Off", "count": 6, "icon": "ti-calendar-off", "color": "primary"},
                {"type": "Leaves", "count": 3, "icon": "ti-calendar-event", "color": "primary"},
                {"type": "Shift Allocation", "count": 3, "icon": "ti-users", "color": "primary"},
                {"type": "Wallet or Voucher", "count": 2, "icon": "ti-wallet", "color": "primary"},
                {"type": "Salary Exemption", "count": 1, "icon": "ti-currency-dollar", "color": "primary"},
                {"type": "Claims", "count": 2, "icon": "ti-receipt", "color": "primary"},
                {"type": "Help Desk", "count": 2, "icon": "ti-help", "color": "primary"},
                {"type": "Work Flow", "count": 1, "icon": "ti-workflow", "color": "primary"}
            ]
        
        # Get birthdays data from database
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        birthdays_db = self.db.query(Birthday, Employee).join(Employee).filter(
            Birthday.birth_date.in_([today, tomorrow, date(2025, 1, 25)])
        ).all()
        
        birthdays = []
        for birthday, employee in birthdays_db:
            if birthday.birth_date == today:
                date_str = "Today"
            elif birthday.birth_date == tomorrow:
                date_str = "Tomorrow"
            else:
                date_str = birthday.birth_date.strftime("%d %b %Y")
                
            birthdays.append({
                "name": employee.name,
                "department": employee.department,
                "date": date_str,
                "avatar": employee.profile_picture or "/assets/img/users/user-default.jpg",
                "action": "Send"
            })
        
        # Fallback to hardcoded data if no database records
        if not birthdays:
            birthdays = [
                {"name": "Andrew Jermia", "department": "IT", "date": "Today", "avatar": "/assets/img/users/user-01.jpg", "action": "Send"},
                {"name": "Mary Zeen", "department": "HR", "date": "Tomorrow", "avatar": "/assets/img/users/user-02.jpg", "action": "Send"},
                {"name": "Antony Lewis", "department": "Finance", "date": "25 Jan 2025", "avatar": "/assets/img/users/user-03.jpg", "action": "Send"},
                {"name": "Douglas Martini", "department": "Operations", "date": "25 Jan 2025", "avatar": "/assets/img/users/user-04.jpg", "action": "Send"}
            ]
        
        return {
            "stats": stats,
            "summary_cards": summary_cards,
            "attendance_trend": attendance_trend,
            "open_requests": open_requests,
            "birthdays": birthdays
        }
    
    async def get_attendance_data(self, start_date: Optional[date] = None, end_date: Optional[date] = None, 
                                department: Optional[str] = None, status: Optional[str] = None, 
                                sort_by: Optional[str] = "Recently Added"):
        """Get attendance dashboard data with filtering options"""
        # Implementation would go here - keeping it simple for now
        return {"message": "Attendance data - implementation in progress"}
    
    async def get_flight_risk_data(self, viewing: Optional[str] = None):
        """Get flight risk dashboard data"""
        # Implementation would go here - keeping it simple for now
        return {"message": "Flight risk data - implementation in progress"}
    
    async def get_leads_data(self, start_date: Optional[date] = None, end_date: Optional[date] = None):
        """Get leads dashboard data"""
        # Implementation would go here - keeping it simple for now
        return {"message": "Leads data - implementation in progress"}