from app.models.intake_log import IntakeLog
from app.models.food import Food
from sqlalchemy.orm import Session
from app.schemas.meal import *
from typing import List, Tuple
from datetime import datetime, timedelta, date

def insert_intake_log(request: CreateMealRequest, db: Session, user_id: int, food_id: int = None) -> dict:
    if not request.food_name or not request.food_name or not request.datetime or not request.quantity:
        raise ValueError("입력값이 부족합니다.")
    log = IntakeLog(
        user_id=user_id,
        food_name=request.food_name,
        food_id=food_id,
        quantity=request.quantity,
        memo=request.memo,
        created_at=request.datetime,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return {"log_id": log.id, "food_name": log.food_name}

def make_suggested_products(data: List[Tuple[int, float]], db: Session) -> List[SuggestedProduct]:
    food_ids = [food_id for food_id, _ in data]
    foods_in_db = db.query(Food).filter(Food.id.in_(food_ids)).all()
    food_map = {food.id: food for food in foods_in_db}
    foods = []

    for food_id, score in data:
        food = food_map.get(food_id)
        foods.append(SuggestedProduct(
            product_id=food.id,
            name=food.name,
            image_url=food.image_url or "",
            match_score=score
        ))
    return foods

def update_intake_log(request: ConnectMealRequest, db: Session, user_id: int):
    if not request.record_id:
        raise ValueError("기록 ID가 전달되지 않았습니다.")
    elif not request.matched_product_id:
        raise ValueError("상품을 찾을 수 없습니다.")
    record = db.query(IntakeLog).filter(IntakeLog.id == request.record_id).first()
    if record.user_id != user_id:
        raise ValueError("해당 기록에 접근할 수 없습니다.")
    record.food_id = request.matched_product_id
    db.commit()

def select_intake_log(day: date, db: Session, user_id: int):
    
    start = datetime.combine(day, datetime.min.time())
    end = start + timedelta(days=1)

    return db.query(IntakeLog).filter(
        IntakeLog.user_id == user_id,
        IntakeLog.created_at >= start,
        IntakeLog.created_at < end
    ).all()