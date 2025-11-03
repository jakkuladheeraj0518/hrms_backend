from pydantic import BaseModel
from datetime import date


# 1) Initiated Exit
class InitiatedExitCreate(BaseModel):
    employee_name: str
    employee_code: str
    resignation_date: date | None = None
    notice_period: int | None = None
    last_working_date: date | None = None
    reason_of_exit: str | None = None
    remarks: str | None = None
    trying_to_retain: bool | None = False


class InitiatedExitResponse(InitiatedExitCreate):
    id: int
    status: str | None = "Initiated"

    class Config:
        orm_mode = True


# 2) Pending Exits grid item (derived from initiated/pending tables)
class PendingExitItem(BaseModel):
    id: int
    employee_name: str
    exit_date: date | None = None
    exit_reason: str | None = None
    status: str | None = None


# 3) Ex-Employees grid item
class ExEmployeeItem(BaseModel):
    id: int
    employee_name: str
    employee_code: str
    exit_date: date
    reason_of_exit: str
    remarks: str | None = None
