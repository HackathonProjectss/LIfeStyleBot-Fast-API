from fastapi import APIRouter
from api.handlers import user
from core.config import settings

router = APIRouter()
router.include_router(user.user_router, prefix=settings.API_V1_STR + "/users", tags=["users"])

