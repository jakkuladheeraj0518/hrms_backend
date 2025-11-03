"""
Alert Service - Business Logic Layer for Alerts
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from fastapi import HTTPException, UploadFile
from app import models, schemas
from pathlib import Path
from datetime import datetime
import os
import shutil

from app.models import hr_management as models
from app.schemas import hr_management as schemas
from app.repositories import hr_management as repositories

from app.repositories import AlertRepository
from app.repositories import BirthdayGreetingRepository
from app.repositories import LetterTemplateRepository, LetterHistoryRepository
from app.repositories import NotificationRepository
from app.repositories import PolicyRepository
from app.repositories import WeddingAnniversaryRepository
from app.repositories import WorkAnniversaryRepository



class AlertService:
    """Service for Alert business logic"""
    
    def __init__(self):
        self.repository = AlertRepository()
    
    def get_all_alerts(self, db: Session) -> List[models.Alert]:
        """Get all alerts"""
        return self.repository.get_all(db)
    
    def get_alert_by_id(self, db: Session, alert_id: int) -> models.Alert:
        """Get alert by ID"""
        alert = self.repository.get_by_id(db, alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return alert
    
    def create_alert(self, db: Session, alert_data: schemas.AlertCreate) -> models.Alert:
        """Create a new alert"""
        return self.repository.create(db, alert_data.dict())
    
    def update_alert(self, db: Session, alert_id: int, alert_data: schemas.AlertUpdate) -> models.Alert:
        """Update an existing alert"""
        alert = self.get_alert_by_id(db, alert_id)
        return self.repository.update(db, alert, alert_data.dict())
    
    def delete_alert(self, db: Session, alert_id: int) -> dict:
        """Delete an alert"""
        alert = self.get_alert_by_id(db, alert_id)
        self.repository.delete(db, alert)
        return {"message": "Alert deleted successfully"}
    
    def get_active_alerts(self, db: Session) -> List[models.Alert]:
        """Get all active alerts"""
        return self.repository.get_active_alerts(db)
    


"""
Birthday Greeting Service - Business Logic Layer for Birthday Greetings
"""

class BirthdayGreetingService:
    """Service for Birthday Greeting business logic"""
    
    def __init__(self):
        self.repository = BirthdayGreetingRepository()
    
    def get_all_greetings(self, db: Session) -> List[models.BirthdayGreeting]:
        """Get all birthday greetings"""
        return self.repository.get_all(db)
    
    def get_greeting_by_id(self, db: Session, greeting_id: int) -> models.BirthdayGreeting:
        """Get greeting by ID"""
        greeting = self.repository.get_by_id(db, greeting_id)
        if not greeting:
            raise HTTPException(status_code=404, detail="Birthday greeting not found")
        return greeting
    
    def create_greeting(self, db: Session, greeting_data: schemas.BirthdayGreetingBase) -> models.BirthdayGreeting:
        """Create a new birthday greeting"""
        return self.repository.create(db, greeting_data.dict())
    
    def update_greeting(self, db: Session, greeting_id: int, greeting_data: schemas.BirthdayGreetingBase) -> models.BirthdayGreeting:
        """Update an existing birthday greeting"""
        greeting = self.get_greeting_by_id(db, greeting_id)
        return self.repository.update(db, greeting, greeting_data.dict())
    
    def delete_greeting(self, db: Session, greeting_id: int) -> dict:
        """Delete a birthday greeting"""
        greeting = self.get_greeting_by_id(db, greeting_id)
        self.repository.delete(db, greeting)
        return {"message": f"Birthday greeting {greeting_id} deleted successfully"}
    
    def get_enabled_greetings(self, db: Session) -> List[models.BirthdayGreeting]:
        """Get all enabled birthday greetings"""
        return self.repository.get_enabled_greetings(db)
    


"""
Letter Service - Business Logic Layer for Letters
"""


class LetterTemplateService:
    """Service for LetterTemplate business logic"""

    def __init__(self):
        self.repository = LetterTemplateRepository()

    def get_all_templates(self, db: Session) -> List[models.LetterTemplate]:
        """Get all letter templates"""
        return self.repository.get_all(db)

    def get_template_by_id(self, db: Session, template_id: int) -> models.LetterTemplate:
        """Get letter template by ID"""
        template = self.repository.get_by_id(db, template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Letter template not found")
        return template

    def get_template_by_name(self, db: Session, name: str) -> models.LetterTemplate:
        """Get letter template by name"""
        template = self.repository.get_by_name(db, name)
        if not template:
            raise HTTPException(status_code=404, detail="Letter template not found")
        return template

    def create_template(self, db: Session, template_data: schemas.LetterTemplateCreate) -> models.LetterTemplate:
        """Create a new letter template"""
        return self.repository.create(db, template_data.dict())

    def update_template(self, db: Session, template_id: int, template_data: schemas.LetterTemplateUpdate) -> models.LetterTemplate:
        """Update an existing letter template"""
        template = self.get_template_by_id(db, template_id)
        return self.repository.update(db, template, template_data.dict())

    def delete_template(self, db: Session, template_id: int) -> dict:
        """Delete a letter template"""
        template = self.get_template_by_id(db, template_id)
        self.repository.delete(db, template)
        return {"message": "Letter template deleted successfully"}

    def get_offer_templates(self, db: Session) -> List[models.LetterTemplate]:
        """Get all offer letter templates"""
        return self.repository.get_offer_letters(db)

    def get_non_offer_templates(self, db: Session) -> List[models.LetterTemplate]:
        """Get all non-offer letter templates"""
        return self.repository.get_non_offer_letters(db)


class LetterHistoryService:
    """Service for LetterHistory business logic"""

    def __init__(self):
        self.repository = LetterHistoryRepository()

    def get_all_histories(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.LetterHistory]:
        """Get all letter history entries with pagination"""
        return self.repository.get_all(db, skip=skip, limit=limit)

    def get_history_by_id(self, db: Session, history_id: int) -> models.LetterHistory:
        """Get letter history by ID"""
        history = self.repository.get_by_id(db, history_id)
        if not history:
            raise HTTPException(status_code=404, detail="Letter history not found")
        return history

    def get_histories_by_letter_name(self, db: Session, letter_name: str) -> List[models.LetterHistory]:
        """Get letter history entries by letter name"""
        return self.repository.get_by_letter_name(db, letter_name)

    def get_histories_by_status(self, db: Session, status: str) -> List[models.LetterHistory]:
        """Get letter history entries by status"""
        return self.repository.get_by_status(db, status)

    def get_recent_histories(self, db: Session, limit: int = 10) -> List[models.LetterHistory]:
        """Get recent letter history entries"""
        return self.repository.get_recent(db, limit=limit)

    def create_history(self, db: Session, history_data: schemas.LetterHistoryCreate) -> models.LetterHistory:
        """Create a new letter history entry"""
        return self.repository.create(db, history_data.dict())

    def delete_history(self, db: Session, history_id: int) -> dict:
        """Delete a letter history entry"""
        history = self.get_history_by_id(db, history_id)
        self.repository.delete(db, history)
        return {"message": "Letter history deleted successfully"}
    

"""
Notification Service - Business Logic Layer for Notifications
"""


class NotificationService:
    """Service for Notification business logic"""
    
    def __init__(self):
        self.repository = NotificationRepository()
        self.upload_dir = Path("uploads/notifications")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_send_option(self, send_option: str) -> models.SendOption:
        """Validate and convert send option"""
        try:
            return models.SendOption(send_option)
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="Invalid send option. Use 'send_now' or 'send_later'"
            )
    
    def parse_scheduled_time(self, scheduled_time: Optional[str]) -> Optional[datetime]:
        """Parse scheduled time from string"""
        if not scheduled_time:
            return None
        
        try:
            return datetime.fromisoformat(scheduled_time.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="Invalid scheduled_time format. Use ISO format."
            )
    
    def validate_image(self, image: UploadFile) -> bytes:
        """Validate image file"""
        if image.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            raise HTTPException(
                status_code=400, 
                detail="Only JPG, JPEG, PNG images are allowed"
            )
        
        return image.file.read()
    
    def save_image(self, image: UploadFile, subject: str) -> Tuple[str, str]:
        """Save image file and return path and filename"""
        file_content = self.validate_image(image)
        
        if len(file_content) > 1_000_000:  # 1MB
            raise HTTPException(
                status_code=400, 
                detail="Image size must be less than 1MB"
            )
        
        file_extension = os.path.splitext(image.filename)[1]
        safe_subject = subject.replace(' ', '_').replace('/', '_').replace('\\', '_')[:50]
        image_filename = f"{safe_subject}_{datetime.now().timestamp()}{file_extension}"
        image_path_obj = self.upload_dir / image_filename
        
        with open(image_path_obj, "wb") as buffer:
            buffer.write(file_content)
        
        return str(image_path_obj), image_filename
    
    def create_notification(
        self,
        db: Session,
        location: str,
        department: str,
        send_option: str,
        subject: str,
        description: str,
        employee_search: Optional[str] = None,
        scheduled_time: Optional[str] = None,
        image: Optional[UploadFile] = None
    ) -> models.Notification:
        """Create a new notification"""
        # Validate send option
        send_opt = self.validate_send_option(send_option)
        
        # Parse scheduled time
        scheduled_dt = self.parse_scheduled_time(scheduled_time)
        
        # Validate send_later requires scheduled_time
        if send_opt == models.SendOption.SEND_LATER and not scheduled_dt:
            raise HTTPException(
                status_code=400, 
                detail="scheduled_time is required when send_option is 'send_later'"
            )
        
        # Handle image upload
        image_path = None
        image_filename = None
        
        if image:
            image_path, image_filename = self.save_image(image, subject)
        
        # Create notification
        notification_data = {
            "location": location,
            "department": department,
            "employee_search": employee_search,
            "send_option": send_opt,
            "subject": subject,
            "description": description,
            "image_path": image_path,
            "image_filename": image_filename,
            "scheduled_time": scheduled_dt,
            "is_sent": (send_opt == models.SendOption.SEND_NOW),
            "sent_at": datetime.now() if send_opt == models.SendOption.SEND_NOW else None
        }
        
        return self.repository.create(db, notification_data)
    
    def get_all_notifications(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        location: Optional[str] = None,
        department: Optional[str] = None,
        is_sent: Optional[bool] = None
    ) -> List[models.Notification]:
        """Get all notifications with optional filters"""
        return self.repository.get_all_with_filters(
            db, skip, limit, location, department, is_sent
        )
    
    def get_notification_by_id(self, db: Session, notification_id: int) -> models.Notification:
        """Get notification by ID"""
        notification = self.repository.get_by_id(db, notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        return notification
    
    def update_notification(
        self,
        db: Session,
        notification_id: int,
        location: Optional[str] = None,
        department: Optional[str] = None,
        send_option: Optional[str] = None,
        subject: Optional[str] = None,
        description: Optional[str] = None,
        employee_search: Optional[str] = None,
        scheduled_time: Optional[str] = None,
        image: Optional[UploadFile] = None
    ) -> models.Notification:
        """Update an existing notification"""
        notification = self.get_notification_by_id(db, notification_id)
        
        update_data = {}
        
        if location:
            update_data["location"] = location
        if department:
            update_data["department"] = department
        if employee_search is not None:
            update_data["employee_search"] = employee_search
        if subject:
            update_data["subject"] = subject
        if description:
            update_data["description"] = description
        
        # Handle send option change
        if send_option:
            send_opt = self.validate_send_option(send_option)
            update_data["send_option"] = send_opt
        
        # Handle scheduled time
        if scheduled_time:
            scheduled_dt = self.parse_scheduled_time(scheduled_time)
            update_data["scheduled_time"] = scheduled_dt
        
        # Handle image update
        if image:
            # Delete old image if exists
            if notification.image_path and os.path.exists(notification.image_path):
                try:
                    os.remove(notification.image_path)
                except Exception:
                    pass
            
            image_path, image_filename = self.save_image(image, notification.subject)
            update_data["image_path"] = image_path
            update_data["image_filename"] = image_filename
        
        return self.repository.update(db, notification, update_data)
    
    def delete_notification(self, db: Session, notification_id: int) -> dict:
        """Delete a notification"""
        notification = self.get_notification_by_id(db, notification_id)
        subject = notification.subject
        self.repository.delete_with_image(db, notification)
        return {"message": f"Notification '{subject}' deleted successfully"}
    
    def get_notification_image_path(self, db: Session, notification_id: int) -> str:
        """Get notification image path"""
        notification = self.get_notification_by_id(db, notification_id)
        
        if not notification.image_path:
            raise HTTPException(
                status_code=404, 
                detail="This notification does not have an image"
            )
        
        if not os.path.exists(notification.image_path):
            raise HTTPException(
                status_code=404, 
                detail="Image file not found on server"
            )
        
        return notification.image_path
    
    def send_notification(self, db: Session, notification_id: int) -> dict:
        """Manually trigger sending a notification"""
        notification = self.get_notification_by_id(db, notification_id)
        
        if notification.is_sent:
            raise HTTPException(
                status_code=400, 
                detail="Notification already sent"
            )
        
        # Mark as sent
        notification = self.repository.mark_as_sent(db, notification)
        
        return {
            "message": "Notification sent successfully",
            "notification_id": notification.id,
            "sent_at": notification.sent_at
        }
    
    def get_notification_stats(self, db: Session) -> dict:
        """Get notification statistics"""
        return self.repository.get_stats(db)



"""
Policy Service - Business Logic Layer for Policies
"""


class PolicyService:
    """Service for Policy business logic"""
    
    def __init__(self):
        self.repository = PolicyRepository()
        self.upload_dir = Path("uploads/policies")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_policy_type(self, type_str: str) -> models.PolicyType:
        """Validate and convert policy type"""
        try:
            return models.PolicyType(type_str)
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="Invalid policy type. Use 'uploaded' or 'online'"
            )
    
    def save_policy_file(self, file: UploadFile, policy_name: str) -> Tuple[str, str]:
        """Save policy file and return path and filename"""
        file_extension = os.path.splitext(file.filename)[1]
        file_name = f"{policy_name.replace(' ', '_')}{file_extension}"
        file_path = self.upload_dir / file_name
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return str(file_path), file_name
    
    def create_policy(
        self,
        db: Session,
        policy_name: str,
        type: str,
        content: Optional[str] = None,
        file: Optional[UploadFile] = None,
        actions: Optional[bool] = None
    ) -> models.Policy:
        """Create a new policy"""
        policy_type = self.validate_policy_type(type)
        
        if policy_type == models.PolicyType.UPLOADED:
            if not file:
                raise HTTPException(
                    status_code=400, 
                    detail="File is required for uploaded policy type"
                )
            
            file_path, file_name = self.save_policy_file(file, policy_name)
            
            policy_data = {
                "policy_name": policy_name,
                "type": policy_type,
                "file_path": file_path,
                "file_name": file_name,
                "actions": actions
            }
        
        elif policy_type == models.PolicyType.ONLINE:
            if not content:
                raise HTTPException(
                    status_code=400, 
                    detail="Content is required for online policy type"
                )
            
            policy_data = {
                "policy_name": policy_name,
                "type": policy_type,
                "content": content,
                "actions": actions
            }
        
        return self.repository.create(db, policy_data)
    
    def get_all_policies(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Policy]:
        """Get all policies with pagination"""
        return self.repository.get_all(db, skip, limit)
    
    def get_policy_by_id(self, db: Session, policy_id: int) -> models.Policy:
        """Get policy by ID"""
        policy = self.repository.get_by_id(db, policy_id)
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        return policy
    
    def update_policy(
        self,
        db: Session,
        policy_id: int,
        policy_name: Optional[str] = None,
        type: Optional[str] = None,
        content: Optional[str] = None,
        file: Optional[UploadFile] = None,
        actions: Optional[bool] = None
    ) -> models.Policy:
        """Update an existing policy"""
        policy = self.get_policy_by_id(db, policy_id)
        
        update_data = {}
        
        # Update policy name if provided
        if policy_name is not None and policy_name.strip():
            update_data["policy_name"] = policy_name.strip()
            policy.policy_name = policy_name.strip()
        
        # Determine target type
        target_type = None
        if type:
            target_type = self.validate_policy_type(type)
        
        # Handle type change or updates
        if target_type == models.PolicyType.UPLOADED:
            if file:
                # Delete old file if exists
                if policy.file_path and os.path.exists(policy.file_path):
                    try:
                        os.remove(policy.file_path)
                    except Exception:
                        pass
                
                # Save new file
                file_path, file_name = self.save_policy_file(file, policy.policy_name)
                update_data["file_path"] = file_path
                update_data["file_name"] = file_name
                update_data["content"] = None
            elif policy.type != models.PolicyType.UPLOADED:
                raise HTTPException(
                    status_code=400,
                    detail="File is required when changing to uploaded policy type"
                )
            
            update_data["type"] = models.PolicyType.UPLOADED
        
        elif target_type == models.PolicyType.ONLINE:
            if content is not None:
                update_data["content"] = content
                
                # Delete file if switching from uploaded to online
                if policy.file_path and os.path.exists(policy.file_path):
                    try:
                        os.remove(policy.file_path)
                    except Exception:
                        pass
                
                update_data["file_path"] = None
                update_data["file_name"] = None
            elif policy.type != models.PolicyType.ONLINE:
                raise HTTPException(
                    status_code=400,
                    detail="Content is required when changing to online policy type"
                )
            
            update_data["type"] = models.PolicyType.ONLINE
        
        else:
            # No type change, just update existing policy's content/file
            if policy.type == models.PolicyType.UPLOADED and file:
                if policy.file_path and os.path.exists(policy.file_path):
                    try:
                        os.remove(policy.file_path)
                    except Exception:
                        pass
                
                file_path, file_name = self.save_policy_file(file, policy.policy_name)
                update_data["file_path"] = file_path
                update_data["file_name"] = file_name
            
            elif policy.type == models.PolicyType.ONLINE and content is not None:
                update_data["content"] = content
        
        if actions is not None:
            update_data["actions"] = actions
        
        return self.repository.update(db, policy, update_data)
    
    def delete_policy(self, db: Session, policy_id: int) -> dict:
        """Delete a policy"""
        policy = self.get_policy_by_id(db, policy_id)
        policy_name = policy.policy_name
        self.repository.delete_with_file(db, policy)
        return {"message": f"Policy '{policy_name}' deleted successfully"}
    
    def get_policy_file_path(self, db: Session, policy_id: int) -> Tuple[str, str]:
        """Get policy file path for download"""
        policy = self.get_policy_by_id(db, policy_id)
        
        if policy.type != models.PolicyType.UPLOADED or not policy.file_path:
            raise HTTPException(
                status_code=400, 
                detail="This policy does not have a downloadable file"
            )
        
        if not os.path.exists(policy.file_path):
            raise HTTPException(
                status_code=404, 
                detail="Policy file not found on server"
            )
        
        return policy.file_path, policy.file_name
    


"""
Wedding Anniversary Service - Business Logic Layer for Wedding Anniversary Greetings
"""

class WeddingAnniversaryService:
    """Service for Wedding Anniversary Greeting business logic"""
    
    def __init__(self):
        self.repository = WeddingAnniversaryRepository()
    
    def get_all_greetings(self, db: Session) -> List[models.WeddingAnniversaryGreeting]:
        """Get all wedding anniversary greetings"""
        return self.repository.get_all(db)
    
    def get_greeting_by_id(self, db: Session, greeting_id: int) -> models.WeddingAnniversaryGreeting:
        """Get greeting by ID"""
        greeting = self.repository.get_by_id(db, greeting_id)
        if not greeting:
            raise HTTPException(
                status_code=404, 
                detail="Wedding anniversary greeting not found"
            )
        return greeting
    
    def create_greeting(
        self, 
        db: Session, 
        greeting_data: schemas.WeddingAnniversaryGreetingBase
    ) -> models.WeddingAnniversaryGreeting:
        """Create a new wedding anniversary greeting"""
        return self.repository.create(db, greeting_data.dict())
    
    def update_greeting(
        self,
        db: Session,
        greeting_id: int,
        greeting_data: schemas.WeddingAnniversaryGreetingBase
    ) -> models.WeddingAnniversaryGreeting:
        """Update an existing wedding anniversary greeting"""
        greeting = self.get_greeting_by_id(db, greeting_id)
        return self.repository.update(db, greeting, greeting_data.dict())
    
    def delete_greeting(self, db: Session, greeting_id: int) -> dict:
        """Delete a wedding anniversary greeting"""
        greeting = self.get_greeting_by_id(db, greeting_id)
        self.repository.delete(db, greeting)
        return {"message": f"Wedding anniversary greeting {greeting_id} deleted successfully"}
    
    def get_enabled_greetings(self, db: Session) -> List[models.WeddingAnniversaryGreeting]:
        """Get all enabled wedding anniversary greetings"""
        return self.repository.get_enabled_greetings(db)
    

"""
Work Anniversary Service - Business Logic Layer for Work Anniversary Greetings
"""


class WorkAnniversaryService:
    """Service for Work Anniversary Greeting business logic"""
    
    def __init__(self):
        self.repository = WorkAnniversaryRepository()
    
    def get_all_greetings(self, db: Session) -> List[models.WorkAnniversaryGreeting]:
        """Get all work anniversary greetings"""
        return self.repository.get_all(db)
    
    def get_greeting_by_id(self, db: Session, greeting_id: int) -> models.WorkAnniversaryGreeting:
        """Get greeting by ID"""
        greeting = self.repository.get_by_id(db, greeting_id)
        if not greeting:
            raise HTTPException(status_code=404, detail="Greeting not found")
        return greeting
    
    def create_greeting(
        self, 
        db: Session, 
        greeting_data: schemas.WorkAnniversaryGreetingCreate
    ) -> models.WorkAnniversaryGreeting:
        """Create a new work anniversary greeting"""
        return self.repository.create(db, greeting_data.dict())
    
    def update_greeting(
        self,
        db: Session,
        greeting_id: int,
        greeting_data: schemas.WorkAnniversaryGreetingCreate
    ) -> models.WorkAnniversaryGreeting:
        """Update an existing work anniversary greeting"""
        greeting = self.get_greeting_by_id(db, greeting_id)
        return self.repository.update(db, greeting, greeting_data.dict())
    
    def delete_greeting(self, db: Session, greeting_id: int) -> dict:
        """Delete a work anniversary greeting"""
        greeting = self.get_greeting_by_id(db, greeting_id)
        self.repository.delete(db, greeting)
        return {"message": f"Greeting {greeting_id} deleted successfully"}
    
    def get_enabled_greetings(self, db: Session) -> List[models.WorkAnniversaryGreeting]:
        """Get all enabled work anniversary greetings"""
        return self.repository.get_enabled_greetings(db)