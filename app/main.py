from fastapi import FastAPI
from app.api import allergen, auth, product, search, favorite

import app.models
from app.models.base import Base

app = FastAPI()

print(list(Base.registry._class_registry.keys()))

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(product.router, prefix="/api/product", tags=["Product"])
app.include_router(favorite.router, prefix="/api/user", tags=["Favorites"])
app.include_router(search.router, prefix="/api", tags=["Search"])
app.include_router(allergen.router, prefix="/api/user/allergies", tags=["Allergies"])

