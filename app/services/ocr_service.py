import os, uuid, shutil
from sqlalchemy.orm import Session
from fastapi import UploadFile
import pytesseract
from rapidfuzz import fuzz

from app.models import User
from app.crud.product import get_all_products_id_name
from app.crud.meal import make_suggested_products
from app.schemas.ocr import OCRProductResponse
from app.core.ocr_utils import preprocess_image, extract_known_allergens, match_user_allergens

async def analyze_product_from_ocr(product_name: str, image_file: UploadFile, db: Session, current_user: User) -> OCRProductResponse:
    # 이미지 저장
    temp_path = os.path.join("/tmp", f"ocr_{uuid.uuid4().hex}.jpg")
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(image_file.file, buffer)

    # 전처리 & OCR
    processed = preprocess_image(temp_path)
    text = pytesseract.image_to_string(processed, lang="kor", config="--psm 6")

    if not text.strip():
        raise ValueError("성분 정보를 인식할 수 없습니다.")

    # 알러지 추출 및 비교
    user_allergens = [a.name for a in current_user.allergen]
    extracted = extract_known_allergens(text)
    hit, safe = match_user_allergens(extracted, user_allergens)

    # 제품 추천 (유사도 기반)
    all_products = get_all_products_id_name(db)
    similarity_scores = [(p["id"], fuzz.ratio(product_name, p["name"])) for p in all_products]
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
