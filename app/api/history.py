from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.history import UnifiedHistoryResponse
from app.core.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.services.history import get_view_logs_service

router = APIRouter()

@router.get("/history", response_model=UnifiedHistoryResponse)
def get_view_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_view_logs_service(db, current_user)
