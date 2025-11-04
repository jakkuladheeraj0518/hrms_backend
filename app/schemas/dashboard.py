"""
Dashboard schemas for request/response validation
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date


class SummaryCard(BaseModel):
    """Schema for summary card"""
    title: str
    value: int
    subtitle: str
    icon: str
    color: str
    progress: int


class ChartData(BaseModel):
    """Schema for chart data"""
    labels: List[str]
    data: List[int]
    colors: List[str]


class AttendanceTrendChart(BaseModel):
    """Schema for attendance trend chart"""
    labels: List[str]
    datasets: List[Dict[str, Any]]


class BirthdayGroup(BaseModel):
    """Schema for birthday group"""
    dateLabel: str
    people: List[Dict[str, str]]


class OverviewDashboard(BaseModel):
    """Schema for overview dashboard response"""
    summary_cards: List[SummaryCard]
    attendance_trend: AttendanceTrendChart
    open_requests: List[Dict[str, Any]]
    birthdays: List[BirthdayGroup]
    stats: Dict[str, Any]


class EmployeeAttendance(BaseModel):
    """Schema for employee attendance"""
    id: int
    name: str
    avatar: str
    department: str
    designation: str
    shift: str
    time_in: str
    time_out: str
    status: str
    status_class: str
    is_late: bool
    is_early_out: bool


class AttendanceCharts(BaseModel):
    """Schema for attendance charts"""
    attendance: ChartData
    late_comers: ChartData
    early_goers: ChartData


class FilterOptions(BaseModel):
    """Schema for filter options"""
    departments: List[str]
    statuses: List[str]
    sort_options: List[str]


class AttendanceSummary(BaseModel):
    """Schema for attendance summary"""
    total_employees: int
    present: int
    absent: int
    on_leave: int
    late_comers: int
    early_goers: int
    date: str


class AttendanceDashboardResponse(BaseModel):
    """Schema for attendance dashboard response"""
    status: str
    charts: AttendanceCharts
    absent_employees: List[EmployeeAttendance]
    present_employees: List[EmployeeAttendance]
    filter_options: FilterOptions
    summary: AttendanceSummary


class FlightRiskEmployee(BaseModel):
    """Schema for flight risk employee"""
    id: str
    name: str
    deputation: str
    dept: str
    last_updated: str
    risk_percent: str
    risk_status: str
    actions: str
    picture: str
    risk_signals: List[str]


class FlightRiskCounts(BaseModel):
    """Schema for flight risk counts"""
    untracked: int
    uncalculated: int
    no_risk: int
    moderate_risk: int
    high_risk: int


class FlightRiskEmployees(BaseModel):
    """Schema for flight risk employees by category"""
    untracked: List[FlightRiskEmployee]
    uncalculated: List[FlightRiskEmployee]
    no_risk: List[FlightRiskEmployee]
    moderate_risk: List[FlightRiskEmployee]
    high_risk: List[FlightRiskEmployee]


class FlightRiskSummary(BaseModel):
    """Schema for flight risk summary"""
    total_employees: int
    tracked_employees: int
    untracked_employees: int
    uncalculated_employees: int


class FlightRiskDashboardResponse(BaseModel):
    """Schema for flight risk dashboard response"""
    status: str
    counts: FlightRiskCounts
    employees: FlightRiskEmployees
    summary: FlightRiskSummary


class HeatmapData(BaseModel):
    """Schema for heatmap data"""
    This_Week: List[List[str]] = []
    This_Month: List[List[str]] = []
    This_Year: List[List[str]] = []

    class Config:
        # Allow field names with spaces/special chars
        populate_by_name = True
        alias_generator = lambda field_name: field_name.replace('_', ' ')


class LeadsDashboardResponse(BaseModel):
    """Schema for leads dashboard response"""
    status: str
    summary_cards: List[SummaryCard]
    attendance_trend: Dict[str, Any]
    new_leads_heatmap: Dict[str, List[List[str]]]
    lost_leads_chart: Dict[str, Any]
    leads_by_companies: List[Dict[str, Any]]
    leads_by_source: Dict[str, Any]
    recent_follow_up: List[Dict[str, Any]]
    recent_activities: List[Dict[str, Any]]
    notifications: List[Dict[str, Any]]
    top_countries: Dict[str, Any]
    recent_leads: List[Dict[str, Any]]
    summary: Dict[str, Any]


class DashboardStats(BaseModel):
    """Schema for general dashboard statistics"""
    total_employees: int
    active_employees: int
    total_leads: int
    conversion_rate: float
    active_subscriptions: int
    pending_requests: int




    ---------------------------------



    """
Attendance schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class AttendanceStatus(str, Enum):
    """Attendance status enum"""
    PRESENT = "Present"
    ABSENT = "Absent"
    LEAVE = "Leave"
    WEEKOFF = "WeekOff"
    HOLIDAY = "Holiday"


class AttendanceRecordBase(BaseModel):
    """Base attendance record schema"""
    employee_id: int
    date: date
    time_in: Optional[str] = None
    time_out: Optional[str] = None
    status: AttendanceStatus
    is_late: bool = False
    is_early_out: bool = False


class AttendanceRecordCreate(AttendanceRecordBase):
    """Schema for creating attendance record"""
    pass


class AttendanceRecordUpdate(BaseModel):
    """Schema for updating attendance record"""
    time_in: Optional[str] = None
    time_out: Optional[str] = None
    status: Optional[AttendanceStatus] = None
    is_late: Optional[bool] = None
    is_early_out: Optional[bool] = None


class AttendanceRecord(AttendanceRecordBase):
    """Schema for attendance record response"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AttendanceChartData(BaseModel):
    """Schema for attendance chart data"""
    labels: List[str]
    data: List[int]
    colors: List[str]


class AttendanceStats(BaseModel):
    """Schema for attendance statistics"""
    total_employees: int
    present: int
    absent: int
    on_leave: int
    late_comers: int
    early_goers: int
    date: str


class AttendanceDashboard(BaseModel):
    """Schema for attendance dashboard response"""
    status: str
    charts: dict
    absent_employees: List[dict]
    present_employees: List[dict]
    filter_options: dict
    summary: AttendanceStats


class FlightRiskLevel(str, Enum):
    """Flight risk level enum"""
    NO_RISK = "No Risk"
    MODERATE_RISK = "Moderate Risk"
    HIGH_RISK = "High Risk"


class FlightRiskAssessmentBase(BaseModel):
    """Base flight risk assessment schema"""
    employee_id: int
    risk_score: float
    risk_level: FlightRiskLevel
    risk_signals: Optional[str] = None
    is_tracked: bool = True


class FlightRiskAssessmentCreate(FlightRiskAssessmentBase):
    """Schema for creating flight risk assessment"""
    pass


class FlightRiskAssessmentUpdate(BaseModel):
    """Schema for updating flight risk assessment"""
    risk_score: Optional[float] = None
    risk_level: Optional[FlightRiskLevel] = None
    risk_signals: Optional[str] = None
    is_tracked: Optional[bool] = None


class FlightRiskAssessment(FlightRiskAssessmentBase):
    """Schema for flight risk assessment response"""
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True


class FlightRiskCounts(BaseModel):
    """Schema for flight risk counts"""
    untracked: int
    uncalculated: int
    no_risk: int
    moderate_risk: int
    high_risk: int


class FlightRiskDashboard(BaseModel):
    """Schema for flight risk dashboard response"""
    status: str
    counts: FlightRiskCounts
    employees: dict
    summary: dict

    ---------------------------------------------


    """
Employee schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class EmployeeBase(BaseModel):
    """Base employee schema"""
    employee_id: Optional[str] = None
    name: str
    email: str
    department: Optional[str] = None
    designation: Optional[str] = None
    shift_time: Optional[str] = None
    is_active: bool = True
    is_mobile_user: bool = False
    profile_picture: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    """Schema for creating employee"""
    pass


class EmployeeUpdate(BaseModel):
    """Schema for updating employee"""
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    shift_time: Optional[str] = None
    is_active: Optional[bool] = None
    is_mobile_user: Optional[bool] = None
    profile_picture: Optional[str] = None


class Employee(EmployeeBase):
    """Schema for employee response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BirthdayBase(BaseModel):
    """Base birthday schema"""
    employee_id: int
    birth_date: date


class BirthdayCreate(BirthdayBase):
    """Schema for creating birthday"""
    pass


class Birthday(BirthdayBase):
    """Schema for birthday response"""
    id: int
    employee: Optional[Employee] = None

    class Config:
        from_attributes = True


class EmployeeWithBirthday(Employee):
    """Employee with birthday information"""
    birthday: Optional[Birthday] = None


class EmployeeList(BaseModel):
    """Schema for employee list response"""
    employees: List[Employee]
    total: int
    page: int
    per_page: int


class EmployeeStats(BaseModel):
    """Schema for employee statistics"""
    total_employees: int
    active_employees: int
    inactive_employees: int
    active_mobile_users: int
    departments: List[str]


    ---------------------------------


    """
Lead schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class LeadStatus(str, Enum):
    """Lead status enum"""
    NEW = "New"
    CONTACTED = "Contacted"
    QUALIFIED = "Qualified"
    PROPOSAL = "Proposal"
    NEGOTIATION = "Negotiation"
    CLOSED_WON = "Closed Won"
    CLOSED_LOST = "Closed Lost"
    NOT_CONTACTED = "Not Contacted"


class LeadSource(str, Enum):
    """Lead source enum"""
    WEBSITE = "Website"
    GOOGLE = "Google"
    SOCIAL_MEDIA = "Social Media"
    EMAIL_CAMPAIGN = "Email Campaign"
    REFERRAL = "Referral"
    COLD_CALL = "Cold Call"
    TRADE_SHOW = "Trade Show"
    PARTNER = "Partner"


class LeadBase(BaseModel):
    """Base lead schema"""
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    source: Optional[LeadSource] = None
    status: LeadStatus = LeadStatus.NEW
    value: Optional[float] = None
    notes: Optional[str] = None
    assigned_to: Optional[str] = None


class LeadCreate(LeadBase):
    """Schema for creating lead"""
    pass


class LeadUpdate(BaseModel):
    """Schema for updating lead"""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    source: Optional[LeadSource] = None
    status: Optional[LeadStatus] = None
    value: Optional[float] = None
    notes: Optional[str] = None
    assigned_to: Optional[str] = None


class Lead(LeadBase):
    """Schema for lead response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LeadList(BaseModel):
    """Schema for lead list response"""
    leads: List[Lead]
    total: int
    page: int
    per_page: int


class LeadStats(BaseModel):
    """Schema for lead statistics"""
    total_leads: int
    new_leads: int
    contacted_leads: int
    qualified_leads: int
    closed_won: int
    closed_lost: int
    conversion_rate: float


class LeadsBySource(BaseModel):
    """Schema for leads by source chart"""
    labels: List[str]
    series: List[int]
    colors: List[str]


class LeadsByCompany(BaseModel):
    """Schema for leads by company"""
    name: str
    value: str
    status: str
    status_class: str
    icon: str


class RecentLead(BaseModel):
    """Schema for recent lead"""
    lead_name: str
    company_name: str
    company_logo: str
    stage: str
    stage_class: str
    created_date: str
    lead_owner: str


class TopCountry(BaseModel):
    """Schema for top country"""
    name: str
    leads: int
    percentage: int
    flag: str
    color: str


class TopCountries(BaseModel):
    """Schema for top countries data"""
    countries: List[TopCountry]
    chart_series: List[int]
    chart_colors: List[str]


class LeadsDashboard(BaseModel):
    """Schema for leads dashboard response"""
    status: str
    summary_cards: List[dict]
    attendance_trend: dict
    new_leads_heatmap: dict
    lost_leads_chart: dict
    leads_by_companies: List[LeadsByCompany]
    leads_by_source: LeadsBySource
    recent_follow_up: List[dict]
    recent_activities: List[dict]
    notifications: List[dict]
    top_countries: TopCountries
    recent_leads: List[RecentLead]
    summary: dict


    -----------------------------------------

    """
Notification schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    """Notification type enum"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class NotificationBase(BaseModel):
    """Base notification schema"""
    title: str
    message: str
    type: NotificationType = NotificationType.INFO
    user_id: Optional[int] = None
    is_read: bool = False


class NotificationCreate(NotificationBase):
    """Schema for creating notification"""
    pass


class NotificationUpdate(BaseModel):
    """Schema for updating notification"""
    title: Optional[str] = None
    message: Optional[str] = None
    type: Optional[NotificationType] = None
    is_read: Optional[bool] = None


class Notification(NotificationBase):
    """Schema for notification response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificationList(BaseModel):
    """Schema for notification list response"""
    notifications: List[Notification]
    total: int
    unread_count: int


class ActivityType(str, Enum):
    """Activity type enum"""
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    VIEW = "view"


class ActivityBase(BaseModel):
    """Base activity schema"""
    user_id: int
    action: str
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class ActivityCreate(ActivityBase):
    """Schema for creating activity"""
    pass


class Activity(ActivityBase):
    """Schema for activity response"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityList(BaseModel):
    """Schema for activity list response"""
    activities: List[Activity]
    total: int
    page: int
    per_page: int


class OpenRequestBase(BaseModel):
    """Base open request schema"""
    request_type: str
    count: int
    icon: Optional[str] = None
    color: Optional[str] = None


class OpenRequestCreate(OpenRequestBase):
    """Schema for creating open request"""
    pass


class OpenRequestUpdate(BaseModel):
    """Schema for updating open request"""
    request_type: Optional[str] = None
    count: Optional[int] = None
    icon: Optional[str] = None
    color: Optional[str] = None


class OpenRequest(OpenRequestBase):
    """Schema for open request response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OpenRequestList(BaseModel):
    """Schema for open request list response"""
    open_requests: List[OpenRequest]
    total: int


    -------------------------------------



    """
Subscription schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum


class SubscriptionStatus(str, Enum):
    """Subscription status enum"""
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"
    PENDING = "Pending"


class SubscriptionPlan(str, Enum):
    """Subscription plan enum"""
    BASIC = "Basic"
    STANDARD = "Standard"
    PREMIUM = "Premium"
    ENTERPRISE = "Enterprise"


class SubscriptionBase(BaseModel):
    """Base subscription schema"""
    plan_name: SubscriptionPlan
    status: SubscriptionStatus
    start_date: date
    end_date: date
    total_employees: int
    active_employees: int


class SubscriptionCreate(SubscriptionBase):
    """Schema for creating subscription"""
    pass


class SubscriptionUpdate(BaseModel):
    """Schema for updating subscription"""
    plan_name: Optional[SubscriptionPlan] = None
    status: Optional[SubscriptionStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    total_employees: Optional[int] = None
    active_employees: Optional[int] = None


class Subscription(SubscriptionBase):
    """Schema for subscription response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SubscriptionStats(BaseModel):
    """Schema for subscription statistics"""
    total_subscriptions: int
    active_subscriptions: int
    expired_subscriptions: int
    total_revenue: float
    monthly_revenue: float