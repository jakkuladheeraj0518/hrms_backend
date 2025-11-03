
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models
from datetime import datetime
from sqlalchemy import desc
import os
from app.models.hr_management import PolicyType, LetterTemplate, LetterHistory, Notification, SendOption, Policy, WeddingAnniversaryGreeting, WorkAnniversaryGreeting,Alert,BirthdayGreeting



"""
Alert Repository - Data Access Layer for Alerts
"""
class AlertRepository:
    """Repository for Alert model"""
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Alert]:
        """Get all alerts with pagination"""
        return db.query(models.Alert).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, alert_id: int) -> Optional[models.Alert]:
        """Get alert by ID"""
        return db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    
    def create(self, db: Session, alert_data: dict) -> models.Alert:
        """Create a new alert"""
        db_alert = models.Alert(**alert_data)
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        return db_alert
    
    def update(self, db: Session, alert: models.Alert, update_data: dict) -> models.Alert:
        """Update an existing alert"""
        for key, value in update_data.items():
            if value is not None:
                setattr(alert, key, value)
        db.commit()
        db.refresh(alert)
        return alert
    
    def delete(self, db: Session, alert: models.Alert) -> bool:
        """Delete an alert"""
        db.delete(alert)
        db.commit()
        return True
    
    def get_active_alerts(self, db: Session) -> List[models.Alert]:
        """Get all active alerts"""
        return db.query(models.Alert).filter(models.Alert.active == True).all()
    
    def get_by_name(self, db: Session, alert_name: str) -> Optional[models.Alert]:
        """Get alert by name"""
        return db.query(models.Alert).filter(models.Alert.alert_name == alert_name).first()
    


"""
Birthday Greeting Repository - Data Access Layer for Birthday Greetings
"""


class BirthdayGreetingRepository:
    """Repository for BirthdayGreeting model"""
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.BirthdayGreeting]:
        """Get all birthday greetings with pagination"""
        return db.query(models.BirthdayGreeting).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, greeting_id: int) -> Optional[models.BirthdayGreeting]:
        """Get birthday greeting by ID"""
        return db.query(models.BirthdayGreeting).filter(models.BirthdayGreeting.id == greeting_id).first()
    
    def create(self, db: Session, greeting_data: dict) -> models.BirthdayGreeting:
        """Create a new birthday greeting"""
        db_greeting = models.BirthdayGreeting(**greeting_data)
        db.add(db_greeting)
        db.commit()
        db.refresh(db_greeting)
        return db_greeting
    
    def update(self, db: Session, greeting: models.BirthdayGreeting, update_data: dict) -> models.BirthdayGreeting:
        """Update an existing birthday greeting"""
        for key, value in update_data.items():
            if value is not None:
                setattr(greeting, key, value)
        db.commit()
        db.refresh(greeting)
        return greeting
    
    def delete(self, db: Session, greeting: models.BirthdayGreeting) -> bool:
        """Delete a birthday greeting"""
        db.delete(greeting)
        db.commit()
        return True
    
    def get_enabled_greetings(self, db: Session) -> List[models.BirthdayGreeting]:
        """Get all enabled birthday greetings"""
        return db.query(models.BirthdayGreeting).filter(
            models.BirthdayGreeting.enable == True
        ).all()
    

"""
Letter Template & History Repositories - Data Access Layer
"""



class LetterTemplateRepository:
    """Repository for LetterTemplate model"""

    def get_all(self, db: Session) -> List[LetterTemplate]:
        """Get all letter templates"""
        return db.query(LetterTemplate).all()

    def get_by_id(self, db: Session, template_id: int) -> Optional[LetterTemplate]:
        """Get a letter template by ID"""
        return db.query(LetterTemplate).filter(LetterTemplate.id == template_id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[LetterTemplate]:
        """Get a letter template by name"""
        return db.query(LetterTemplate).filter(LetterTemplate.name == name).first()

    def get_offer_letters(self, db: Session) -> List[LetterTemplate]:
        """Get all offer letter templates"""
        return db.query(LetterTemplate).filter(LetterTemplate.is_offer_letter == True).all()

    def get_non_offer_letters(self, db: Session) -> List[LetterTemplate]:
        """Get all non-offer letter templates"""
        return db.query(LetterTemplate).filter(LetterTemplate.is_offer_letter == False).all()

    def create(self, db: Session, template_data: dict) -> LetterTemplate:
        """Create a new letter template"""
        template = LetterTemplate(**template_data)
        db.add(template)
        db.commit()
        db.refresh(template)
        return template

    def update(self, db: Session, template: LetterTemplate, update_data: dict) -> LetterTemplate:
        """Update an existing letter template"""
        for key, value in update_data.items():
            if value is not None:
                setattr(template, key, value)
        template.last_updated = datetime.utcnow()
        db.commit()
        db.refresh(template)
        return template

    def delete(self, db: Session, template: LetterTemplate) -> bool:
        """Delete a letter template"""
        db.delete(template)
        db.commit()
        return True

    def exists_by_name(self, db: Session, name: str) -> bool:
        """Check if a letter template exists by name"""
        return db.query(LetterTemplate).filter(LetterTemplate.name == name).first() is not None

    def count_total(self, db: Session) -> int:
        """Count total letter templates"""
        return db.query(LetterTemplate).count()

    def count_offer_letters(self, db: Session) -> int:
        """Count offer letter templates"""
        return db.query(LetterTemplate).filter(LetterTemplate.is_offer_letter == True).count()


class LetterHistoryRepository:
    """Repository for LetterHistory model"""

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[LetterHistory]:
        """Get all letter history entries with pagination"""
        return db.query(LetterHistory).order_by(LetterHistory.requested_at.desc()).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, history_id: int) -> Optional[LetterHistory]:
        """Get a letter history entry by ID"""
        return db.query(LetterHistory).filter(LetterHistory.id == history_id).first()

    def get_by_letter_name(self, db: Session, letter_name: str) -> List[LetterHistory]:
        """Get letter history entries by letter name"""
        return db.query(LetterHistory).filter(LetterHistory.letter_name == letter_name)\
                 .order_by(LetterHistory.requested_at.desc()).all()

    def get_by_status(self, db: Session, status: str) -> List[LetterHistory]:
        """Get letter history entries by status"""
        return db.query(LetterHistory).filter(LetterHistory.status == status)\
                 .order_by(LetterHistory.requested_at.desc()).all()

    def get_recent(self, db: Session, limit: int = 10) -> List[LetterHistory]:
        """Get recent letter history entries"""
        return db.query(LetterHistory).order_by(LetterHistory.requested_at.desc()).limit(limit).all()

    def create(self, db: Session, history_data: dict) -> LetterHistory:
        """Create a new letter history entry"""
        history = LetterHistory(**history_data)
        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    def delete(self, db: Session, history: LetterHistory) -> bool:
        """Delete a letter history entry"""
        db.delete(history)
        db.commit()
        return True

    def count_total(self, db: Session) -> int:
        """Count total letter history entries"""
        return db.query(LetterHistory).count()

    def count_by_status(self, db: Session, status: str) -> int:
        """Count letter history entries by status"""
        return db.query(LetterHistory).filter(LetterHistory.status == status).count()
    



"""
Notification Repository - Data Access Layer for Notifications
"""



class NotificationRepository:
    """Repository for Notification model"""
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Notification]:
        """Get all notifications with pagination"""
        return db.query(models.Notification).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, notification_id: int) -> Optional[models.Notification]:
        """Get notification by ID"""
        return db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    
    def create(self, db: Session, notification_data: dict) -> models.Notification:
        """Create a new notification"""
        db_notification = models.Notification(**notification_data)
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        return db_notification
    
    def update(self, db: Session, notification: models.Notification, update_data: dict) -> models.Notification:
        """Update an existing notification"""
        for key, value in update_data.items():
            if value is not None:
                setattr(notification, key, value)
        db.commit()
        db.refresh(notification)
        return notification
    
    def delete(self, db: Session, notification: models.Notification) -> bool:
        """Delete a notification"""
        db.delete(notification)
        db.commit()
        return True
    
    def get_all_with_filters(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        location: Optional[str] = None,
        department: Optional[str] = None,
        is_sent: Optional[bool] = None
    ) -> List[models.Notification]:
        """Get notifications with optional filters"""
        query = db.query(models.Notification)
        
        if location:
            query = query.filter(models.Notification.location == location)
        
        if department:
            query = query.filter(models.Notification.department == department)
        
        if is_sent is not None:
            query = query.filter(models.Notification.is_sent == is_sent)
        
        return query.order_by(desc(models.Notification.created_at)).offset(skip).limit(limit).all()
    
    def get_pending_notifications(self, db: Session) -> List[models.Notification]:
        """Get all pending (unsent) notifications"""
        return db.query(models.Notification).filter(
            models.Notification.is_sent == False
        ).all()
    
    def get_scheduled_notifications(self, db: Session) -> List[models.Notification]:
        """Get notifications scheduled for later"""
        return db.query(models.Notification).filter(
            models.Notification.send_option == models.SendOption.SEND_LATER,
            models.Notification.is_sent == False
        ).all()
    
    def mark_as_sent(self, db: Session, notification: models.Notification) -> models.Notification:
        """Mark notification as sent"""
        from datetime import datetime
        notification.is_sent = True
        notification.sent_at = datetime.now()
        db.commit()
        db.refresh(notification)
        return notification
    
    def get_stats(self, db: Session) -> dict:
        """Get notification statistics"""
        stats = {
            "total_notifications": db.query(models.Notification).count(),
            "sent_notifications": db.query(models.Notification).filter(
                models.Notification.is_sent == True
            ).count(),
            "pending_notifications": db.query(models.Notification).filter(
                models.Notification.is_sent == False
            ).count(),
            "by_location": {
                "all_locations": db.query(models.Notification).filter(
                    models.Notification.location == "all_locations"
                ).count(),
                "bangalore": db.query(models.Notification).filter(
                    models.Notification.location == "bangalore"
                ).count(),
                "hyderabad": db.query(models.Notification).filter(
                    models.Notification.location == "hyderabad"
                ).count()
            },
            "by_department": {
                "all_departments": db.query(models.Notification).filter(
                    models.Notification.department == "all_departments"
                ).count(),
                "product_development": db.query(models.Notification).filter(
                    models.Notification.department == "product_development"
                ).count(),
                "hr_executive": db.query(models.Notification).filter(
                    models.Notification.department == "hr_executive"
                ).count(),
                "technical_support": db.query(models.Notification).filter(
                    models.Notification.department == "technical_support"
                ).count()
            }
        }
        return stats
    
    def delete_with_image(self, db: Session, notification: models.Notification) -> bool:
        """Delete notification and associated image file"""
        # Delete associated image if exists
        if notification.image_path and os.path.exists(notification.image_path):
            try:
                os.remove(notification.image_path)
            except Exception:
                pass
        
        db.delete(notification)
        db.commit()
        return True
    

"""
Policy Repository - Data Access Layer for Policies
"""


class PolicyRepository:
    """Repository for Policy model"""
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Policy]:
        """Get all policies with pagination"""
        return db.query(models.Policy).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, policy_id: int) -> Optional[models.Policy]:
        """Get policy by ID"""
        return db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    
    def create(self, db: Session, policy_data: dict) -> models.Policy:
        """Create a new policy"""
        db_policy = models.Policy(**policy_data)
        db.add(db_policy)
        db.commit()
        db.refresh(db_policy)
        return db_policy
    
    def update(self, db: Session, policy: models.Policy, update_data: dict) -> models.Policy:
        """Update an existing policy"""
        for key, value in update_data.items():
            if value is not None:
                setattr(policy, key, value)
        db.commit()
        db.refresh(policy)
        return policy
    
    def delete(self, db: Session, policy: models.Policy) -> bool:
        """Delete a policy"""
        db.delete(policy)
        db.commit()
        return True
    
    def get_by_type(self, db: Session, policy_type: models.PolicyType) -> List[models.Policy]:
        """Get policies by type"""
        return db.query(models.Policy).filter(models.Policy.type == policy_type).all()
    
    def get_uploaded_policies(self, db: Session) -> List[models.Policy]:
        """Get all uploaded policies"""
        return self.get_by_type(db, models.PolicyType.UPLOADED)
    
    def get_online_policies(self, db: Session) -> List[models.Policy]:
        """Get all online policies"""
        return self.get_by_type(db, models.PolicyType.ONLINE)
    
    def delete_with_file(self, db: Session, policy: models.Policy) -> bool:
        """Delete policy and associated file"""
        # Delete associated file if exists
        if policy.file_path and os.path.exists(policy.file_path):
            try:
                os.remove(policy.file_path)
            except Exception:
                pass
        
        db.delete(policy)
        db.commit()
        return True
    
    def get_by_name(self, db: Session, policy_name: str) -> Optional[models.Policy]:
        """Get policy by name"""
        return db.query(models.Policy).filter(models.Policy.policy_name == policy_name).first()
    

"""
Wedding Anniversary Repository - Data Access Layer for Wedding Anniversary Greetings
"""



class WeddingAnniversaryRepository:
    """Repository for WeddingAnniversaryGreeting model"""
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.WeddingAnniversaryGreeting]:
        """Get all wedding anniversary greetings with pagination"""
        return db.query(models.WeddingAnniversaryGreeting).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, greeting_id: int) -> Optional[models.WeddingAnniversaryGreeting]:
        """Get wedding anniversary greeting by ID"""
        return db.query(models.WeddingAnniversaryGreeting).filter(
            models.WeddingAnniversaryGreeting.id == greeting_id
        ).first()
    
    def create(self, db: Session, greeting_data: dict) -> models.WeddingAnniversaryGreeting:
        """Create a new wedding anniversary greeting"""
        db_greeting = models.WeddingAnniversaryGreeting(**greeting_data)
        db.add(db_greeting)
        db.commit()
        db.refresh(db_greeting)
        return db_greeting
    
    def update(self, db: Session, greeting: models.WeddingAnniversaryGreeting, update_data: dict) -> models.WeddingAnniversaryGreeting:
        """Update an existing wedding anniversary greeting"""
        for key, value in update_data.items():
            if value is not None:
                setattr(greeting, key, value)
        db.commit()
        db.refresh(greeting)
        return greeting
    
    def delete(self, db: Session, greeting: models.WeddingAnniversaryGreeting) -> bool:
        """Delete a wedding anniversary greeting"""
        db.delete(greeting)
        db.commit()
        return True
    
    def get_enabled_greetings(self, db: Session) -> List[models.WeddingAnniversaryGreeting]:
        """Get all enabled wedding anniversary greetings"""
        return db.query(models.WeddingAnniversaryGreeting).filter(
            models.WeddingAnniversaryGreeting.enable == True
        ).all()
    

"""
Work Anniversary Repository - Data Access Layer for Work Anniversary Greetings
"""



class WorkAnniversaryRepository:
    """Repository for WorkAnniversaryGreeting model"""
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.WorkAnniversaryGreeting]:
        """Get all work anniversary greetings with pagination"""
        return db.query(models.WorkAnniversaryGreeting).offset(skip).limit(limit).all()
    
    def get_by_id(self, db: Session, greeting_id: int) -> Optional[models.WorkAnniversaryGreeting]:
        """Get work anniversary greeting by ID"""
        return db.query(models.WorkAnniversaryGreeting).filter(
            models.WorkAnniversaryGreeting.id == greeting_id
        ).first()
    
    def create(self, db: Session, greeting_data: dict) -> models.WorkAnniversaryGreeting:
        """Create a new work anniversary greeting"""
        db_greeting = models.WorkAnniversaryGreeting(**greeting_data)
        db.add(db_greeting)
        db.commit()
        db.refresh(db_greeting)
        return db_greeting
    
    def update(self, db: Session, greeting: models.WorkAnniversaryGreeting, update_data: dict) -> models.WorkAnniversaryGreeting:
        """Update an existing work anniversary greeting"""
        for key, value in update_data.items():
            if value is not None:
                setattr(greeting, key, value)
        db.commit()
        db.refresh(greeting)
        return greeting
    
    def delete(self, db: Session, greeting: models.WorkAnniversaryGreeting) -> bool:
        """Delete a work anniversary greeting"""
        db.delete(greeting)
        db.commit()
        return True
    
    def get_enabled_greetings(self, db: Session) -> List[models.WorkAnniversaryGreeting]:
        """Get all enabled work anniversary greetings"""
        return db.query(models.WorkAnniversaryGreeting).filter(
            models.WorkAnniversaryGreeting.enable == True
        ).all()