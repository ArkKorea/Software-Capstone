from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Union
from app.db.database import get_db
from app.schemas.search import SearchRequest, StoreProductListRequest, StoreProductListResponse
from app.schemas.product import ProductResponse, BundleResponse
from app.services.search_service import *

router = APIRouter()

@router.post("/search", response_model=Union[ProductResponse, BundleResponse])
def search_function(request: SearchRequest, user_email: str, db: Session = Depends(get_db)):
    search_type = request.type
    if search_type == "product":
        return search_product(request, db, user_email)
    elif search_type == "store":
        return search_store(request, db)
    else:
        raise HTTPException(status_code=400,
                            detail="유효하지 않은 요청 타입입니다. 'product' 또는 'bundle'을 입력해주세요.")
    

@router.post("/store/products", response_model=StoreProductListResponse)
def search_store_product_list(request: StoreProductListRequest, user_email: str, db: Session = Depends(get_db)):
    return get_store_product_list(request, db, user_email)