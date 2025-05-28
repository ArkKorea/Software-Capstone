from sqlalchemy.orm import Session
from app.models.allergen import Allergen
from app.models.user import User

def get_allergies_by_user_id(user_id: int, db: Session):
    return db.query(Allergen).filter(Allergen.user.any(User.id== user_id)).all()

def save_allergies_by_user_id(user: User, allergies: list[str], db: Session):
    allergen_odjs = db.query(Allergen).filter(Allergen.name.in_(allergies)).all()
    user.allergen = allergen_odjs
    db.commit()
