from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from app.models.bulk_updatesmodels import EmployeeBulkUpdates, EmployeeBulkUpdatesBiometric


class EmployeeBiometricRepository:

    @staticmethod
    async def get_all_employees(
        session: AsyncSession,
        business_unit_id: Optional[int] = None,
        location_id: Optional[int] = None,
        cost_center_id: Optional[int] = None,
        department_id: Optional[int] = None,
    ) -> List[EmployeeBulkUpdates]:
        query = select(EmployeeBulkUpdates)

        if location_id:
            query = query.where(EmployeeBulkUpdates.location_id == location_id)
        if department_id:
            query = query.where(EmployeeBulkUpdates.department_id == department_id)
        if cost_center_id:
            query = query.where(EmployeeBulkUpdates.cost_center_id == cost_center_id)

        result =  session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_employee_by_id(session: AsyncSession, employee_id: int) -> Optional[EmployeeBulkUpdates]:
        result = session.execute(select(EmployeeBulkUpdates).where(EmployeeBulkUpdates.id == employee_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_biometric_by_employee_id(session: AsyncSession, employee_id: int) -> Optional[EmployeeBulkUpdatesBiometric]:
        result =  session.execute(
            select(EmployeeBulkUpdatesBiometric).where(EmployeeBulkUpdatesBiometric.employee_id == employee_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_biometric(session: AsyncSession, biometric: EmployeeBulkUpdatesBiometric):
        session.add(biometric)
        session.commit()
        session.refresh(biometric)
        return biometric

    @staticmethod
    async def update_biometric(session: AsyncSession, biometric: EmployeeBulkUpdatesBiometric, biometric_code: str):
        biometric.biometric_code = biometric_code
        await session.commit()
        await session.refresh(biometric)
        return biometric
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.bulk_updatesmodels import (
    EmployeeBulkUpdates,
    BulkLocation,
    BulkDepartment,
    BulkDesignation,
    BulkCostCenter,
    EmployeeBulkUpdatesOptions,
)


class BulkUpdatesRepository:
    """Database operations for bulk updates."""

    @staticmethod
    async def get_all_metadata(session: AsyncSession):
        locs = ( session.execute(select(BulkLocation))).scalars().all()
        depts = ( session.execute(select(BulkDepartment))).scalars().all()
        desigs = ( session.execute(select(BulkDesignation))).scalars().all()
        ccs = ( session.execute(select(BulkCostCenter))).scalars().all()
        return locs, depts, desigs, ccs

    @staticmethod
    async def filter_employees(
        session: AsyncSession,
        locations: Optional[List[str]] = None,
        departments: Optional[List[str]] = None,
        designations: Optional[List[str]] = None,
        cost_centers: Optional[List[str]] = None,
    ) -> List[EmployeeBulkUpdates]:
        """Filter employees based on master names."""

        query = select(EmployeeBulkUpdates)

        if locations:
            query = query.join(BulkLocation).where(BulkLocation.name.in_(locations))
        if departments:
            query = query.join(BulkDepartment).where(BulkDepartment.name.in_(departments))
        if designations:
            query = query.join(BulkDesignation).where(BulkDesignation.name.in_(designations))
        if cost_centers:
            query = query.join(BulkCostCenter).where(BulkCostCenter.name.in_(cost_centers))

        result =  session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_employee_by_id(session: AsyncSession, emp_id: int) -> Optional[EmployeeBulkUpdates]:
        result =  session.execute(select(EmployeeBulkUpdates).where(EmployeeBulkUpdates.id == emp_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_or_create_options(session: AsyncSession, employee_id: int, options_json: str):
        """Upsert into EmployeeBulkUpdatesOptions."""
        result =  session.execute(
            select(EmployeeBulkUpdatesOptions).where(EmployeeBulkUpdatesOptions.employee_id == employee_id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.options = options_json
        else:
            new = EmployeeBulkUpdatesOptions(employee_id=employee_id, options=options_json)
            session.add(new)
        return True
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import app.models.bulk_updatesmodels as models


class EmployeeAddressRepository:
    @staticmethod
    async def get_employee_by_id(db: AsyncSession, employee_id: int):
        """Fetch an employee by ID."""
        result =  db.execute(select(models.EmployeeBulkUpdates).where(models.EmployeeBulkUpdates.id == employee_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_existing_addresses(db: AsyncSession, employee_id: int, address_type: str):
        """Fetch existing addresses of a given type for the employee."""
        result =  db.execute(
            select(models.EmployeeBulkUpdatesAddress).where(
                models.EmployeeBulkUpdatesAddress.employee_id == employee_id,
                models.EmployeeBulkUpdatesAddress.address_type == address_type,
            )
        )
        return result.scalars().all()

    @staticmethod
    async def add_address(db: AsyncSession, address_data: dict):
        """Insert new employee address record."""
        new_address = models.EmployeeBulkUpdatesAddress(**address_data)
        db.add(new_address)
        return new_address
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.bulk_updatesmodels import EmployeeBulkUpdates, EmployeeBulkUpdatesBank


class EmployeeBankRepository:
    @staticmethod
    async def get_all_employees(db: AsyncSession, business_unit_id=None, location_id=None, department_id=None):
        """Fetch all employees with optional filters and eager loading."""
        query = (
            select(EmployeeBulkUpdates)
            .options(
                selectinload(EmployeeBulkUpdates.bank_details),
                selectinload(EmployeeBulkUpdates.department),
                selectinload(EmployeeBulkUpdates.location),
                selectinload(EmployeeBulkUpdates.cost_center),
            )
        )

        # if business_unit_id:
        #     query = query.where(EmployeeBulkUpdates.cost_center_id == business_unit_id)
        if location_id:
            query = query.where(EmployeeBulkUpdates.location_id == location_id)
        if department_id:
            query = query.where(EmployeeBulkUpdates.department_id == department_id)

        result =  db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_employee_by_id(db: AsyncSession, employee_id: int):
        """Fetch employee by ID."""
        result =  db.execute(select(EmployeeBulkUpdates).where(EmployeeBulkUpdates.id == employee_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_employee_bank(db: AsyncSession, employee_id: int):
        """Fetch bank record for employee."""
        result =  db.execute(select(EmployeeBulkUpdatesBank).where(EmployeeBulkUpdatesBank.employee_id == employee_id))
        return result.scalar_one_or_none()  
    
    @staticmethod
    async def create_employee_bank(db: AsyncSession, bank_record: EmployeeBulkUpdatesBank):
        """Create new bank record."""
        db.add(bank_record)
        return bank_record

#repositories/employee_records_repository.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models.bulk_updatesmodels import (
    EmployeeBulkUpdates,
    BulkLocation,
    BulkDepartment,
    BulkDesignation,
    BulkCostCenter,
    BulkShiftPolicy,
    BulkWeekOffPolicy,
)

class EmployeeRecordsRepository:
    """Handles employee record creation and updates from Excel uploads."""

    @staticmethod
    async def get_or_create_master(db: AsyncSession, model, name: str, create_if_missing: bool = True):
        if not name:
            return None

        # ✅ Correct non-awaited select usage
        result = db.execute(select(model).where(model.name == name))
        instance = result.scalar_one_or_none()
        if instance:
            return instance

        if create_if_missing:
            new_instance = model(name=name)
            db.add(new_instance)
            db.flush()
            return new_instance

        return None

    @staticmethod
    async def get_by_code(db: AsyncSession, employee_code: str) -> Optional[EmployeeBulkUpdates]:
        """Fetch an employee by employee_code."""
        if not employee_code:
            return None

        # ✅ Only one await (for db.execute)
        result =  db.execute(
            select(EmployeeBulkUpdates).where(EmployeeBulkUpdates.employee_code == employee_code)
        )
        employee = result.scalar_one_or_none()  # ✅ no await
        return employee

    @staticmethod
    async def commit(db: AsyncSession):
        """Commit the transaction."""
        await db.commit()



# repositories/salary_deductions_repository.py
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.models.bulk_updatesmodels import SalaryDeduction, EmployeeBulkUpdates


class SalaryDeductionsRepository:

    # 🔹 Get employees (with related data + filters)
    @staticmethod
    async def get_employees_with_deductions(
        db: AsyncSession,
        business_unit_id: Optional[int] = None,
        location_id: Optional[int] = None,
        cost_center_id: Optional[int] = None,
        department_id: Optional[int] = None,
    ) -> List[EmployeeBulkUpdates]:
        query = (
            select(EmployeeBulkUpdates)
            .options(
                selectinload(EmployeeBulkUpdates.location),
                selectinload(EmployeeBulkUpdates.department),
                selectinload(EmployeeBulkUpdates.cost_center),
                selectinload(EmployeeBulkUpdates.salary_deduction),
            )
        )

        # if business_unit_id:
        #     query = query.where(EmployeeBulkUpdates.business_unit_id == business_unit_id)
        if location_id:
            query = query.where(EmployeeBulkUpdates.location_id == location_id)
        if cost_center_id:
            query = query.where(EmployeeBulkUpdates.cost_center_id == cost_center_id)
        if department_id:
            query = query.where(EmployeeBulkUpdates.department_id == department_id)

        result =  db.execute(query)
        return result.scalars().all()

    # 🔹 Get employee by ID
    @staticmethod
    async def get_employee_by_id(db: AsyncSession, employee_id: int) -> Optional[EmployeeBulkUpdates]:
        result =  db.execute(select(EmployeeBulkUpdates).where(EmployeeBulkUpdates.id == employee_id))
        return result.scalar_one_or_none()

    # 🔹 Get deduction by ID
    @staticmethod
    async def get_deduction_by_id(db: AsyncSession, deduction_id: int) -> Optional[SalaryDeduction]:
        result =  db.execute(
            select(SalaryDeduction)
            .options(selectinload(SalaryDeduction.employee))
            .where(SalaryDeduction.id == deduction_id)
        )
        return result.scalar_one_or_none()

    # 🔹 Create new deduction
    @staticmethod
    async def create_deduction(db: AsyncSession, deduction: SalaryDeduction):
        db.add(deduction)
        db.commit()
        db.refresh(deduction)
        return deduction

    # 🔹 Update existing deduction
    @staticmethod
    async def update_deduction(db: AsyncSession, deduction: SalaryDeduction):
        db.add(deduction)
        await db.commit()
        await db.refresh(deduction)
        return deduction

# repositories/salary_revision_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List, Optional
import app.models.bulk_updatesmodels as models


class SalaryRevisionRepository:
    """Handles DB operations for SalaryRevision"""

    @staticmethod
    async def get_all_salaries(
        db: AsyncSession,
        business_unit: Optional[str] = None,
        location: Optional[str] = None,
        department: Optional[str] = None,
    ) -> List[models.SalaryRevision]:
        query = (
            select(models.SalaryRevision)
            .options(joinedload(models.SalaryRevision.employee))
        )

        # if business_unit:
        #     query = query.where(
        #         models.SalaryRevision.employee.has(
        #             models.EmployeeBulkUpdates.business_unit.has(name=business_unit)
        #         )
        #     )
        if location:
            query = query.where(
                models.SalaryRevision.employee.has(
                    models.EmployeeBulkUpdates.location.has(name=location)
                )
            )
        if department:
            query = query.where(
                models.SalaryRevision.employee.has(
                    models.EmployeeBulkUpdates.department.has(name=department)
                )
            )

        result =  db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_employee_by_id(db: AsyncSession, employee_id: int):
        result =  db.execute(
            select(models.EmployeeBulkUpdates).where(models.EmployeeBulkUpdates.id == employee_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_existing_salary_revision(
        db: AsyncSession,
        employee_id: int,
        month: str,
        year: int,
    ):
        result =  db.execute(
            select(models.SalaryRevision).where(
                models.SalaryRevision.employee_id == employee_id,
                models.SalaryRevision.effective_month == month,
                models.SalaryRevision.effective_year == year,
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_salary_revision(db: AsyncSession, revision: models.SalaryRevision):
        db.add(revision)
        db.commit()
        db.refresh(revision)
        return revision

    @staticmethod
    async def update_salary_revision(db: AsyncSession, revision: models.SalaryRevision):
        db.add(revision)
        await db.commit()
        await db.refresh(revision)
        return revision

#workprofile
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.bulk_updatesmodels import EmployeeBulkUpdates
from app.models.bulk_updatesmodels import WorkProfile


class WorkProfileRepository:
    @staticmethod
    async def fetch_all(
        session: AsyncSession,
        business_unit_id: Optional[int] = None,
        location_id: Optional[int] = None,
        cost_center_id: Optional[int] = None,
        department_id: Optional[int] = None,
    ) -> List[EmployeeBulkUpdates]:
        """Fetch employees with their work profiles and filters."""
        query = (
            select(EmployeeBulkUpdates)
            .options(
                selectinload(EmployeeBulkUpdates.work_profile)
            )
        )

        # Apply filters dynamically
        # if business_unit_id:
        #     query = query.where(EmployeeBulkUpdates.business_unit_id == business_unit_id)
        if location_id:
            query = query.where(EmployeeBulkUpdates.location_id == location_id)
        if cost_center_id:
            query = query.where(EmployeeBulkUpdates.cost_center_id == cost_center_id)
        if department_id:
            query = query.where(EmployeeBulkUpdates.department_id == department_id)

        result =  session.execute(query)
        return result.scalars().all()
