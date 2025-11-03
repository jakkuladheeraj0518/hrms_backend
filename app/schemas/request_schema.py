from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

# Missed Punch Request Schemas
class MissedPunchRequestBase(BaseModel):
    employee_code: str
    employee_name: str
    missed_punch_time: datetime
    comment: Optional[str] = None
    location: Optional[str] = None

class MissedPunchRequestCreate(MissedPunchRequestBase):
    pass

class MissedPunchRequest(MissedPunchRequestBase):
    id: int
    status: str
    requested_on: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Leave Request Schemas
class LeaveRequestBase(BaseModel):
    employee_code: str
    employee_name: str
    leave_type: str
    from_date: date
    to_date: date
    date_range: Optional[str] = None
    comment: Optional[str] = None
    location: Optional[str] = None

class LeaveRequestCreate(LeaveRequestBase):
    pass

class LeaveRequest(LeaveRequestBase):
    id: int
    status: str
    requested_on: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Comp Off Request Schemas
class CompOffRequestBase(BaseModel):
    employee_code: str
    employee_name: str
    compoff_date: date
    comment: Optional[str] = None
    location: Optional[str] = None

class CompOffRequestCreate(CompOffRequestBase):
    pass

class CompOffRequest(CompOffRequestBase):
    id: int
    status: str
    requested_on: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Helpdesk Request Schemas
class HelpdeskRequestBase(BaseModel):
    employee_code: str
    employee_name: str
    category: str
    subject: str
    description: Optional[str] = None
    location: Optional[str] = None
    approver: Optional[str] = None

class HelpdeskRequestCreate(HelpdeskRequestBase):
    pass

class HelpdeskRequest(HelpdeskRequestBase):
    id: int
    status: str
    requested_on: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Claim Request Schemas
class ClaimRequestBase(BaseModel):
    employee_code: str
    employee_name: str
    component: str
    amount: int
    claim_date: date
    description: Optional[str] = None
    location: Optional[str] = None

class ClaimRequestCreate(ClaimRequestBase):
    pass

class ClaimRequest(ClaimRequestBase):
    id: int
    status: str
    requested_on: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Time Relaxation Request Schemas
class TimeRelaxationRequestBase(BaseModel):
    employee_code: str
    employee_name: str
    relaxation_date: date
    relaxation_time: int
    reason: Optional[str] = None
    location: Optional[str] = None

class TimeRelaxationRequestCreate(TimeRelaxationRequestBase):
    pass

class TimeRelaxationRequest(TimeRelaxationRequestBase):
    id: int
    status: str
    requested_on: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Shift Roster Request Schemas
class ShiftRosterRequestBase(BaseModel):
    employee_code: str
    employee_name: str
    shift_date: date
    shift_name: str
    location: Optional[str] = None

class ShiftRosterRequestCreate(ShiftRosterRequestBase):
    pass

class ShiftRosterRequest(ShiftRosterRequestBase):
    id: int
    status: str
    requested_on: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Week Off Roster Request Schemas
class WeekOffRosterRequestBase(BaseModel):
    employee_code: str
    employee_name: str
    weekoff_date: date
    location: Optional[str] = None

class WeekOffRosterRequestCreate(WeekOffRosterRequestBase):
    pass

class WeekOffRosterRequest(WeekOffRosterRequestBase):
    id: int
    status: str
    requested_on: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Strike Exemption Request Schemas
class StrikeExemptionRequestBase(BaseModel):
    employee_code: str
    employee_name: str
    exemption_date: date
    reason: Optional[str] = None
    location: Optional[str] = None

class StrikeExemptionRequestCreate(StrikeExemptionRequestBase):
    pass

class StrikeExemptionRequest(StrikeExemptionRequestBase):
    id: int
    status: str
    requested_on: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Visit Punch Request Schemas
class VisitPunchRequestBase(BaseModel):
    employee_code: str
    employee_name: str
    visit_date: date
    visit_location: str
    purpose: Optional[str] = None
    location: Optional[str] = None

class VisitPunchRequestCreate(VisitPunchRequestBase):
    pass

class VisitPunchRequest(VisitPunchRequestBase):
    id: int
    status: str
    requested_on: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Workflow Request Schemas
class WorkflowRequestBase(BaseModel):
    employee_code: str
    employee_name: str
    workflow_type: str
    workflow_date: date
    description: Optional[str] = None
    location: Optional[str] = None

class WorkflowRequestCreate(WorkflowRequestBase):
    pass

class WorkflowRequest(WorkflowRequestBase):
    id: int
    status: str
    requested_on: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Shift Roster Schemas
class ShiftRosterBase(BaseModel):
    employee_code: str
    employee_name: str
    shift_date: date
    shift_name: str
    location: Optional[str] = None

class ShiftRosterCreate(ShiftRosterBase):
    pass

class ShiftRoster(ShiftRosterBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Common Response Schemas
class StatusUpdate(BaseModel):
    status: str

class DeleteResponse(BaseModel):
    message: str
    id: int



