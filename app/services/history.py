# services/history.py
from sqlalchemy.orm import Session
from app.models.view_log import ViewLog
from app.models.user import User
from app.schemas.history import UnifiedHistoryResponse

from app.services.detail_service import (
    get_product_detail_service,
    get_bundle_detail_service,
    get_supplier_detail_service,
)

def get_view_logs_service(db: Session, user: User) -> UnifiedHistoryResponse:
    logs = (
        db.query(ViewLog)
        .filter(ViewLog.user_id == user.id)
        .order_by(ViewLog.viewed_at.desc())
        .limit(30)
        .all()
    )

    result = []

    for log in logs:
        try:
            if log.type == "food" and log.food:
                product = get_product_detail_service(db, log.food_id, user)
                result.append({
                    "type": "food",
                    "viewed_at": log.viewed_at,
                    "data": product
                })
            elif log.type == "bundle" and log.bundle:
                bundle = get_bundle_detail_service(db, log.bundle_id, user)
                result.append({
                    "type": "bundle",
                    "viewed_at": log.viewed_at,
                    "data": bundle
                })
            elif log.type == "supplier" and log.supplier:
                store = get_supplier_detail_service(db, log.supplier_id, user)
                result.append({
                    "type": "supplier",
                    "viewed_at": log.viewed_at,
                    "data": store
                })
        except Exception as e:
            print(f"[WARN] 히스토리 변환 실패: {e}")

    return {"history": result}
