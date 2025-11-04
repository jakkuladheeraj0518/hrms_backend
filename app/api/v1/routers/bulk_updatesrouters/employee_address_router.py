import io
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.utils.bulk_updatesutils import create_excel_template
from app.services.bulk_updatesservices import EmployeeAddressService

router = APIRouter(prefix="/employee-address", tags=["Employee Address"])


# 📤 Download Template
@router.get("/download-template")
async def download_template():
    columns = [
        "employee_id",
        "address_line1",
        "address_line2",
        "city",
        "state",
        "country",
        "pincode",
        "address_type",
    ]
    return create_excel_template(columns, "Employee_Address_Template.xlsx")


# 📥 Upload Excel
@router.post("/upload")
async def upload_employee_addresses(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    return await EmployeeAddressService.process_upload(file, db)
