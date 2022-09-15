from fastapi import APIRouter

from app.api.v1.endpoints.health_check import router as health_check_router
from app.api.v1.endpoints.item import router as item_router

api_router = APIRouter()
api_router.include_router(health_check_router, tags=["health_check"])
api_router.include_router(item_router, tags=["item"])
