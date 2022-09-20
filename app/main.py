from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.services.exceptions import exception_handlers
from app.services.utils import get_logger

logger = get_logger()


def create_application() -> FastAPI:
    application = FastAPI(
        debug=settings.DEBUG,
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=f"{settings.API_PREFIX}/docs",
        exception_handlers=exception_handlers,
    )

    # Include application routes
    application.include_router(api_router, prefix=settings.API_PREFIX)

    # Allow only current domain as HTTP `Host` header - prevent Host header attacks
    application.add_middleware(TrustedHostMiddleware, allowed_hosts=[settings.DOMAIN])

    # CORS middleware - origins allowed to make requests to the application
    if settings.ALLOWED_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.ALLOWED_ORIGINS],
            allow_credentials=True,
            allow_methods=["OPTIONS", "POST", "GET", "PUT", "PATCH", "DELETE"],
            allow_headers=["*"],
        )

    # Turn on HTTPS redirection
    if settings.HTTPS_ON:
        application.add_middleware(HTTPSRedirectMiddleware)

    return application


app = create_application()


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Application starting up...")


@app.on_event("shutdown")
async def on_shutdown() -> None:
    logger.info("Application shutting down...")
