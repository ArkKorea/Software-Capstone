from fastapi import APIRouter, Depends, HTTPException
from typing import Union
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.db.database import get_db
from app.schemas.search import SearchRequest, StoreProductListRequest, StoreProductListResponse
from app.services.search_service import *

router = APIRouter()

@router.post("/search", response_model=Union[SearchProductResponse, SearchStoreResponse])
def search_function(request: SearchRequest,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    search_type = request.type
    if search_type == "product":
        return search_product(request, db, current_user)
    elif search_type == "store":
        return search_store(request, db)
    else:
        raise HTTPException(status_code=400,
                            detail="유효하지 않은 요청 타입입니다. 'product' 또는 'store'을 입력해주세요.")
    

@router.post("/store/products", response_model=StoreProductListResponse)
def search_store_product_list(request: StoreProductListRequest,
                              db: Session = Depends(get_db),
                              current_user: User = Depends(get_current_user)):
    return get_store_product_list(request, db, current_user)