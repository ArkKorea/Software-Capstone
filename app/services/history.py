# services/history.py
from sqlalchemy.orm import Session
from app.models.view_log import ViewLog
from app.models.user import User
from app.schemas.history import ViewLogItem, ViewLogResponse


def get_view_logs_service(db: Session, user: User) -> ViewLogResponse:
    logs = (
        db.query(ViewLog)
        .filter(ViewLog.user_id == user.id)
        .order_by(ViewLog.viewed_at.desc())
        .limit(30)
        .all()
    )

    result = []
    for log in logs:
        if log.type == "food" and log.food:
            result.append(ViewLogItem(
                type="food",
                id=log.food_id,
                name=log.food.name,
                image_url=log.food.image_url,
                viewed_at=log.viewed_at
            ))
        elif log.type == "bundle" and log.bundle:
            result.append(ViewLogItem(
                type="bundle",
                id=log.bundle_id,
                name=log.bundle.name,
                image_url=log.bundle.image_url,
                viewed_at=log.viewed_at
            ))
        elif log.type == "supplier" and log.supplier:
            result.append(ViewLogItem(
                type="supplier",
                id=log.supplier_id,
                name=log.supplier.name,
                image_url=log.supplier.image_url,
                viewed_at=log.viewed_at
            ))

    return ViewLogResponse(products=result)