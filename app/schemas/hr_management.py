from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import Field


class AlertBase(BaseModel):
    alert_name: str
    attendance_condition: str
    days_more_than: int
    send_letter: str
    check_every: str
    active: bool

class AlertCreate(AlertBase):
    pass

class AlertUpdate(AlertBase):
    pass

class Alert(AlertBase):
    id: int

    class Config:
        from_attributes = True



class BirthdayGreetingBase(BaseModel):
    enable: bool = True
    send_copy: bool = True
    post_feed: bool = True
    search_employee: str | None = None
    message: str | None = None


class BirthdayGreetingResponse(BirthdayGreetingBase):
    id: int
    
    class Config:
        from_attributes = True


# 📨 Letter Template Schema
class LetterTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_offer_letter: bool = False


class LetterTemplateCreate(LetterTemplateBase):
    pass


class LetterTemplateResponse(LetterTemplateBase):
    id: int
    file_path: str
    last_updated: datetime

    class Config:
        from_attributes = True  # Updated for Pydantic v2 (was orm_mode in v1)


# 📜 Letter History Schema
class LetterHistoryBase(BaseModel):
    letter_name: str
    status: Optional[str] = "Completed"


class LetterHistoryCreate(LetterHistoryBase):
    pass


class LetterHistoryResponse(LetterHistoryBase):
    id: int
    requested_at: datetime

    class Config:
        from_attributes = True  # Updated for Pydantic v2 (was orm_mode in v1)



class SendOption(str, Enum):
    """Send option enumeration"""
    SEND_NOW = "send_now"
    SEND_LATER = "send_later"


class LocationOption(str, Enum):
    """Location options"""
    ALL_LOCATIONS = "all_locations"
    BANGALORE = "bangalore"
    HYDERABAD = "hyderabad"


class DepartmentOption(str, Enum):
    """Department options"""
    ALL_DEPARTMENTS = "all_departments"
    PRODUCT_DEVELOPMENT = "product_development"
    HR_EXECUTIVE = "hr_executive"
    TECHNICAL_SUPPORT = "technical_support"


class NotificationBase(BaseModel):
    """Base schema for Notification"""
    location: str = Field(..., description="Location: all_locations, bangalore, hyderabad")
    department: str = Field(..., description="Department: all_departments, product_development, hr_executive, technical_support")
    employee_search: Optional[str] = Field(None, description="Search term for specific employees")
    send_option: SendOption = Field(default=SendOption.SEND_NOW, description="Send now or schedule for later")
    subject: str = Field(..., min_length=1, max_length=255, description="Notification subject")
    description: str = Field(..., min_length=1, description="Notification description/message")
    scheduled_time: Optional[datetime] = Field(None, description="Scheduled time for send_later option")


class NotificationCreate(NotificationBase):
    """Schema for creating a new notification"""
    pass


class NotificationUpdate(BaseModel):
    """Schema for updating a notification"""
    location: Optional[str] = None
    department: Optional[str] = None
    employee_search: Optional[str] = None
    send_option: Optional[SendOption] = None
    subject: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    scheduled_time: Optional[datetime] = None
    is_sent: Optional[bool] = None


class NotificationResponse(NotificationBase):
    """Schema for notification response"""
    id: int
    image_path: Optional[str] = None
    image_filename: Optional[str] = None
    is_sent: bool
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    """Schema for listing notifications"""
    id: int
    subject: str
    description: str
    location: str
    department: str
    is_sent: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LocationList(BaseModel):
    """Available locations"""
    locations: list[dict] = [
        {"value": "all_locations", "label": "All Locations"},
        {"value": "bangalore", "label": "Bangalore"},
        {"value": "hyderabad", "label": "Hyderabad"}
    ]


class DepartmentList(BaseModel):
    """Available departments"""
    departments: list[dict] = [
        {"value": "all_departments", "label": "All Departments"},
        {"value": "product_development", "label": "Product Development Team"},
        {"value": "hr_executive", "label": "HR Executive"},
        {"value": "technical_support", "label": "Technical Support"}
    ]



class PolicyType(str, Enum):
    """Policy type enumeration"""
    UPLOADED = "uploaded"
    ONLINE = "online"


class PolicyBase(BaseModel):
    """Base schema for Policy"""
    policy_name: str = Field(..., min_length=1, max_length=255, description="Name of the policy")
    type: PolicyType = Field(..., description="Type of policy: uploaded or online")
    actions: Optional[bool] = Field(None, description="Whether actions are enabled for this policy")


class PolicyCreate(PolicyBase):
    """Schema for creating a new policy"""
    file_path: Optional[str] = Field(None, max_length=500, description="Path to uploaded policy file")
    file_name: Optional[str] = Field(None, max_length=255, description="Name of uploaded file")
    content: Optional[str] = Field(None, description="Content for online policy")


class PolicyUpdate(BaseModel):
    """Schema for updating a policy"""
    policy_name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[PolicyType] = None
    file_path: Optional[str] = Field(None, max_length=500)
    file_name: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    actions: Optional[bool] = None


class PolicyResponse(PolicyBase):
    """Schema for policy response"""
    id: int
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    content: Optional[str] = None
    created_on: datetime
    last_updated: datetime
    actions: Optional[bool] = None

    class Config:
        from_attributes = True


class PolicyListResponse(BaseModel):
    """Schema for listing policies"""
    id: int
    policy_name: str
    type: PolicyType
    created_on: datetime
    last_updated: datetime
    actions: Optional[bool] = None

    class Config:
        from_attributes = True


class WeddingAnniversaryGreetingBase(BaseModel):
    enable: bool = False
    send_copy: bool = True
    post_feed: bool = True
    subject: str | None = None
    message: str | None = None


class WeddingAnniversaryGreetingResponse(WeddingAnniversaryGreetingBase):
    id: int
    
    class Config:
        from_attributes = True


class WorkAnniversaryGreetingBase(BaseModel):
    enable: bool
    send_copy: bool
    post_feed: bool
    subject: str
    message: str

class WorkAnniversaryGreetingCreate(WorkAnniversaryGreetingBase):
    pass

class WorkAnniversaryGreetingResponse(WorkAnniversaryGreetingBase):
    id: int

    class Config:
        from_attributes = True

