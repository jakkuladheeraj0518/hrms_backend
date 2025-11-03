from sqlalchemy import Column, Integer, String, Boolean
from app.database.base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum as SQLEnum, func
from datetime import datetime
import enum




class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_name = Column(String, index=True)
    attendance_condition = Column(String)
    days_more_than = Column(Integer)
    send_letter = Column(String)
    check_every = Column(String)
    active = Column(Boolean, default=True)


class BirthdayGreeting(Base):
    __tablename__ = "birthday_greetings"
    
    id = Column(Integer, primary_key=True, index=True)
    enable = Column(Boolean, default=True)
    send_copy = Column(Boolean, default=True)
    post_feed = Column(Boolean, default=True)
    search_employee=Column(String, nullable=True)
    message = Column(String, nullable=True)



class LetterTemplate(Base):
    __tablename__ = "letter_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    file_path = Column(String, nullable=False)
    is_offer_letter = Column(Boolean, default=False)
    last_updated = Column(DateTime, default=datetime.utcnow)


class LetterHistory(Base):
    __tablename__ = "letter_history"

    id = Column(Integer, primary_key=True, index=True)
    letter_name = Column(String, nullable=False)
    requested_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Completed")


class SendOption(str, enum.Enum):
    """Send option enumeration"""
    SEND_NOW = "send_now"
    SEND_LATER = "send_later"


class Notification(Base):
    """Notification model for employee notifications"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    
    # Recipient Selection
    location = Column(String(100), nullable=False, index=True)  
    department = Column(String(100), nullable=False, index=True)  
    employee_search = Column(String(255), nullable=True)  
    
    # Message Details
    send_option = Column(SQLEnum(SendOption), nullable=False, default=SendOption.SEND_NOW)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    # Image attachment (optional)
    image_path = Column(String(500), nullable=True)
    image_filename = Column(String(255), nullable=True)
    
    # Send scheduling
    scheduled_time = Column(DateTime(timezone=True), nullable=True)  # For "send later"
    
    # Status tracking
    is_sent = Column(Boolean, default=False, nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Notification(id={self.id}, subject={self.subject}, location={self.location}, department={self.department})>"


class PolicyType(str, enum.Enum):
    """Policy type enumeration"""
    UPLOADED = "uploaded"
    ONLINE = "online"


class Policy(Base):
    """Policy model for storing company policies"""
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    policy_name = Column(String(255), nullable=False, index=True)
    type = Column(SQLEnum(PolicyType), nullable=False, default=PolicyType.UPLOADED)
    actions = Column(Boolean, nullable=True)

    # For uploaded policies
    file_path = Column(String(500), nullable=True)
    file_name = Column(String(255), nullable=True)
    
    # For online policies
    content = Column(Text, nullable=True)
    
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    
    def __repr__(self):
        return f"<Policy(id={self.id}, name={self.policy_name}, type={self.type},actions={self.actions})>"


class WeddingAnniversaryGreeting(Base):
    __tablename__ = "wedding_anniversary_greetings"
    
    id = Column(Integer, primary_key=True, index=True)
    enable = Column(Boolean, default=False)
    send_copy = Column(Boolean, default=True)
    post_feed = Column(Boolean, default=True)
    subject = Column(String, nullable=True)
    message = Column(String, nullable=True)


class WorkAnniversaryGreeting(Base):
    __tablename__ = "work_anniversary_greetings"
    
    id = Column(Integer, primary_key=True, index=True)
    enable = Column(Boolean, default=False)
    send_copy = Column(Boolean, default=True)
    post_feed = Column(Boolean, default=True)
    subject = Column(String, nullable=True)
    message = Column(String, nullable=True)
