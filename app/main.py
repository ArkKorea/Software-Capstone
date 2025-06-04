from fastapi import FastAPI
from app.api import allergen, auth, product, search, favorite, symptom, meal, detail, bundle, route_to_app, api_ocr


import app.models
from app.models.base import Base

app = FastAPI()

print(list(Base.registry._class_registry.keys()))

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(product.router, prefix="/api/product", tags=["Product"])
app.include_router(favorite.router, prefix="/api/user", tags=["Favorites"])
app.include_router(search.router, prefix="/api", tags=["Search"])
app.include_router(allergen.router, prefix="/api/user/allergies", tags=["Allergies"])
app.include_router(symptom.router, prefix="/api/user/symptoms", tags=["Symptoms"])
app.include_router(meal.router, prefix="/api/user/meals", tags=["Meals"])
app.include_router(detail.router, prefix="/api/details", tags=["Details"])
app.include_router(bundle.router, prefix="/api/bundles", tags=["Bundles"])
app.include_router(route_to_app.router, prefix="", tags=["Route_to_app"])
app.include_router(bundle.router, prefix="/api", tags=["Ocr"])
