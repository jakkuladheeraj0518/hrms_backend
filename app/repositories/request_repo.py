from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Type, Any
from datetime import date, datetime
from app.models.request_models import (
    MissedPunchRequest, LeaveRequest, CompOffRequest,
    HelpdeskRequest, ClaimRequest, TimeRelaxationRequest,
    ShiftRosterRequest, WeekOffRosterRequest, StrikeExemptionRequest,
    VisitPunchRequest, WorkflowRequest, ShiftRoster
)


class BaseRepository:
    """Base repository class with common CRUD operations"""
    
    def __init__(self, model: Type[Any]):
        self.model = model
    
    def create(self, db: Session, **kwargs) -> Any:
        """Create a new record"""
        db_obj = self.model(**kwargs)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: int) -> Optional[Any]:
        """Get a record by ID"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Any]:
        """Get all records with pagination"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, db: Session, id: int, **kwargs) -> Optional[Any]:
        """Update a record by ID"""
        db_obj = self.get(db, id)
        if db_obj:
            for key, value in kwargs.items():
                setattr(db_obj, key, value)
            db.commit()
            db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> bool:
        """Delete a record by ID"""
        db_obj = self.get(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False
    
    def count(self, db: Session) -> int:
        """Count total records"""
        return db.query(self.model).count()


class LeaveRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(LeaveRequest)
    
    def get_filtered(
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
    ) -> List[LeaveRequest]:
        """Get filtered leave requests"""
        query = db.query(LeaveRequest)
        
        if location and location != "All Locations":
            query = query.filter(LeaveRequest.location == location)
        
        if status:
            query = query.filter(LeaveRequest.status == status)
        
        if leave_type and leave_type != "All Leaves":
            query = query.filter(LeaveRequest.leave_type == leave_type)
        
        if from_date:
            query = query.filter(LeaveRequest.from_date >= from_date)
        
        if to_date:
            query = query.filter(LeaveRequest.to_date <= to_date)
        
        if search:
            query = query.filter(
                or_(
                    LeaveRequest.employee_name.ilike(f"%{search}%"),
                    LeaveRequest.employee_code.ilike(f"%{search}%")
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    def count_filtered(
        self,
        db: Session,
        location: Optional[str] = None,
        status: Optional[str] = None,
        leave_type: Optional[str] = None
    ) -> int:
        """Count filtered leave requests"""
        query = db.query(LeaveRequest)
        
        if location and location != "All Locations":
            query = query.filter(LeaveRequest.location == location)
        
        if status:
            query = query.filter(LeaveRequest.status == status)
        
        if leave_type and leave_type != "All Leaves":
            query = query.filter(LeaveRequest.leave_type == leave_type)
        
        return query.count()


class MissedPunchRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(MissedPunchRequest)


class CompOffRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(CompOffRequest)


class HelpdeskRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(HelpdeskRequest)


class ClaimRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(ClaimRequest)


class TimeRelaxationRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(TimeRelaxationRequest)


class ShiftRosterRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(ShiftRosterRequest)


class WeekOffRosterRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(WeekOffRosterRequest)


class StrikeExemptionRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(StrikeExemptionRequest)


class VisitPunchRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(VisitPunchRequest)


class WorkflowRequestRepository(BaseRepository):
    def __init__(self):
        super().__init__(WorkflowRequest)


class ShiftRosterRepository(BaseRepository):
    def __init__(self):
        super().__init__(ShiftRoster)



