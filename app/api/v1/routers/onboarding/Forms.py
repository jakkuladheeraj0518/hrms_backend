import os
import json
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.utils.helpers import parse_date, ensure_upload_dir
from app.database.session import get_db
from app.models.onboarding import Candidate
from app.schemas.onboarding import CandidateResponse, CandidateStatusUpdate

# Ensure upload directory exists
UPLOAD_DIR = ensure_upload_dir("uploads")

router = APIRouter(prefix="/forms", tags=["Forms"])


# -------------------- 1️⃣ Get all candidates --------------------
@router.get("/", response_model=List[CandidateResponse])
def get_candidates(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).all()
    # parse documents JSON string into Python list for each candidate
    for c in candidates:
        if getattr(c, "documents", None):
            try:
                c.documents = json.loads(c.documents)
            except Exception:
                c.documents = []
        else:
            c.documents = None
    return candidates


# -------------------- 2️⃣ Get single candidate --------------------
@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    # if model has a documents column (may be optional in some branches), parse safely
    docs_val = getattr(candidate, "documents", None)
    if docs_val:
        try:
            candidate.documents = json.loads(docs_val)
        except Exception:
            candidate.documents = []
    else:
        # ensure attribute exists for response models but keep None when absent
        if hasattr(candidate, "documents"):
            candidate.documents = None
    return candidate


# -------------------- 3️⃣ Create candidate with Aadhaar + PAN (Text + File) --------------------
@router.post("/", response_model=CandidateResponse)
async def create_candidate(
    # Basic Info
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),

    # Optional Info
    firstName: Optional[str] = Form(None),
    lastName: Optional[str] = Form(None),
    dob: Optional[str] = Form(None),
    homePhone: Optional[str] = Form(None),
    emergencyContact: Optional[str] = Form(None),
    fatherName: Optional[str] = Form(None),
    fatherPhone: Optional[str] = Form(None),
    fatherDOB: Optional[str] = Form(None),
    motherName: Optional[str] = Form(None),
    motherPhone: Optional[str] = Form(None),
    motherDOB: Optional[str] = Form(None),
    marital: Optional[str] = Form(None),
    blood: Optional[str] = Form(None),
    drivingLicense: Optional[str] = Form(None),
    uan: Optional[str] = Form(None),
    esi: Optional[str] = Form(None),
    presentAddress: Optional[str] = Form(None),
    permanentAddress: Optional[str] = Form(None),
    bankName: Optional[str] = Form(None),
    ifsc: Optional[str] = Form(None),
    accountNumber: Optional[str] = Form(None),
    accountName: Optional[str] = Form(None),

    # Aadhaar (text + upload)
    aadhaarNumber: Optional[str] = Form(None),
    aadhaarFile: Optional[UploadFile] = File(None),

    # PAN (text + upload)
    panNumber: Optional[str] = Form(None),
    panFile: Optional[UploadFile] = File(None),

    db: Session = Depends(get_db),
):
    aadhaar_path, pan_path = None, None

    # Save uploaded files (if any)
    if aadhaarFile:
        aadhaar_filename = f"{name.replace(' ', '_')}_aadhaar_{aadhaarFile.filename}"
        aadhaar_path = os.path.join(UPLOAD_DIR, aadhaar_filename)
        with open(aadhaar_path, "wb") as f:
            f.write(await aadhaarFile.read())

    if panFile:
        pan_filename = f"{name.replace(' ', '_')}_pan_{panFile.filename}"
        pan_path = os.path.join(UPLOAD_DIR, pan_filename)
        with open(pan_path, "wb") as f:
            f.write(await panFile.read())

    # Build documents list for uploaded files
    documents_list = []
    if aadhaar_path:
        documents_list.append({
            "type": "aadhaar",
            "filename": os.path.basename(aadhaar_path),
            "path": aadhaar_path,
        })
    if pan_path:
        documents_list.append({
            "type": "pan",
            "filename": os.path.basename(pan_path),
            "path": pan_path,
        })

    # Create candidate
    candidate_kwargs = dict(
        name=name,
        email=email,
        phone=phone,
        firstName=firstName,
        lastName=lastName,
        dob=parse_date(dob, required=False),
        homePhone=homePhone,
        emergencyContact=emergencyContact,
        fatherName=fatherName,
        fatherPhone=fatherPhone,
        fatherDOB=parse_date(fatherDOB, required=False),
        motherName=motherName,
        motherPhone=motherPhone,
        motherDOB=parse_date(motherDOB, required=False),
        marital=marital,
        blood=blood,
        drivingLicense=drivingLicense,
        # textual IDs
        aadhaar=aadhaarNumber,
        pan=panNumber,
        # uploaded file paths
        aadhaarFile=aadhaar_path,
        panFile=pan_path,
        uan=uan,
        esi=esi,
        presentAddress=presentAddress,
        permanentAddress=permanentAddress,
        bankName=bankName,
        ifsc=ifsc,
        accountNumber=accountNumber,
        accountName=accountName,
        status="Pending",
    )

    # only include documents if the ORM model declares the attribute
    if documents_list and hasattr(Candidate, "documents"):
        candidate_kwargs["documents"] = json.dumps(documents_list)

    candidate = Candidate(**candidate_kwargs)

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    # Convert documents JSON (if any) to Python list before returning
    docs_val = getattr(candidate, "documents", None)
    if docs_val:
        try:
            candidate.documents = json.loads(docs_val)
        except Exception:
            candidate.documents = []
    else:
        if hasattr(candidate, "documents"):
            candidate.documents = None

    return candidate


@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: int,
    # Basic Info
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),

    # Optional Info
    firstName: Optional[str] = Form(None),
    lastName: Optional[str] = Form(None),
    dob: Optional[str] = Form(None),
    homePhone: Optional[str] = Form(None),
    emergencyContact: Optional[str] = Form(None),
    fatherName: Optional[str] = Form(None),
    fatherPhone: Optional[str] = Form(None),
    fatherDOB: Optional[str] = Form(None),
    motherName: Optional[str] = Form(None),
    motherPhone: Optional[str] = Form(None),
    motherDOB: Optional[str] = Form(None),
    marital: Optional[str] = Form(None),
    blood: Optional[str] = Form(None),
    drivingLicense: Optional[str] = Form(None),
    uan: Optional[str] = Form(None),
    esi: Optional[str] = Form(None),
    presentAddress: Optional[str] = Form(None),
    permanentAddress: Optional[str] = Form(None),
    bankName: Optional[str] = Form(None),
    ifsc: Optional[str] = Form(None),
    accountNumber: Optional[str] = Form(None),
    accountName: Optional[str] = Form(None),

    # Aadhaar (text + upload)
    aadhaarNumber: Optional[str] = Form(None),
    aadhaarFile: Optional[UploadFile] = File(None),

    # PAN (text + upload)
    panNumber: Optional[str] = Form(None),
    panFile: Optional[UploadFile] = File(None),

    db: Session = Depends(get_db),
):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Save uploaded files if provided and update file path fields
    if aadhaarFile:
        aadhaar_filename = f"{(name or candidate.name).replace(' ', '_')}_aadhaar_{aadhaarFile.filename}"
        aadhaar_path = os.path.join(UPLOAD_DIR, aadhaar_filename)
        with open(aadhaar_path, "wb") as f:
            f.write(await aadhaarFile.read())
        candidate.aadhaarFile = aadhaar_path

    if panFile:
        pan_filename = f"{(name or candidate.name).replace(' ', '_')}_pan_{panFile.filename}"
        pan_path = os.path.join(UPLOAD_DIR, pan_filename)
        with open(pan_path, "wb") as f:
            f.write(await panFile.read())
        candidate.panFile = pan_path

    # Update simple fields if provided
    # Textual IDs
    if aadhaarNumber is not None:
        candidate.aadhaar = aadhaarNumber
    if panNumber is not None:
        candidate.pan = panNumber

    # Other fields
    for attr, val in {
        "name": name,
        "email": email,
        "phone": phone,
        "firstName": firstName,
        "lastName": lastName,
        "homePhone": homePhone,
        "emergencyContact": emergencyContact,
        "fatherName": fatherName,
        "fatherPhone": fatherPhone,
        "motherName": motherName,
        "motherPhone": motherPhone,
        "marital": marital,
        "blood": blood,
        "drivingLicense": drivingLicense,
        "uan": uan,
        "esi": esi,
        "presentAddress": presentAddress,
        "permanentAddress": permanentAddress,
        "bankName": bankName,
        "ifsc": ifsc,
        "accountNumber": accountNumber,
        "accountName": accountName,
    }.items():
        if val is not None:
            setattr(candidate, attr, val)

    # dates
    if dob is not None:
        candidate.dob = parse_date(dob, required=False)
    if fatherDOB is not None:
        candidate.fatherDOB = parse_date(fatherDOB, required=False)
    if motherDOB is not None:
        candidate.motherDOB = parse_date(motherDOB, required=False)

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    # ensure documents attribute exists and is parsed when present
    docs_val = getattr(candidate, "documents", None)
    if docs_val:
        try:
            candidate.documents = json.loads(docs_val)
        except Exception:
            candidate.documents = []
    else:
        if hasattr(candidate, "documents"):
            candidate.documents = None

    return candidate


@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # attempt to remove uploaded files if paths are present
    try:
        if getattr(candidate, "aadhaarFile", None):
            try:
                os.remove(candidate.aadhaarFile)
            except Exception:
                pass
        if getattr(candidate, "panFile", None):
            try:
                os.remove(candidate.panFile)
            except Exception:
                pass
    except Exception:
        # Continue even if file deletion fails
        pass

    db.delete(candidate)
    db.commit()

    return {"detail": "Candidate deleted"}


# -------------------- 6️⃣ Update candidate status --------------------
@router.patch("/{candidate_id}/status", response_model=CandidateResponse)
def update_candidate_status(candidate_id: int, status_update: CandidateStatusUpdate, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    candidate.status = status_update.status
    db.commit()
    db.refresh(candidate)
    return candidate
