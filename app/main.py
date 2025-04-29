from fastapi import FastAPI
from app.api import auth, favorite


app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

app.include_router(favorite.router, prefix="/api/user", tags=["Favorites"])
