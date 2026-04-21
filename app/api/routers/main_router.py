from fastapi import APIRouter
from app.api.routers.user_router import user_router

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Welcome to FastAPI Production Boilerplate!"}

router.include_router(user_router)


