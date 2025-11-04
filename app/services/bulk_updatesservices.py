from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import EmployeeBulkUpdatesBiometric
from app.repositories.bulk_updatesrepositories import EmployeeBiometricRepository
from app.schemas.bulk_updatesschemas import EmployeeBiometricOut, EmployeeBiometricCreate, EmployeeBiometricUpdate


class EmployeeBiometricService:

    @staticmethod
    async def list_biometrics(session: AsyncSession, **filters):
        employees =await EmployeeBiometricRepository.get_all_employees(session, **filters)

        response = []
        for emp in employees:
            biometric = emp.biometric_record
            response.append(
                EmployeeBiometricOut(
                    id=biometric.id if biometric else 0,
                    employee_id=emp.id,
                    employee_code=emp.employee_code,
                    name=emp.employee_name or f"{emp.first_name} {emp.last_name or ''}".strip(),
                    location=emp.location.name if emp.location else None,
                    cost_center=emp.cost_center.name if emp.cost_center else None,
                    business_unit=emp.business_unit_rel.name if emp.business_unit_rel else None,
                    department=emp.department.name if emp.department else None,
                    biometric_code=biometric.biometric_code if biometric else None,
                )
            )
        return response

    @staticmethod
    async def create_biometric(data: EmployeeBiometricCreate, session: AsyncSession):
        emp = await EmployeeBiometricRepository.get_employee_by_id(session, data.employee_id)
        if not emp:
            raise HTTPException(status_code=404, detail="Employee not found")

        existing = await EmployeeBiometricRepository.get_biometric_by_employee_id(session, emp.id)
        if existing:
            raise HTTPException(status_code=400, detail="Biometric record already exists for this employee")

        biometric = EmployeeBulkUpdatesBiometric(
            employee_id=emp.id,
            employee_code=emp.employee_code,
            name=emp.employee_name or f"{emp.first_name} {emp.last_name or ''}".strip(),
            location=emp.location.name if emp.location else None,
            department=emp.department.name if emp.department else None,
            cost_center=emp.cost_center.name if emp.cost_center else None,
            business_unit=emp.business_unit_rel.name if emp.business_unit_rel else None,
            biometric_code=data.biometric_code,
        )

        return await EmployeeBiometricRepository.create_biometric(session, biometric)

    @staticmethod
    async def update_biometric(employee_id: int, data: EmployeeBiometricUpdate, session: AsyncSession):
        biometric = await EmployeeBiometricRepository.get_biometric_by_employee_id(session, employee_id)
        if not biometric:
            raise HTTPException(status_code=404, detail="Employee biometric not found")

        return await EmployeeBiometricRepository.update_biometric(session, biometric, data.biometric_code)

import json
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.bulk_updatesrepositories import BulkUpdatesRepository
from app.schemas.bulk_updatesschemas import BulkUpdateResponse, EmployeePreview
from app.utils.bulk_updatesutils import parse_selections


class BulkUpdatesService:
    """Handles business logic for bulk updates."""

    @staticmethod
    async def get_metadata(session: AsyncSession):
        locs, depts, desigs, ccs = await BulkUpdatesRepository.get_all_metadata(session)
        to_names = lambda items: [x.name for x in items]
        return {
            "locations": to_names(locs),
            "departments": to_names(depts),
            "designations": to_names(desigs),
            "cost_centers": to_names(ccs),
        }

    @staticmethod
    async def apply_bulk_update(payload, session: AsyncSession) -> BulkUpdateResponse:
        selections = payload.selections
        salary_settings = payload.salarySettings
        attendance_settings = payload.attendanceSettings
        travel_settings = payload.travelSettings
        community_settings = payload.communitySettings
        workman_settings = payload.workmanSettings

        filters = parse_selections(selections.model_dump())

        employees = await BulkUpdatesRepository.filter_employees(
            session=session,
            locations=filters.get("locations"),
            departments=filters.get("departments"),
            designations=filters.get("designations"),
            cost_centers=filters.get("cost_centers"),
        )

        if not employees:
            return BulkUpdateResponse(matched_count=0, updated_count=0, preview=[])
        consolidated = {
        "selections": selections.model_dump(),
        "salarySettings": salary_settings.model_dump() if salary_settings else None,
        "attendanceSettings": attendance_settings.model_dump() if attendance_settings else None,
        "travelSettings": travel_settings.model_dump() if travel_settings else None,
        "communitySettings": community_settings.model_dump() if community_settings else None,
        "workmanSettings": workman_settings.model_dump() if workman_settings else None,
    }
        options_json = json.dumps(consolidated)
        updated_count = 0
        preview = []

        for emp in employees:
            await BulkUpdatesRepository.get_or_create_options(session, emp.id, options_json)
            updated_count += 1
            preview.append(
                EmployeePreview(
                    id=emp.id,
                    employee_code=emp.employee_code,
                    first_name=emp.first_name,
                    last_name=emp.last_name,
                    email=emp.email,
                    mobile=emp.mobile,
                )
            )

        session.commit()

        return BulkUpdateResponse(
            matched_count=len(employees),
            updated_count=updated_count,
            preview=preview[:20]
        )
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.bulk_updatesrepositories import EmployeeAddressRepository
from app.utils.bulk_updatesutils import read_excel_file


class EmployeeAddressService:
    REQUIRED_COLUMNS = [
        "employee_id",
        "address_line1",
        "city",
        "state",
        "country",
        "pincode",
        "address_type",
    ]

    @staticmethod
    async def process_upload(file, db: AsyncSession):
        """Main logic for uploading employee addresses."""
        headers, rows = read_excel_file(file)

        # ✅ Validate columns
        for col in EmployeeAddressService.REQUIRED_COLUMNS:
            if col not in headers:
                raise HTTPException(status_code=400, detail=f"Missing column: {col}")

        success_count = 0
        skipped = []
        failed = []

        for i, row in enumerate(rows, start=2):
            employee_id = row.get("employee_id")
            address_type = row.get("address_type", "Permanent")

            if not employee_id:
                failed.append({"row": i, "error": "Missing employee_id"})
                continue

            # ✅ Validate employee existence
            employee = await EmployeeAddressRepository.get_employee_by_id(db, employee_id)
            if not employee:
                failed.append({"row": i, "error": f"Employee ID {employee_id} not found"})
                continue

            # ✅ Check duplicates
            existing = await EmployeeAddressRepository.get_existing_addresses(db, employee_id, address_type)
            if existing:
                skipped.append({
                    "row": i,
                    "employee_id": employee_id,
                    "reason": f"Found {len(existing)} existing address(es) for type '{address_type}' — skipped",
                })
                continue

            # ✅ Add new address
            try:
                address_data = {
                    "employee_id": employee_id,
                    "address_line1": row["address_line1"],
                    "address_line2": row.get("address_line2"),
                    "city": row.get("city"),
                    "state": row.get("state"),
                    "country": row.get("country"),
                    "pincode": str(row.get("pincode")),
                    "address_type": address_type,
                }
                await EmployeeAddressRepository.add_address(db, address_data)
                success_count += 1
            except Exception as e:
                failed.append({"row": i, "error": str(e)})

        db.commit()

        return {
            "message": "Employee addresses upload completed",
            "successful": success_count,
            "skipped_duplicates": len(skipped),
            "failed_rows": len(failed),
            "details": {"skipped": skipped, "failed": failed},
        }
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.bulk_updatesrepositories import EmployeeBankRepository
from app.schemas.bulk_updatesschemas import EmployeeBankResponse, EmployeeBankCreate


class EmployeeBankService:
    @staticmethod
    async def get_all_employee_bank_details(
        db: AsyncSession,
        business_unit_id=None,
        location_id=None,
        department_id=None,
    ):
        """Service to get employees and their bank details."""
        employees = await EmployeeBankRepository.get_all_employees(
            db, business_unit_id, location_id, department_id
        )

        if not employees:
            return []

        responses = []
        for emp in employees:
            bank = emp.bank_details
            responses.append(
                EmployeeBankResponse(
                    id=bank.id if bank else None,
                    employee_id=emp.id,
                    employee_code=emp.employee_code,
                    employee_name=f"{emp.first_name} {emp.last_name or ''}".strip(),
                    department=emp.department.name if emp.department else "",
                    location=emp.location.name if emp.location else "",
                    cost_center=emp.cost_center.name if emp.cost_center else "",
                    bank_name=bank.bank_name if bank else "",
                    ifsc_code=bank.ifsc_code if bank else "",
                    account_no=bank.account_no if bank else "",
                    verified=bank.verified if bank else False,
                )
            )
        return responses

    @staticmethod
    async def update_employee_bank_details(updates: list[EmployeeBankCreate], db: AsyncSession):
        """Service to create or update bank details."""
        for item in updates:
            employee = await EmployeeBankRepository.get_employee_by_id(db, item.employee_id)
            if not employee:
                raise HTTPException(status_code=404, detail=f"Employee ID {item.employee_id} not found")

            bank = await EmployeeBankRepository.get_employee_bank(db, item.employee_id)
            if bank:
                bank.bank_name = item.bank_name
                bank.ifsc_code = item.ifsc_code
                bank.account_no = item.account_no
                bank.verified = item.verified
            else:
                bank_record = EmployeeBulkUpdatesBank(
    employee_id=item.employee_id,
    bank_name=item.bank_name,
    ifsc_code=item.ifsc_code,
    account_no=item.account_no,
    verified=item.verified,
)

                await EmployeeBankRepository.create_employee_bank(
                    db, bank_record
                )

        db.commit()
        return {"message": "Bank details updated successfully"}

    @staticmethod
    async def get_employees_for_dropdown(db: AsyncSession):
        """Return basic employee info for UI dropdowns."""
        employees = await EmployeeBankRepository.get_all_employees(db)
        return [
            {
                "id": emp.id,
                "employee_code": emp.employee_code,
                "name": f"{emp.first_name} {emp.last_name or ''}".strip(),
            }
            for emp in employees
        ]

# services/employee_records_service.py
import traceback
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.models.bulk_updatesmodels import (
    EmployeeBulkUpdates,
    BulkLocation,
    BulkDepartment,
    BulkDesignation,
    BulkCostCenter,
    BulkShiftPolicy,
    BulkWeekOffPolicy,
    EmployeeBulkUpdatesBank,
)
from app.repositories.bulk_updatesrepositories import EmployeeRecordsRepository
from app.utils.bulk_updatesutils import clean_header, clean_cell, load_excel


class EmployeeRecordsService:
    @staticmethod
    async def process_excel(file_bytes: bytes, db, create_masters: bool, send_mobile: bool, send_web: bool):
        try:
            # ✅ Load Excel
            ws = load_excel(file_bytes)
            rows = list(ws.iter_rows(values_only=True))
            if len(rows) < 2:
                raise HTTPException(status_code=400, detail="No data rows found in Excel")

            # ✅ Normalize headers
            headers = [clean_header(c) for c in rows[0]]
            header_pos = {h: i for i, h in enumerate(headers)}

            def get_cell(row, name):
                idx = header_pos.get(name.lower())
                if idx is None or idx >= len(row):
                    return None
                return clean_cell(row[idx])

            # ✅ Collect master values
            masters_found = {
                "locations": set(),
                "departments": set(),
                "designations": set(),
                "cost_centers": set(),
                "shift_policies": set(),
                "week_off_policies": set(),
            }

            parsed = []

            # 🟢 Parse each row
            for row in rows[1:]:
                if all(cell is None for cell in row):
                    continue

                emp_code = get_cell(row, "employee_code")
                if not emp_code:
                    continue

                # ✅ Master names
                loc_name = get_cell(row, "location_name")
                dep_name = get_cell(row, "department_name")
                desig_name = get_cell(row, "designation_name")
                cost_name = get_cell(row, "cost_center_name")
                shift_name = get_cell(row, "shift_policy_name")
                week_name = get_cell(row, "week_off_policy_name")

                # Track masters found
                for k, v in [
                    ("locations", loc_name),
                    ("departments", dep_name),
                    ("designations", desig_name),
                    ("cost_centers", cost_name),
                    ("shift_policies", shift_name),
                    ("week_off_policies", week_name),
                ]:
                    if v:
                        masters_found[k].add(v)

                # ✅ Resolve master references
                location = await EmployeeRecordsRepository.get_or_create_master(db, BulkLocation, loc_name, create_masters)
                department = await EmployeeRecordsRepository.get_or_create_master(db, BulkDepartment, dep_name, create_masters)
                designation = await EmployeeRecordsRepository.get_or_create_master(db, BulkDesignation, desig_name, create_masters)
                cost_center = await EmployeeRecordsRepository.get_or_create_master(db, BulkCostCenter, cost_name, create_masters)
                shift_policy = await EmployeeRecordsRepository.get_or_create_master(db, BulkShiftPolicy, shift_name, create_masters)
                week_off_policy = await EmployeeRecordsRepository.get_or_create_master(db, BulkWeekOffPolicy, week_name, create_masters)

                # ✅ Fetch or create employee
                emp = await EmployeeRecordsRepository.get_by_code(db, emp_code)

                if emp:
                    emp.first_name = get_cell(row, "first_name")
                    emp.last_name = get_cell(row, "last_name")
                    emp.email = get_cell(row, "email")
                    emp.mobile = get_cell(row, "mobile")
                    emp.date_of_joining = get_cell(row, "date_of_joining")
                    emp.location_id = location.id if location else None
                    emp.department_id = department.id if department else None
                    emp.designation_id = designation.id if designation else None
                    emp.cost_center_id = cost_center.id if cost_center else None
                    emp.shift_policy_id = shift_policy.id if shift_policy else None
                    emp.week_off_policy_id = week_off_policy.id if week_off_policy else None
                    emp.notes = get_cell(row, "notes")
                else:
                    emp = EmployeeBulkUpdates(
                        employee_code=emp_code,
                        first_name=get_cell(row, "first_name"),
                        last_name=get_cell(row, "last_name"),
                        email=get_cell(row, "email"),
                        mobile=get_cell(row, "mobile"),
                        date_of_joining=get_cell(row, "date_of_joining"),
                        location_id=location.id if location else None,
                        department_id=department.id if department else None,
                        designation_id=designation.id if designation else None,
                        cost_center_id=cost_center.id if cost_center else None,
                        shift_policy_id=shift_policy.id if shift_policy else None,
                        week_off_policy_id=week_off_policy.id if week_off_policy else None,
                        notes=get_cell(row, "notes"),
                    )
                    db.add(emp)

                parsed.append(emp)

            # ✅ Commit once
            EmployeeRecordsRepository.commit(db)

            # ✅ Structured JSON output
            return JSONResponse(
                status_code=200,
                content={
                    "parsed_count": len(parsed),
                    "parsed_preview": [
                        {
                            "employee_code": e.employee_code,
                            "first_name": e.first_name,
                            "last_name": e.last_name,
                            "email": e.email,
                            "mobile": e.mobile,
                        }
                        for e in parsed[:10]
                    ],
                    "masters_found": {k: list(v) for k, v in masters_found.items()},
                    "create_masters": create_masters,
                    "send_mobile": send_mobile,
                    "send_web": send_web,
                },
            )

        except Exception as e:
            print("❌ Error in process_excel:", e)
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Error processing Excel: {str(e)}")

# services/salary_deductions_service.py
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.bulk_updatesmodels import SalaryDeduction
from app.schemas.bulk_updatesschemas import SalaryDeductionCreate, SalaryDeductionOut, SalaryDeductionBase, EmployeeSimple
from app.repositories.bulk_updatesrepositories import SalaryDeductionsRepository


class SalaryDeductionsService:

    # 🔹 List salary deductions (with filters)
    @staticmethod
    async def list_salary_deductions(
        db: AsyncSession,
        business_unit_id: Optional[int] = None,
        location_id: Optional[int] = None,
        cost_center_id: Optional[int] = None,
        department_id: Optional[int] = None,
    ):
        employees = await SalaryDeductionsRepository.get_employees_with_deductions(
            db, business_unit_id, location_id, cost_center_id, department_id
        )

        response = []
        for emp in employees:
            deduction = emp.salary_deduction
            response.append(
                {
                    "id": deduction.id if deduction else 0,
                    "employee_id": emp.id,
                    "employee_code": emp.employee_code,
                    "name": f"{emp.first_name} {emp.last_name or ''}".strip(),
                    "location": emp.location.name if emp.location else None,
                    "department": emp.department.name if emp.department else None,
                    "cost_center": emp.cost_center.name if emp.cost_center else None,
                    "business_unit": emp.business_unit.name if emp.business_unit else None,
                    "gi": deduction.gi if deduction else None,
                    "gratuity": deduction.gratuity if deduction else None,
                       # ✅ Add missing fields
                    "last_updated": deduction.last_updated if deduction else None,
                   "employee": {
                        "id": emp.id,
                        "employee_code": emp.employee_code,
                        "first_name": emp.first_name,      # ✅ Add this
                        "last_name": emp.last_name,        # optional if schema includes it
                        "name": f"{emp.first_name} {emp.last_name or ''}".strip(),
                        "department": emp.department.name if emp.department else None,
                        "location": emp.location.name if emp.location else None,
                    }if emp else None,
                }
            )
        return response

    # 🔹 Create a salary deduction
    @staticmethod
    async def create_salary_deduction(
        db: AsyncSession, payload: SalaryDeductionCreate
    ) -> SalaryDeductionOut:
        employee = await SalaryDeductionsRepository.get_employee_by_id(db, payload.employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        deduction = SalaryDeduction(
            employee_id=payload.employee_id,
            gi=payload.gi,
            gratuity=payload.gratuity,
        )

        deduction = await SalaryDeductionsRepository.create_deduction(db, deduction)

        db.refresh(
            deduction,
            attribute_names=["employee"]
        )
        db.refresh(
            deduction.employee,
            attribute_names=["business_unit", "location", "department", "cost_center", "designation"]
        )

        emp = deduction.employee
        return SalaryDeductionOut(
            id=deduction.id,
            employee_id=emp.id,
            gi=deduction.gi,
            gratuity=deduction.gratuity,
            last_updated=deduction.last_updated,
            employee=EmployeeSimple(
                id=emp.id,
                employee_code=emp.employee_code,
                first_name=emp.first_name,
                last_name=emp.last_name,
                employee_name=f"{emp.first_name} {emp.last_name or ''}".strip(),
                email=emp.email,
                position=emp.position,
                designation=emp.designation.name if emp.designation else None,
                department=emp.department.name if emp.department else None,
                location=emp.location.name if emp.location else None,
                business_unit=emp.business_unit.name if emp.business_unit else None,
                cost_center=emp.cost_center.name if emp.cost_center else None,
            ),
        )

    # 🔹 Update GI / Gratuity
    @staticmethod
    async def update_salary_deduction(
        db: AsyncSession, deduction_id: int, payload: SalaryDeductionBase
    ) -> SalaryDeductionOut:
        deduction = await SalaryDeductionsRepository.get_deduction_by_id(db, deduction_id)
        if not deduction:
            raise HTTPException(status_code=404, detail="Salary deduction not found")

        if payload.gi is not None:
            deduction.gi = payload.gi
        if payload.gratuity is not None:
            deduction.gratuity = payload.gratuity

        deduction = await SalaryDeductionsRepository.update_deduction(db, deduction)

        emp = deduction.employee
        return SalaryDeductionOut(
            id=deduction.id,
            employee_id=emp.id,
            gi=deduction.gi,
            gratuity=deduction.gratuity,
            last_updated=deduction.last_updated,
            employee=EmployeeSimple(
                id=emp.id,
                employee_code=emp.employee_code,
                first_name=emp.first_name,
                last_name=emp.last_name,
                employee_name=f"{emp.first_name} {emp.last_name or ''}".strip(),
                email=emp.email,
                position=emp.position,
                designation=emp.designation.name if emp.designation else None,
                department=emp.department.name if emp.department else None,
                location=emp.location.name if emp.location else None,
                business_unit=emp.business_unit.name if emp.business_unit else None,
                cost_center=emp.cost_center.name if emp.cost_center else None,
            ),
        )

# services/salary_revision_service.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import app.models.bulk_updatesmodels as models
import app.schemas.bulk_updatesschemas as schemas
from app.repositories.bulk_updatesrepositories import SalaryRevisionRepository


class SalaryRevisionService:
    """Handles business logic for salary revisions"""

    @staticmethod
    async def get_all_salaries(
        db: AsyncSession,
        business_unit: Optional[str] = None,
        location: Optional[str] = None,
        department: Optional[str] = None,
    ) -> List[schemas.SalaryRevisionOut]:
        salary_records = await SalaryRevisionRepository.get_all_salaries(
            db, business_unit, location, department
        )

        response = []
        for s in salary_records:
            emp = s.employee
            response.append(
                schemas.SalaryRevisionOut(
                    id=s.id,
                    employee_id=s.employee_id,
                    basic=s.basic,
                    hra=s.hra,
                    sa=s.sa,
                    mda=s.mda,
                    ca=s.ca,
                    ta=s.ta,
                    effective_month=s.effective_month,
                    effective_year=s.effective_year,
                    remarks=s.remarks,
                    employee={
                        "id": emp.id,
                        "first_name": emp.first_name,
                        "last_name": emp.last_name,
                        "email": emp.email,
                        "department": getattr(emp.department, "name", None),
                        "location": getattr(emp.location, "name", None),
                        "business_unit": getattr(emp.business_unit, "name", None),
                        "name": f"{emp.first_name} {emp.last_name or ''}".strip(),
                        "cost_center": getattr(emp.cost_center, "name", None),
                    },
                )
            )

        return response

    @staticmethod
    async def create_or_update_salary(
        db: AsyncSession, salary: schemas.SalaryRevisionCreate
    ) -> schemas.SalaryRevisionOut:
        # ✅ Ensure employee exists
        employee = await SalaryRevisionRepository.get_employee_by_id(db, salary.employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail=f"Employee {salary.employee_id} not found")

        # ✅ Check existing revision
        existing = await SalaryRevisionRepository.get_existing_salary_revision(
            db, salary.employee_id, salary.effective_month, salary.effective_year
        )

        if existing:
            # Update
            existing.basic = salary.basic
            existing.hra = salary.hra
            existing.sa = salary.sa
            existing.mda = salary.mda
            existing.ca = salary.ca
            existing.ta = salary.ta
            existing.remarks = salary.remarks
            revision = await SalaryRevisionRepository.update_salary_revision(db, existing)
        else:
            # Create
            revision = models.SalaryRevision(**salary.dict())
            revision = await SalaryRevisionRepository.create_salary_revision(db, revision)

        # ✅ Prepare structured response
        employee_name = f"{employee.first_name} {employee.last_name or ''}".strip()

        return schemas.SalaryRevisionOut(
            id=revision.id,
            employee_id=revision.employee_id,
            basic=revision.basic,
            hra=revision.hra,
            sa=revision.sa,
            mda=revision.mda,
            ca=revision.ca,
            ta=revision.ta,
            effective_month=revision.effective_month,
            effective_year=revision.effective_year,
            remarks=revision.remarks,
            employee={
                "id": employee.id,
                "employee_code": employee.employee_code,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "employee_name": employee_name,
                "email": employee.email,
                "position": getattr(employee, "position", None),
                "designation": getattr(employee.designation, "name", None)
                if hasattr(employee.designation, "name")
                else str(employee.designation)
                if employee.designation
                else None,
                "department": getattr(employee.department, "name", None)
                if hasattr(employee.department, "name")
                else str(employee.department)
                if employee.department
                else None,
                "location": getattr(employee.location, "name", None)
                if hasattr(employee.location, "name")
                else str(employee.location)
                if employee.location
                else None,
                "business_unit": getattr(employee.business_unit, "name", None)
                if hasattr(employee.business_unit, "name")
                else str(employee.business_unit)
                if employee.business_unit
                else None,
                "cost_center": getattr(employee.cost_center, "name", None)
                if hasattr(employee.cost_center, "name")
                else str(employee.cost_center)
                if employee.cost_center
                else None,
            },
        )
#workprofile
from typing import List
from app.schemas.bulk_updatesschemas import EmployeeWorkProfileOut
from app.repositories.bulk_updatesrepositories import WorkProfileRepository


class WorkProfileService:
    @staticmethod
    async def list_work_profiles(
        session,
        business_unit_id=None,
        location_id=None,
        cost_center_id=None,
        department_id=None,
    ) -> List[EmployeeWorkProfileOut]:
        """Get formatted employee + work profile data."""
        employees = await WorkProfileRepository.fetch_all(
            session,
            business_unit_id,
            location_id,
            cost_center_id,
            department_id,
        )

        response = []
        for emp in employees:
            wp = emp.work_profile
            response.append(
                EmployeeWorkProfileOut(
                    id=wp.id if wp else 0,
                    employee_id=emp.id,
                    employee_code=emp.employee_code,
                    name=f"{emp.first_name} {emp.last_name or ''}".strip(),
                    location=wp.location if wp else None,
                    department=wp.department if wp else None,
                    cost_center=wp.cost_center if wp else None,
                    business_unit=wp.business_unit if wp else None,
                    designation=wp.designation if wp else None,
                    grade=wp.grade if wp else None,
                    employment_type=None,  # Adjust if you have this field
                    date_of_joining=None,  # Adjust if you have this field
                )
            )
        return response
