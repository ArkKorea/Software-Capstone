from app.models.symptom import SymptomsLog
from app.schemas.symptom import *
from sqlalchemy.orm import Session
from datetime import date

def insert_user_symptom(request: SymptomSaveRequest, db: Session, current_user_id: int):
    if request.date is None or request.skin is None or request.stomach is None or request.breath is None or request.headache is None or request.fatigue is None:
        raise ValueError("설문 데이터가 누락되었습니다.")
    elif not (1 <= request.skin <= 5 and 1 <= request.stomach <= 5 and 1 <= request.breath <= 5 and 1 <= request.headache <= 5 and 1 <= request.fatigue <= 5):
        raise ValueError("설문 데이터는 1~5까지의 정수여야 합니다.")
    
    symptom = SymptomsLog(
        user_id=current_user_id,
        skin=request.skin,
        stomach=request.stomach,
        breath=request.breath,
        headache=request.headache,
        fatigue=request.fatigue,
        log_time=request.date
    )
    db.add(symptom)
    db.commit()
    db.refresh(symptom)
    return symptom

def select_user_symptom(date: date, db: Session, user_id: int):
    return db.query(SymptomsLog).filter(SymptomsLog.user_id == user_id, SymptomsLog.log_time == date).first()