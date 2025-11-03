from fastapi import APIRouter
from . import (
    attendanceemployee,
    attendancemodal,
    calendartable,
    dailyattendance,
    dailypunch,
    leavecorrection,
    manualattendance,
    monthlyattendance,
)

router = APIRouter()

router.include_router(attendanceemployee.router)
router.include_router(attendancemodal.router)
router.include_router(calendartable.router)
router.include_router(dailyattendance.router)
router.include_router(dailypunch.router)
router.include_router(leavecorrection.router)
router.include_router(manualattendance.router)
router.include_router(monthlyattendance.router)
