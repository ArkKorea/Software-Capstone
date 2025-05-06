from app.schemas.search import SearchRequest, Store, SearchStoreResponse, SearchProductResponse, Bundle, StoreProductListRequest, StoreProductListResponse
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud.search import *
from app.crud.user import get_user_by_email
from app.services.product_service import build_product_response

def search_product(request: SearchRequest, db: Session, user_email: str) -> SearchProductResponse:
    result_product = get_product_by_keyword(request.query, db)
    result_bundle = get_bundle_by_keyword(request.query, db)
    return_value = SearchProductResponse()
    result_product = [build_product_response(product, user_email, db) for product in result_product]
    return_value.products = result_product
    user = get_user_by_email(db, user_email)
    for bundle in result_bundle:
        bundle_allergen_hit = []
        bundle_allergen_safe = []

        for product in bundle.food:
            bundle_allergen_hit += [a.name for a in product.allergen if a.id in user.allergen]
            bundle_allergen_safe += [a.name for a in product.allergen if a.id not in user.allergen]
        
        list(set(bundle_allergen_hit))
        list(set(bundle_allergen_safe))
        
        return_value.bundles.append(Bundle(bundle_id=bundle.id, name=bundle.name, image_url=bundle.image_url,
                                           allergen_hit=bundle_allergen_hit, allergen_safe=bundle_allergen_safe,
                                           supplier_id=bundle.supplier.id, supplier_name=bundle.supplier.name))
    return return_value

def search_store(request: SearchRequest, db: Session) -> SearchStoreResponse:
    result = get_store_by_keyword(request.query, db)
    if not result:
        raise HTTPException(status_code=404, detail="해당 지점을 찾을 수 없습니다.")
    return SearchStoreResponse(
        stores=[Store(store_id=store.id, name=store.name, address=store.address) for store in result]
    )

def get_store_product_list(request: StoreProductListRequest, db: Session, user_email: str) -> StoreProductListResponse:
    store = get_store_by_id(request.store_id, db)
    if not store:
        raise HTTPException(status_code=404, detail="해당 지점을 찾을 수 없습니다.")
    
    products = store.foods
    return StoreProductListResponse(
        store=Store(store_id=store.id, name=store.name, address=store.address),
        products=[build_product_response(product, user_email, db) for product in products]
    )