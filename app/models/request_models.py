from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Date, Time
from datetime import datetime
from app.database.base import Base
    
class MissedPunchRequest(Base):
    __tablename__ = "missed_punch_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50))
    employee_name = Column(String(200))
    missed_punch_time = Column(DateTime, nullable=False)
    comment = Column(Text)
    requested_on = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Open")
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50))
    employee_name = Column(String(200))
    leave_type = Column(String(100))
    from_date = Column(Date)
    to_date = Column(Date)
    date_range = Column(String(200))
    comment = Column(Text)
    requested_on = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Open")
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CompOffRequest(Base):
    __tablename__ = "compoff_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50))
    employee_name = Column(String(200))
    compoff_date = Column(Date)
    comment = Column(Text)
    requested_on = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Open")
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HelpdeskRequest(Base):
    __tablename__ = "helpdesk_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50))
    employee_name = Column(String(200))
    category = Column(String(100))
    subject = Column(String(500))
    description = Column(Text)
    requested_on = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Open")
    location = Column(String(100))
    approver = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ClaimRequest(Base):
    __tablename__ = "claim_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50))
    employee_name = Column(String(200))
    component = Column(String(100))
    amount = Column(Integer)
    claim_date = Column(Date)
    description = Column(Text)
    requested_on = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Open")
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TimeRelaxationRequest(Base):
    __tablename__ = "time_relaxation_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50))
    employee_name = Column(String(200))
    relaxation_date = Column(Date)
    relaxation_time = Column(Integer)  # in minutes
    reason = Column(Text)
    requested_on = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Open")
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ShiftRosterRequest(Base):
    __tablename__ = "shift_roster_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50))
    employee_name = Column(String(200))
    shift_date = Column(Date)
    shift_name = Column(String(100))
    requested_on = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Open")
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WeekOffRosterRequest(Base):
    __tablename__ = "weekoff_roster_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50))
    employee_name = Column(String(200))
    weekoff_date = Column(Date)
    requested_on = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Open")
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class StrikeExemptionRequest(Base):
    __tablename__ = "strike_exemption_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50))
    employee_name = Column(String(200))
    exemption_date = Column(Date)
    reason = Column(Text)
    requested_on = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Open")
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class VisitPunchRequest(Base):
    __tablename__ = "visit_punch_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50))
    employee_name = Column(String(200))
    visit_date = Column(Date)
    visit_location = Column(String(200))
    purpose = Column(Text)
    requested_on = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Open")
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WorkflowRequest(Base):
    __tablename__ = "workflow_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50))
    employee_name = Column(String(200))
    workflow_type = Column(String(100))
    workflow_date = Column(Date)
    description = Column(Text)
    requested_on = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Open")
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ShiftRoster(Base):
    __tablename__ = "shift_rosters"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50))
    employee_name = Column(String(200))
    shift_date = Column(Date)
    shift_name = Column(String(100))
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



