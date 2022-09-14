import os
import secrets
from functools import lru_cache

from pydantic import AnyHttpUrl, validator


class BaseConfig:
    # Core
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "prod")
    DEBUG: bool = os.getenv("DEBUG", False) in ["True", "1"]
    API_STR: str = "/api"
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI")
    HTTPS_ON: bool = os.getenv("HTTPS_ON") in ["True", 1]
    AUTH_NAME: str = os.getenv("AUTH_NAME", "X-API-KEY")
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ALLOWED_ORIGINS: list[AnyHttpUrl | str | None] = []

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


@lru_cache()
def get_settings() -> BaseConfig:
    config_cls_dict = {
        "dev": DevelopmentConfig,
        "prod": ProductionConfig,
        "test": TestingConfig,
    }
    environment = os.getenv("ENVIRONMENT", "prod")
    config_cls = config_cls_dict[environment]
    return config_cls()


settings = get_settings()
