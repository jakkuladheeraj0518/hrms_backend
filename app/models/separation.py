from sqlalchemy import Column, Integer, String, Date, Boolean
from app.database.base import Base


# 1) Initiated Exit
class InitiatedExit(Base):
    __tablename__ = "initiated_exits"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    employee_code = Column(String, nullable=False)
    resignation_date = Column(Date, nullable=False)
    notice_period = Column(Integer, default=0)
    last_working_date = Column(Date, nullable=False)
    reason_of_exit = Column(String, nullable=False)
    remarks = Column(String)
    trying_to_retain = Column(Boolean, default=False)
    status = Column(String, default="Initiated")


# 2) Pending Exit
class PendingExit(Base):
    __tablename__ = "pending_exits"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    employee_code = Column(String, nullable=False)
    exit_date = Column(Date, nullable=False)
    reason_of_exit = Column(String, nullable=False)
    status = Column(String, default="Pending")


# 3) Ex Employee
class ExEmployee(Base):
    __tablename__ = "ex_employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    employee_code = Column(String, nullable=False)
    exit_date = Column(Date, nullable=False)
    reason_of_exit = Column(String, nullable=False)
    remarks = Column(String)
