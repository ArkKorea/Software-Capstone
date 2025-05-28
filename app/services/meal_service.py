from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from rapidfuzz.fuzz import ratio
from app.schemas.meal import *
from app.models.user import User
from app.crud.meal import *
from app.crud.product import get_product_by_id, get_product_by_name, get_all_products_id_name
from datetime import datetime

TOP_N = 3

def create_intake_log(request: CreateMealRequest, db: Session, user: User)  -> CreateMealResponse:
    if not isinstance(request.datetime, datetime):
        raise HTTPException(status_code=400, detail="시간 형식이 올바르지 않습니다.")
    
    food = get_product_by_name(request.food_name, db)

    if food:
        log = insert_intake_log(request, db, user.id, food.id)
        return CreateMealResponse(
            record_id = log["log_id"],
            suggested_products= []
        )
    else:
        log = insert_intake_log(request, db, user.id)
        foods = get_all_products_id_name(db)

        similar_score = [(food_id, ratio(log["food_name"], food_name) /100) for food_id, food_name in foods]
        similar_score.sort(key=lambda x: x[1], reverse=True)
        similar_score = similar_score[:TOP_N]

        return CreateMealResponse(
            record_id = log["log_id"],
            suggested_products= make_suggested_products(similar_score, db)
        )

def connect_intake_log(request: ConnectMealRequest, db: Session, current_user: User) -> ConnectMealResponse:
    update_intake_log(request, db, current_user.id)
    return ConnectMealResponse(
        message= "상품 연동이 완료되었습니다."
    )

def query_intake_log(request: QueryMealRequest, db: Session, current_user: User) -> QueryMealResponse:
    logs = select_intake_log(request.date, db, current_user.id)
    if not logs:
        raise HTTPException(status_code=404, detail="해당 날짜에 기록된 식사가 없습니다.")
    meals = []
    for log in logs:
        matched_product = get_product_by_id(log.food_id, db)
        meals.append(Meal(
            datetime=log.created_at,
            food_name=log.food_name,
            matched_product=MatchedProduct(
                product_id=matched_product.id,
                name=matched_product.name,
                image_url=matched_product.image_url or "",
                supplier_id=matched_product.supplier_id,
                supplier_name=matched_product.supplier.name) if matched_product else None,
            quantity=log.quantity,
            memo=log.memo
        ))

    return QueryMealResponse(
        meals=meals
    )