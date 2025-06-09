import os, uuid, shutil, base64
from sqlalchemy.orm import Session
from fastapi import HTTPException
import pytesseract
from rapidfuzz import fuzz
from app.models import User
from app.crud.product import get_all_products_id_name
from app.crud.meal import make_suggested_products
from app.schemas.ocr import OCRProductResponse
from app.core.ocr_utils import preprocess_image, extract_known_allergens, match_user_allergens

def analyze_product_from_base64(product_name: str, image_base64: str, db: Session, current_user: User) -> OCRProductResponse:
    # base64 → 이미지 파일 저장
    try:
        image_data = base64.b64decode(image_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="이미지 디코딩 실패")

    temp_path = os.path.join(os.getcwd(), f"ocr_{uuid.uuid4().hex}.jpg")
    try:
        with open(temp_path, "wb") as f:
            f.write(image_data)

        # 전처리 및 OCR
        processed = preprocess_image(temp_path)
        text = pytesseract.image_to_string(processed, lang="kor", config="--psm 6")

        if not text.strip():
            raise ValueError("성분 정보를 인식할 수 없습니다.")

        # 알러지 비교
        user_allergens = [a.name for a in current_user.allergen]
        extracted = extract_known_allergens(text)
        hit, safe = match_user_allergens(extracted, user_allergens)

        # 유사 제품 추천
        all_products = get_all_products_id_name(db)
        similarity_scores = [(p[0], fuzz.ratio(product_name, p[1])) for p in all_products]
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        top_matches = similarity_scores[:3]
        suggested_products = make_suggested_products(top_matches, db)

        return OCRProductResponse(
            product_id=-1,
            name=product_name,
            image_url=None,
            allergen_hit=hit,
            allergen_safe=safe,
            ingredient=text.strip(),
            supplier_id=-1,
            created_at=None,
            suggested_products=suggested_products
        )

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
