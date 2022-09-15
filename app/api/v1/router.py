from fastapi import APIRouter
from app.api.v1.endpoints.health_check import router as health_check_router


api_router = APIRouter()
api_router.include_router(health_check_router, tags=["health_check"])
