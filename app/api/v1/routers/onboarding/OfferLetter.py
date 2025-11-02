from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.onboarding import OfferLetterForm, OfferLetter
from app.models.onboarding import OfferLetterTemplate
from app.schemas.onboarding import Template, TemplateCreate, GenerateLetterRequest, GenerateLetterResponse

router = APIRouter(prefix="/offerletter", tags=["Offer Letter"])

@router.post("/templates", response_model=Template)
def create_template(template: TemplateCreate, db: Session = Depends(get_db)):
    from app.models.onboarding import OfferLetterTemplate
    t = OfferLetterTemplate(name=template.name, content=template.content)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


# Get all templates
@router.get("/templates", response_model=List[Template])
def get_templates(db: Session = Depends(get_db)):
    return db.query(OfferLetterTemplate).all()


@router.post("/generate", response_model=GenerateLetterResponse)
def generate_letter(data: GenerateLetterRequest, db: Session = Depends(get_db)):
    from app.models.onboarding import OfferLetterTemplate
    tpl = db.query(OfferLetterTemplate).filter(OfferLetterTemplate.id == data.template_id).first()
    if not tpl:
        raise HTTPException(status_code=404, detail="Template not found")
    generated = tpl.content
    for k, v in data.field_values.items():
        generated = generated.replace(f"{{{k}}}", v)
    return {"generated_letter": generated}
