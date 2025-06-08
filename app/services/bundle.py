from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import delete
from app.models.food_bundle import FoodBundle
from app.models.food_bundle_item import FoodBundleItem
from app.models.food import Food
from app.models.user import User
from app.schemas.food_bundle import BundleCreate, BundleListResponse, BundleListItem, BundleUpdate, BundleDelete
from app.services.product_service import save_image_from_base64
import datetime

def create_bundle_service(db: Session, data: BundleCreate, user: User):
    # if user.role != "supplier" or not user.supplier_id:
    #     raise HTTPException(status_code=403, detail="번들 생성 권한이 없습니다.")

    # 이미지 저장
    image_url = save_image_from_base64(data.image_base64) if data.image_base64 else ""

    # 번들 생성
    new_bundle = FoodBundle(
        name=data.name,
        image_url=image_url,
        supplier_id=user.supplier_id,
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_bundle)
    db.flush()  # id 확보

    # food 구성 연결
    for food_id in data.product_ids:
        db.add(FoodBundleItem(bundle_id=new_bundle.id, food_id=food_id))

    db.commit()
    return {"message": "번들이 성공적으로 생성되었습니다."}

# 내 번들 조회
def get_my_bundles_service(db: Session, user: User) -> BundleListResponse:
    # if user.role != "supplier" or not user.supplier_id:
    #     raise HTTPException(status_code=403, detail="조회 권한이 없습니다.")

    bundles = db.query(FoodBundle).filter(FoodBundle.supplier_id == user.supplier_id).all()

    return BundleListResponse(
        bundles=[
            BundleListItem(
                id=b.id,
                name=b.name,
                image_url=b.image_url or ""
            ) for b in bundles
        ]
    )

# 내 번들 수정
def update_bundle_service(db: Session, data: BundleUpdate, user: User):
    # if user.role != "supplier" or not user.supplier_id:
    #     raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")

    bundle = db.query(FoodBundle).filter(
        FoodBundle.id == data.bundle_id,
        FoodBundle.supplier_id == user.supplier_id
    ).first()

    if not bundle:
        raise HTTPException(status_code=404, detail="해당 번들을 찾을 수 없습니다.")

    if data.name:
        bundle.name = data.name
    if data.image_base64:
        bundle.image_url = save_image_from_base64(data.image_base64)

    if data.product_ids is not None:
        # 기존 구성 제거 후 다시 등록
        db.execute(delete(FoodBundleItem).where(FoodBundleItem.bundle_id == bundle.id))
        for food_id in data.product_ids:
            db.add(FoodBundleItem(bundle_id=bundle.id, food_id=food_id))

    db.commit()
    return {"message": "번들이 성공적으로 수정되었습니다."}

# 번들 삭제
def delete_bundle_service(db: Session, data: BundleDelete, user: User):
    # if user.role != "supplier" or not user.supplier_id:
    #     raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")

    bundle = db.query(FoodBundle).filter(
        FoodBundle.id == data.bundle_id,
        FoodBundle.supplier_id == user.supplier_id
    ).first()

    if not bundle:
        raise HTTPException(status_code=404, detail="해당 번들을 찾을 수 없습니다.")

    db.delete(bundle)
    db.commit()

    return {"message": "번들이 성공적으로 삭제되었습니다."}