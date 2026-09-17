from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.files import router as files_router
from app.api.v1.shares import router as shares_router
from app.api.v1.admin import router as admin_router

api_v1_router = APIRouter()
api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(files_router)
api_v1_router.include_router(shares_router)
api_v1_router.include_router(admin_router)

__all__ = ["api_v1_router"]
