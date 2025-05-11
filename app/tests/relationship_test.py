from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.base import Base
from app.models.food import Food
from app.models.food_bundle import FoodBundle
from app.models.food_bundle_item import FoodBundleItem

# 📌 테스트용 SQLite 메모리 DB 사용 (실제 프로젝트에서는 settings.DATABASE_URL 사용)
engine = create_engine("sqlite:///:memory:", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    # 1. Food, Bundle 생성
    food = Food(name="Test Food", ingredient="salt,sugar", source_type="user", supplier_id=1)
    bundle = FoodBundle(name="Test Bundle", supplier_id=1)

    # 2. 관계 연결
    bundle.items.append(food)  # Many-to-Many via FoodBundleItem

    # 3. DB에 저장
    session.add_all([food, bundle])
    session.commit()

    # 4. 관계 확인
    fetched_bundle = session.query(FoodBundle).first()
    print(f"✔ Bundle name: {fetched_bundle.name}")
    for item in fetched_bundle.items:
        print(f" ↳ Contains food: {item.name}")

    fetched_food = session.query(Food).first()
    print(f"✔ Food name: {fetched_food.name}")
    for bundle in fetched_food.bundles:
        print(f" ↳ Belongs to bundle: {bundle.name}")
