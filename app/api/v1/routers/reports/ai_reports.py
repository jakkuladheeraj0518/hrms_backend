from fastapi import APIRouter, Query
from app.services.report_service import generate_ai_report  # ✅ correct function for AI reports

router = APIRouter(
    prefix="/api/v1/reports/ai",
    tags=["AI Reports"]
)

# 1️⃣ Get AI Reports list
@router.get("/ai-report/", summary="List Reports")
async def list_ai_reports():
    return {"message": "List of AI-generated reports"}

# 2️⃣ Generate AI Report
@router.post("/ai-report/", summary="Generate Report")
async def create_ai_report(
    query: str = Query(..., description="Your AI query text")
):
    result = generate_ai_report(query)
    return {"query": query, "report": result}
