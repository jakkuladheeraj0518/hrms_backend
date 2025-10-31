from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from fastapi import HTTPException

from app.repositories.request_repo import (
    EmployeeRepository, LeaveRequestRepository, MissedPunchRequestRepository,
    CompOffRequestRepository, HelpdeskRequestRepository, ClaimRequestRepository,
    TimeRelaxationRequestRepository, ShiftRosterRequestRepository,
    WeekOffRosterRequestRepository, StrikeExemptionRequestRepository,
    VisitPunchRequestRepository, WorkflowRequestRepository, ShiftRosterRepository
)
from app.schemas.request_schema import (
    EmployeeCreate, LeaveRequestCreate, MissedPunchRequestCreate,
    CompOffRequestCreate, HelpdeskRequestCreate, ClaimRequestCreate,
    TimeRelaxationRequestCreate, ShiftRosterRequestCreate,
    WeekOffRosterRequestCreate, StrikeExemptionRequestCreate,
    VisitPunchRequestCreate, WorkflowRequestCreate, ShiftRosterCreate,
    StatusUpdate
)


class BaseService:
    """Base service class with common business logic"""
    
    def __init__(self, repository):
        self.repository = repository
    
    def create(self, db: Session, **kwargs):
        """Create a new record with business logic validation"""
        return self.repository.create(db, **kwargs)
    
    def get(self, db: Session, id: int):
        """Get a record by ID"""
        result = self.repository.get(db, id)
        if not result:
            raise HTTPException(status_code=404, detail="Record not found")
        return result
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        """Get all records with pagination"""
        return self.repository.get_all(db, skip, limit)
    
    def update_status(self, db: Session, id: int, status: str):
        """Update status of a record"""
        return self.repository.update(db, id, status=status, updated_at=datetime.utcnow())
    
    def delete(self, db: Session, id: int):
        """Delete a record"""
        if not self.repository.delete(db, id):
            raise HTTPException(status_code=404, detail="Record not found")
        return {"message": "Record deleted successfully", "id": id}


class EmployeeService(BaseService):
    def __init__(self):
        super().__init__(EmployeeRepository())
    
    def create_employee(self, db: Session, employee_data: EmployeeCreate):
        """Create a new employee with validation"""
        # Check if employee code already exists
        existing = self.repository.get_by_code(db, employee_data.employee_code)
        if existing:
            raise HTTPException(status_code=400, detail="Employee code already exists")
        
        # Check if email already exists
        existing_email = self.repository.get_by_email(db, employee_data.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")
        
        return self.repository.create(db, **employee_data.dict())


class LeaveRequestService(BaseService):
    def __init__(self):
        super().__init__(LeaveRequestRepository())
    
    def create_leave_request(self, db: Session, request_data: LeaveRequestCreate):
        """Create a new leave request with validation"""
        # Add business logic validation here if needed
        return self.repository.create(db, **request_data.dict())
    
    def get_filtered_requests(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        location: Optional[str] = None,
        status: Optional[str] = None,
        leave_type: Optional[str] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        search: Optional[str] = None
    ):
        """Get filtered leave requests"""
        return self.repository.get_filtered(
            db, skip, limit, location, status, leave_type, from_date, to_date, search
        )
    
    def get_request_count(
        self,
        db: Session,
        location: Optional[str] = None,
        status: Optional[str] = None,
        leave_type: Optional[str] = None
    ):
        """Get count of leave requests"""
        return {"count": self.repository.count_filtered(db, location, status, leave_type)}


class MissedPunchRequestService(BaseService):
    def __init__(self):
        super().__init__(MissedPunchRequestRepository())
    
    def create_missed_punch_request(self, db: Session, request_data: MissedPunchRequestCreate):
        """Create a new missed punch request"""
        return self.repository.create(db, **request_data.dict())


class CompOffRequestService(BaseService):
    def __init__(self):
        super().__init__(CompOffRequestRepository())
    
    def create_compoff_request(self, db: Session, request_data: CompOffRequestCreate):
        """Create a new comp off request"""
        return self.repository.create(db, **request_data.dict())


class HelpdeskRequestService(BaseService):
    def __init__(self):
        super().__init__(HelpdeskRequestRepository())
    
    def create_helpdesk_request(self, db: Session, request_data: HelpdeskRequestCreate):
        """Create a new helpdesk request"""
        return self.repository.create(db, **request_data.dict())


class ClaimRequestService(BaseService):
    def __init__(self):
        super().__init__(ClaimRequestRepository())
    
    def create_claim_request(self, db: Session, request_data: ClaimRequestCreate):
        """Create a new claim request"""
        return self.repository.create(db, **request_data.dict())


class TimeRelaxationRequestService(BaseService):
    def __init__(self):
        super().__init__(TimeRelaxationRequestRepository())
    
    def create_time_relaxation_request(self, db: Session, request_data: TimeRelaxationRequestCreate):
        """Create a new time relaxation request"""
        return self.repository.create(db, **request_data.dict())


class ShiftRosterRequestService(BaseService):
    def __init__(self):
        super().__init__(ShiftRosterRequestRepository())
    
    def create_shift_roster_request(self, db: Session, request_data: ShiftRosterRequestCreate):
        """Create a new shift roster request"""
        return self.repository.create(db, **request_data.dict())


class WeekOffRosterRequestService(BaseService):
    def __init__(self):
        super().__init__(WeekOffRosterRequestRepository())
    
    def create_weekoff_roster_request(self, db: Session, request_data: WeekOffRosterRequestCreate):
        """Create a new week off roster request"""
        return self.repository.create(db, **request_data.dict())


class StrikeExemptionRequestService(BaseService):
    def __init__(self):
        super().__init__(StrikeExemptionRequestRepository())
    
    def create_strike_exemption_request(self, db: Session, request_data: StrikeExemptionRequestCreate):
        """Create a new strike exemption request"""
        return self.repository.create(db, **request_data.dict())


class VisitPunchRequestService(BaseService):
    def __init__(self):
        super().__init__(VisitPunchRequestRepository())
    
    def create_visit_punch_request(self, db: Session, request_data: VisitPunchRequestCreate):
        """Create a new visit punch request"""
        return self.repository.create(db, **request_data.dict())


class WorkflowRequestService(BaseService):
    def __init__(self):
        super().__init__(WorkflowRequestRepository())
    
    def create_workflow_request(self, db: Session, request_data: WorkflowRequestCreate):
        """Create a new workflow request"""
        return self.repository.create(db, **request_data.dict())


class ShiftRosterService(BaseService):
    def __init__(self):
        super().__init__(ShiftRosterRepository())
    
    def create_shift_roster(self, db: Session, roster_data: ShiftRosterCreate):
        """Create a new shift roster"""
        return self.repository.create(db, **roster_data.dict())



