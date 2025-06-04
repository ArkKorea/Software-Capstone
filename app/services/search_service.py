from app.schemas.search import (SearchRequest, Store, SearchStoreResponse, SearchProductResponse,
                                Bundle, StoreProductListRequest, StoreProductListResponse)
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud.search import *
from .detail_service import get_product_detail_service, get_bundle_detail_service
from app.models.user import User


def search_product(request: SearchRequest, db: Session, current_user: User) -> SearchProductResponse:
    result_product = get_product_by_keyword(request.query, db)
    result_bundle = get_bundle_by_keyword(request.query, db)
    return_value = SearchProductResponse(products=[], bundles=[])
    result_product = [get_product_detail_service(db, product.id, current_user) for product in result_product]
    if not result_bundle:
        return SearchProductResponse(products=result_product, bundles=[])
    return_value.products = result_product
    for bundle in result_bundle:
        bundle_allergen_hit = []
        bundle_allergen_safe = []

        user_allergen_ids = [allergen.id for allergen in current_user.allergen]
        for product in bundle.items:
            bundle_allergen_hit += [a.name for a in product.allergen if a.id in user_allergen_ids]
            bundle_allergen_safe += [a.name for a in product.allergen if a.id not in user_allergen_ids]

        bundle_allergen_hit = list(set(bundle_allergen_hit))
        bundle_allergen_safe = list(set(bundle_allergen_safe))
        
        return_value.bundles.append(Bundle(bundle_id=bundle.id, name=bundle.name, image_url=bundle.image_url or "",
                                           allergen_hit=bundle_allergen_hit, allergen_safe=bundle_allergen_safe,
                                           supplier_id=bundle.supplier.id, supplier_name=bundle.supplier.name))
    return return_value

def search_store(request: SearchRequest, db: Session) -> SearchStoreResponse:
    result = get_store_by_keyword(request.query, db)
    if not result:
        raise HTTPException(status_code=404, detail="해당 지점을 찾을 수 없습니다.")
    return SearchStoreResponse(
        stores=[Store(store_id=store.id,
                      name=store.name,
                      address=store.address or "") for store in result]
    )

def get_store_product_list(request: StoreProductListRequest, db: Session, current_user: User) -> StoreProductListResponse:
    store = get_store_by_id(request.store_id, db)
    if not store:
        raise HTTPException(status_code=404, detail="해당 지점을 찾을 수 없습니다.")
    
    products = store.foods
    return StoreProductListResponse(
        store=Store(store_id=store.id,
                    name=store.name or "",
                    address=store.address or ""),
        products=[get_product_detail_service(db, product.id, current_user) for product in products]
    )