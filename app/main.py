from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.v1.router import api_router
from app.core.config import settings


def create_application() -> FastAPI:
    application = FastAPI(
        debug=settings.DEBUG,
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=f"{settings.API_PREFIX}/docs",
    )
    application.include_router(api_router, prefix=settings.API_PREFIX)
    application.add_middleware(TrustedHostMiddleware, allowed_hosts=[settings.DOMAIN])
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
