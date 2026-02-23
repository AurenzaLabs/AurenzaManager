from fastapi import APIRouter

try:
    from backend.database import projects_col, expenses_col
except ModuleNotFoundError:
    from database import projects_col, expenses_col

router = APIRouter()

@router.get("/pnl")
def pnl():
    revenue = sum(p["value"] for p in projects_col.find())
    expense = sum(e["amount"] for e in expenses_col.find({"status": "APPROVED"}))
    return {
        "revenue": revenue,
        "expense": expense,
        "profit": revenue - expense
    }
