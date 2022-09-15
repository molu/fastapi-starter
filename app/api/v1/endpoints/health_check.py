from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health-check", status_code=status.HTTP_200_OK)
async def health_check() -> JSONResponse:
    return JSONResponse({"status": "OK!"})
