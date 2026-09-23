from fastapi import APIRouter, HTTPException
from app.services.paint_service import PaintService
router = APIRouter()
@router.get("/history")
def history(limit: int = 50):
    with PaintService() as s: return {"items": s.history(limit)}
@router.get("/history/{run_id}")
def history_one(run_id: int):
    with PaintService() as s:
        r = s.get_run(run_id)
        if not r: raise HTTPException(404)
        return r
