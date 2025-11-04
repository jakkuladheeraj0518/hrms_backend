"""
Attendance related models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.connection import Base


class AttendanceRecord(Base):
    """Attendance record model"""
    __tablename__ = "attendance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date)
    time_in = Column(String)
    time_out = Column(String)
    status = Column(String)  # Present, Absent, Leave, WeekOff, Holiday
    is_late = Column(Boolean, default=False)
    is_early_out = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("Employee", back_populates="attendance_records")


class FlightRiskAssessment(Base):
    """Flight risk assessment model"""
    __tablename__ = "flight_risk_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    risk_score = Column(Float)
    risk_level = Column(String)  # No Risk, Moderate Risk, High Risk
    risk_signals = Column(Text)  # JSON string of risk signals
    last_updated = Column(DateTime, default=datetime.utcnow)
    is_tracked = Column(Boolean, default=True)
    
    # Relationships
    employee = relationship("Employee", back_populates="flight_risk_assessments")





-----------------------------------



"""
Employee related models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.connection import Base


class Employee(Base):
    """Employee model"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    department = Column(String)
    designation = Column(String)
    shift_time = Column(String)
    is_active = Column(Boolean, default=True)
    is_mobile_user = Column(Boolean, default=False)
    profile_picture = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendance_records = relationship("AttendanceRecord", back_populates="employee")
    flight_risk_assessments = relationship("FlightRiskAssessment", back_populates="employee")


class Birthday(Base):
    """Employee birthday model"""
    __tablename__ = "birthdays"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    birth_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("Employee")


    ---------------------------------------------

"""
Lead related models
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Date
from datetime import datetime
from ..database.connection import Base


class Lead(Base):
    """Lead model"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    company_name = Column(String)
    company_logo = Column(String)
    stage = Column(String)  # Not Contacted, Contacted, Closed, Lost
    value = Column(Float)
    source = Column(String)  # Google, Paid, Campaigns, Referrals
    country = Column(String)
    lead_owner = Column(String)
    created_date = Column(Date)
    lost_reason = Column(String)  # Competitor, Budget, Unresponsive, Timing
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)




    -------------------------------------------


    """
Notification and activity related models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from datetime import datetime
from ..database.connection import Base


class Notification(Base):
    """Notification model"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    message = Column(Text)
    user_name = Column(String)
    user_avatar = Column(String)
    notification_type = Column(String)  # access_request, general, approval
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Activity(Base):
    """Activity model"""
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    activity_type = Column(String)  # phone, message, meeting, user
    icon_class = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class OpenRequest(Base):
    """Open request model"""
    __tablename__ = "open_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    request_type = Column(String)
    count = Column(Integer, default=0)
    icon = Column(String)
    color = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)





    -------------------------------------------



"""
Subscription related models
"""
from sqlalchemy import Column, Integer, String, DateTime, Date
from datetime import datetime
from ..database.connection import Base


class Subscription(Base):
    """Subscription model"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String)
    status = Column(String)  # Active, Inactive, Expired
    start_date = Column(Date)
    end_date = Column(Date)
    total_employees = Column(Integer)
    active_employees = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)