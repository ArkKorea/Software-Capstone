import cv2
import numpy as np

KOREAN_ALLERGENS = [
    "난 류", "우 유", "메 밀", "땅 콩", "대 두", "밀", "고 등 어", "게",
    "새 우", "돼 지 고 기", "복 숭 아", "토 마 토", "아 황 산 염", "호 두", "닭 고 기",
    "소 고 기", "오 징 어", "조 개 류"
]

def preprocess_image(image_path: str):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (gray.shape[1] * 2, gray.shape[0] * 2), interpolation=cv2.INTER_LINEAR)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((1, 1), np.uint8)
    return cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

def extract_known_allergens(text: str):
    # OCR 결과와 알러지 목록 모두 공백 제거 후 비교
    clean_text = text.replace(" ", "")
    return [a for a in KOREAN_ALLERGENS if a.replace(" ", "") in clean_text]

# 사용자 알러지 비교 (공백 제거된 버전으로 비교)
def match_user_allergens(extracted: list, user_allergens: list):
    # 비교를 위해 양쪽 모두 공백 제거
    user_allergens_clean = [a.replace(" ", "") for a in user_allergens]
    extracted_clean = [a.replace(" ", "") for a in extracted]

    hit = [e for e in extracted_clean if e in user_allergens_clean]
    safe = [e for e in extracted_clean if e not in user_allergens_clean]
    return hit, safe