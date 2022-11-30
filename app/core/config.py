import os
from functools import lru_cache

from pydantic import AnyHttpUrl, validator


class BaseConfig:
    # Core
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "prod")
    HTTPS_ON: bool = os.getenv("HTTPS_ON") in ["True", 1]
    DOMAIN: str = os.getenv("DOMAIN", "localhost")
    PORT: int = int(os.getenv("PORT", 8888))
    BASE_URL: str = f'{"https" if HTTPS_ON else "http"}://{DOMAIN}:{PORT}'
    DEBUG: bool = os.getenv("DEBUG") in ["True", "1"]
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI")
    ALLOWED_ORIGINS: list[AnyHttpUrl | str | None] = []
    TIMEZONE: str = os.getenv("TIMEZONE", "Europe/Warsaw")
    OPENAPI_URL: str | None = f"{API_PREFIX}/openapi.json"
    DOCS_URL: str | None = f"{API_PREFIX}/docs"

    # Database
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
    DATABASE_URL: str = (
        "postgresql+asyncpg://"
        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    )
    DB_POOL_SIZE: int = 83
    WEB_CONCURRENCY: int = 9
    POOL_SIZE: int = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


class TestingConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    OPENAPI_URL: str | None = None
    DOCS_URL: str | None = None


@lru_cache()
def get_settings() -> BaseConfig:
    config_cls_dict = {
        "dev": DevelopmentConfig,
        "prod": ProductionConfig,
        "test": TestingConfig,
    }
    config_cls = config_cls_dict[BaseConfig.ENVIRONMENT]
    return config_cls()


settings = get_settings()
