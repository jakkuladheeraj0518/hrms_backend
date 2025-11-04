# app/api/v1/routers/bulk_updatesrouters/employee_records_router.py

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException,
)
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.bulk_updatesservices import EmployeeRecordsService
from app.utils.bulk_updatesutils import create_employee_template

router = APIRouter(prefix="/employee-records", tags=["Employee Records"])


# ============================================================
# 📤 Download Blank Excel Template
# ============================================================
@router.get("/template", summary="Download employee Excel template")
async def download_template():
    """
    Returns a pre-formatted Excel template for employee record uploads.
    """
    try:
        return create_employee_template()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating template: {e}")


# ============================================================
# 📥 Upload Employee Records from Excel
# ============================================================
@router.post("/upload", summary="Upload employee Excel data")
async def upload_employee_records(
    file: UploadFile = File(...),
    create_masters: bool = Form(True),
    send_mobile: bool = Form(True),
    send_web: bool = Form(True),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload and process employee Excel data.
    Automatically creates master entries (if enabled) 
    and updates biometric/work profile data.
    """
    try:
        # ✅ Validate file type
        if not file.filename.endswith((".xlsx", ".xls")):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel file (.xlsx).")

        # ✅ Read file bytes
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # ✅ Process the uploaded Excel file
        return await EmployeeRecordsService.process_excel(
            file_bytes=contents,
            db=db,
            create_masters=create_masters,
            send_mobile=send_mobile,
            send_web=send_web
        )

        # return JSONResponse(content={"message": "File processed successfully", "details": result.body})

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")
#routers/employee_records.py

