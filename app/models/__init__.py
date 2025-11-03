from app.database.base import Base
from app.models.superadmin import (
    Company,
    Domain,
    Package,
    Transaction,
    Subscription
    

)

# Import onboarding models so package-level `app.models` exposes them
from app.models.onboarding import (
    OnboardingEmployee,
    Employees,
    Candidate,
    OfferLetter,
    OfferLetterForm,
    OfferLetterTemplate,
    OnboardingForm,
    OnboardingCandidate,
    FinalizedForm,
)



from app.models.hr_management import (
    Alert,
    BirthdayGreeting,
    LetterTemplate, 
    LetterHistory,
    Notification,
    SendOption,
    Policy,
    PolicyType,
    WeddingAnniversaryGreeting,
    WorkAnniversaryGreeting
    
    )


__all__ = [
    "Base",
    "Company",
    "Domain",
    "Package",
    "Transaction",
    "Subscription",
    # Onboarding models
    "OnboardingEmployee",
    "Employees",
    "Candidate",
    "OfferLetter",
    "OfferLetterForm",
    "OfferLetterTemplate",
    "OnboardingForm",
    "OnboardingCandidate",
    "FinalizedForm",


    # HR Management models
    "Alert",
    "BirthdayGreeting",
    "LetterTemplate",
    "LetterHistory",
    "Notification",
    "SendOption",
    "Policy",
    "PolicyType",
    "WeddingAnniversaryGreeting",
    "WorkAnniversaryGreeting"
]



    