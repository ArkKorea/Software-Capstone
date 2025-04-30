import os
import uuid
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import pytesseract
import cv2
import numpy as np

# FastAPI 인스턴스 생성
app = FastAPI()


# 알러지 성분 목록 (18종)
KOREAN_ALLERGENS = [
    "난 류", "우 유", "메 밀", "땅 콩", "대 두", "밀", "고 등 어", "게",
    "새 우", "돼 지 고 기", "복 숭 아", "토 마 토", "아 황 산 염", "호 두", "닭 고 기",
    "소 고 기", "오 징 어", "조 개 류"
]


# 사용자 알러지 예시
USER_ALLERGENS = ["우 유", "대 두", "복 숭 아"]


# 이미지 전처리 함수 (OpenCV 사용)
def preprocess_image(image_path: str):
    img = cv2.imread(image_path)

    # 1. 그레이스케일 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. 크기 확대 (2배)
    gray = cv2.resize(gray, (gray.shape[1] * 2, gray.shape[0] * 2), interpolation=cv2.INTER_LINEAR)

    # 3. 블러 적용
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # 4. Otsu 이진화
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 5. 형태학적 연산으로 노이즈 제거 (약한 커널 사용)
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    return processed


# OCR 결과에서 알러지 성분 추출 함수
def extract_known_allergens(text: str):
    return [a for a in KOREAN_ALLERGENS if a in text]


# 사용자 알러지와 비교 함수
def match_user_allergens(extracted):
    hit = [a for a in extracted if a in USER_ALLERGENS]  # 사용자 알러지에 해당하는 항목
    safe = [a for a in extracted if a not in USER_ALLERGENS]  # 문제 없는 성분
    return hit, safe


# OCR 처리 및 제품 분석 API 엔드포인트
@app.post("/api/product/from-ocr")
async def from_ocr(product_name: str = Form(...), image_file: UploadFile = File(...)):
    try:
        # 이미지 저장
        temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
        temp_path = os.path.join("/tmp", temp_filename)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)

        # 이미지 전처리 및 OCR 실행
        processed = preprocess_image(temp_path)
        text = pytesseract.image_to_string(processed, lang="kor", config="--psm 6")
        
        if not text.strip():
            return JSONResponse(status_code=422, content={
                "error": "성분 정보를 인식할 수 없습니다."
            })

        # 알러지 성분 추출 및 비교
        extracted = extract_known_allergens(text)
        hit, safe = match_user_allergens(extracted)

        # 결과 구성
        result = {
            "product": {
                "product_id": "temp_001",
                "name": product_name,
                "image_url": None,
                "allergens_hit": hit,
                "allergens_safe": safe,
                "ingredients_text": text.strip()
            },
            "suggested_products": []
        }

        # 결과 반환
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            "detail": str(e)
        })
