from fastapi import FastAPI
from app.api import auth, product, search


app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(product.router, prefix="/api/product", tags=["Product"])
app.include_router(favorite.router, prefix="/api/user", tags=["Favorites"])
app.include_router(search.router, prefix="/api", tags=["Search"])
