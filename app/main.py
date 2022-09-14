from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from app.api.v1.router import api_router
from app.core.config import settings


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)
    application.include_router(api_router, prefix=settings.API_STR)

    if settings.ALLOWED_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.ALLOWED_ORIGINS],
            allow_credentials=True,
            allow_methods=["OPTIONS", "POST", "GET", "PUT", "PATCH", "DELETE"],
            allow_headers=["*"],
        )
    if settings.HTTPS_ON:
        application.add_middleware(HTTPSRedirectMiddleware)
    return application


app = create_application()


@app.on_event("startup")
async def on_startup() -> None:
    pass


@app.on_event("shutdown")
async def on_shutdown() -> None:
    pass
