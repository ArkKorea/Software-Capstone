from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update, func, and_
from app.models.view_log import ViewLog
from app.models.enums import FavoriteType
import datetime

MAX_VIEW_LOGS = 30

def add_or_update_view_log(db: Session, user_id: int, target_type: FavoriteType, target_id: int):
    # 기존에 동일 기록이 있는지 확인
    stmt = select(ViewLog).where(
        ViewLog.user_id == user_id,
        ViewLog.type == target_type,
        getattr(ViewLog, f"{target_type}_id") == target_id
    )
    existing_log = db.scalar(stmt)

    now = datetime.datetime.utcnow()

    if existing_log:
        existing_log.viewed_at = now
    else:
        log = ViewLog(
            user_id=user_id,
            type=target_type,
            viewed_at=now,
            **{f"{target_type}_id": target_id}
        )
        db.add(log)

    db.flush()
    db.commit()
    truncate_view_logs(db, user_id)


def truncate_view_logs(db: Session, user_id: int):
    subq = (
        select(ViewLog.id)
        .where(ViewLog.user_id == user_id)
        .order_by(ViewLog.viewed_at.desc())
        .offset(MAX_VIEW_LOGS)
    )
    old_ids = [row[0] for row in db.execute(subq).all()]
    if old_ids:
        db.execute(delete(ViewLog).where(ViewLog.id.in_(old_ids)))