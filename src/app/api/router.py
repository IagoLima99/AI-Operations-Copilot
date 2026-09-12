"""Compose the application's API routers."""

from fastapi import APIRouter

from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["Health"])
router.include_router(chat_router, prefix="/chat", tags=["Chat"])
