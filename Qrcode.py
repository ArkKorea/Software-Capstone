import cv2
import numpy as np
from pyzbar.pyzbar import decode
import os
import tempfile
import uvicorn
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union, Literal
import uuid
from pathlib import Path

# 데이터베이스 관련 임포트
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import pymysql

# 데이터베이스 설정 (MySQL 사용) - 읽기 전용 접근
DATABASE_URL = ""
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 임시 디렉토리 생성
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

# 데이터베이스 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# QR 코드 유틸리티 클래스
class QRCodeUtils:
    @staticmethod
    def decode_image(image_data):
        """
        이미지에서 QR 코드/바코드 디코딩
        
        Args:
            image_data: CV2 이미지 데이터 또는 바이트 데이터
            
        Returns:
            list: 디코딩된 코드 정보 목록 또는 빈 리스트
        """
        try:
            # 바이트 데이터인 경우 이미지로 변환
            if isinstance(image_data, bytes):
                nparr = np.frombuffer(image_data, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            else:
                image = image_data
                
            if image is None:
                return []
                
            # QR 코드/바코드 디코딩
            decoded_objects = decode(image)
            
            results = []
            for obj in decoded_objects:
                try:
                    code_data = obj.data.decode('utf-8')
                    code_type = "qrcode" if obj.type == "QRCODE" else "barcode"
                    
                    # 결과 추가
                    results.append({
                        "type": code_type,
                        "value": code_data,
                        "rect": {
                            "x": obj.rect.left,
                            "y": obj.rect.top,
                            "width": obj.rect.width,
                            "height": obj.rect.height
                        }
                    })
                except Exception:
                    continue
                    
            return results
            
        except Exception as e:
            print(f"이미지 디코딩 중 오류: {e}")
            return []

# 임시 파일 정리 함수
def cleanup_temp_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"임시 파일 정리 중 오류: {e}")

# FastAPI 앱 생성
app = FastAPI(
    title="식품 알레르기 관리 API",
    description="QR 코드를 통한 식품 알레르기 정보 관리 API",
    version="1.0.0"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시에는 구체적인 도메인 지정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 모델 정의
class ProductCodeRequest(BaseModel):
    type: Literal["barcode", "qrcode"]
    value: str

class ProductResponse(BaseModel):
    product_id: str
    name: str
    image_url: Optional[str] = None
    allergens_hit: List[str] = []
    allergens_safe: List[str] = []
    ingredients_text: Optional[str] = None
    is_favorite: bool = False
    supplier_id: str
    supplier_name: str

class ProductsResponse(BaseModel):
    products: List[ProductResponse] = []

class ErrorResponse(BaseModel):
    error: str
    code: str

# API 엔드포인트
@app.post("/api/scan")
async def scan_image(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """이미지에서 QR 코드/바코드 스캔 API"""
    try:
        # 파일 확장자 확인
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in valid_extensions:
            raise HTTPException(status_code=400, detail="지원되지 않는 이미지 형식")
        
        # 이미지 데이터 읽기
        content = await file.read()
        
        # 임시 파일로 저장 (메모리에서 처리하기 어려운 대용량 이미지를 위함)
        temp_file = os.path.join(TEMP_DIR, f"{uuid.uuid4()}{file_ext}")
        with open(temp_file, "wb") as f:
            f.write(content)
        
        # 배경 작업으로 임시 파일 정리 추가
        if background_tasks:
            background_tasks.add_task(cleanup_temp_file, temp_file)
        
        # 이미지 읽기
        image = cv2.imread(temp_file)
        if image is None:
            raise HTTPException(status_code=400, detail="이미지 읽기 실패")
        
        # QR 코드/바코드 스캔
        results = QRCodeUtils.decode_image(image)
        
        # 응답 생성
        return {"results": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 스캔 실패: {str(e)}")

@app.post("/api/product/from-code", response_model=Union[ProductsResponse, ErrorResponse])
async def get_product_from_code(
    request: ProductCodeRequest,
    user_id: int = Query(..., description="사용자 ID"),
    db: Session = Depends(get_db)
):
    """코드 기반 상품 조회 API"""
    try:
        # 코드 타입 검증
        if request.type not in ["barcode", "qrcode"]:
            return JSONResponse(
                status_code=400, 
                content={
                    "error": "유효하지 않은 요청 타입입니다. 'barcode' 또는 'qrcode'를 입력해주세요.",
                    "code": "INVALID_CODE_TYPE"
                }
            )
        
        # SQL 쿼리 실행 - 사용자 알레르기 정보 조회
        query_user_allergens = """
        SELECT a.id, a.name 
        FROM allergens a
        JOIN user_allergies ua ON a.id = ua.allergen_id
        WHERE ua.user_id = :user_id
        """
        
        # 사용자 알레르기 정보 가져오기
        result_allergens = db.execute(query_user_allergens, {"user_id": user_id})
        user_allergens = [{"id": row.id, "name": row.name} for row in result_allergens]
        user_allergen_ids = [allergen["id"] for allergen in user_allergens]
        
        # SQL 쿼리 실행 - 상품 조회
        query_product = """
        SELECT p.id, p.product_id, p.name, p.description, p.image_url, p.ingredients_text, 
               s.id as supplier_id, s.supplier_id as supplier_external_id, s.name as supplier_name
        FROM products p
        JOIN product_codes pc ON p.id = pc.product_id
        JOIN suppliers s ON p.supplier_id = s.id
        WHERE pc.code_type = :code_type AND pc.code_value = :code_value
        """
        
        # 상품 정보 가져오기
        result_products = db.execute(query_product, {
            "code_type": request.type,
            "code_value": request.value
        })
        
        products_data = []
        for row in result_products:
            # 상품 알레르겐 조회
            query_allergens = """
            SELECT a.id, a.name
            FROM allergens a
            JOIN product_allergens pa ON a.id = pa.allergen_id
            WHERE pa.product_id = :product_id
            """
            
            result_product_allergens = db.execute(query_allergens, {"product_id": row.id})
            product_allergens = [{"id": r.id, "name": r.name} for r in result_product_allergens]
            
            # 알레르기 비교
            allergens_hit = []
            allergens_safe = []
            
            for allergen in product_allergens:
                if allergen["id"] in user_allergen_ids:
                    allergens_hit.append(allergen["name"])
                else:
                    allergens_safe.append(allergen["name"])
            
            # 즐겨찾기 여부 확인
            query_favorite = """
            SELECT id FROM user_favorites
            WHERE user_id = :user_id AND product_id = :product_id
            LIMIT 1
            """
            
            result_favorite = db.execute(query_favorite, {
                "user_id": user_id,
                "product_id": row.id
            }).fetchone()
            
            is_favorite = result_favorite is not None
            
            # 상품 정보 구성
            product_info = {
                "product_id": row.product_id,
                "name": row.name,
                "image_url": row.image_url,
                "allergens_hit": allergens_hit,
                "allergens_safe": allergens_safe,
                "ingredients_text": row.ingredients_text,
                "is_favorite": is_favorite,
                "supplier_id": row.supplier_external_id,
                "supplier_name": row.supplier_name
            }
            
            products_data.append(product_info)
        
        if not products_data:
            return JSONResponse(
                status_code=404, 
                content={
                    "error": "등록된 상품이 없습니다.",
                    "code": "PRODUCT_NOT_FOUND"
                }
            )
        
        return ProductsResponse(products=products_data)
        
    except Exception as e:
        print(f"상품 조회 중 오류: {e}")
        return JSONResponse(
            status_code=500, 
            content={
                "error": "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
                "code": "INTERNAL_SERVER_ERROR"
            }
        )

@app.get("/")
async def read_root():
    return {"message": "식품 알레르기 관리 API 서버가 실행 중입니다. API 문서는 /docs에서 확인하세요."}

# 서버 시작 함수
def start_server(host="0.0.0.0", port=8000):
    """API 서버 시작"""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    # 서버 시작
    start_server()
