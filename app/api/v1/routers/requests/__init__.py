from fastapi import APIRouter

router = APIRouter()

from . import (
    leave_request,
    missed_punch_request,
    compoff,
    helpdesk,
    claim_requests,
    time_relaxation_request,
    shift_roster_request,
    week_roaster,
    strike_requests,
    visit_punch_request,
    workflow_request,
    shift_roster
)

__all__ = [
    "leave_request",
    "missed_punch_request",
    "compoff",
    "helpdesk",
    "claim_requests",
    "time_relaxation_request",
    "shift_roster_request",
    "week_roaster",
    "strike_requests",
    "visit_punch_request",
    "workflow_request",
    "shift_roster",
    "router"
]
