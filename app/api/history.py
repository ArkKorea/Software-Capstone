from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.history import UnifiedHistoryResponse
from app.core.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.services.history import get_view_logs_service
from app.crud.history import add_or_update_view_log
from app.schemas.history import HistoryLogRequest

router = APIRouter()

@router.get("/history", response_model=UnifiedHistoryResponse)
def get_view_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_view_logs_service(db, current_user)

@router.post("/history/add", status_code=204)
def add_view_history(
    req: HistoryLogRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    add_or_update_view_log(
        db=db,
        user_id=current_user.id,
        target_type=req.type,
        target_id=req.target_id
    )
    return  # 204 No Content