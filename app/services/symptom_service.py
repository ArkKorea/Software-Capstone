from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.symptom import *
from app.models.user import User
from app.crud.symptom import *

def save_user_symptom(request: SymptomSaveRequest, db: Session, current_user: User) -> SymptomSaveResponse:
    insert_user_symptom(request, db, current_user.id)
    return SymptomSaveResponse(
        message="설문이 저장되었습니다."
    )

def get_user_symptom_by_date(request: SymptomByDateRequest, db: Session, current_user: User) -> SymptomByDateResponse:
    query = select_user_symptom(request.date, db, current_user.id)
    if query is None:
        raise HTTPException(status_code=404, detail="해당 날짜에 대한 증상 데이터가 없습니다.")
    return SymptomByDateResponse(
        skin=query.skin,
        stomach=query.stomach,
        breath=query.breath,
        headache=query.headache,
        fatigue=query.fatigue
    )
