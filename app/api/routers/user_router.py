from fastapi import APIRouter
from app.api.endpoints.user.user_api import user_module
from app.api.endpoints.user.auth import auth_module
from app.api.endpoints.user.oauth2 import social_auth_module

user_router = APIRouter()

user_router.include_router(
    user_module,
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

user_router.include_router(
    auth_module,
    prefix="",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

user_router.include_router(
    social_auth_module,
    prefix="/social",
    tags=["social-auth"],
    responses={404: {"description": "Not found"}},
)

