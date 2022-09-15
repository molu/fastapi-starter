import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.config import settings


def get_logger() -> logging.Logger:
    logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
    logger = logging.getLogger(settings.PROJECT_NAME)
    return logger


def get_now() -> datetime:
    return datetime.now(tz=ZoneInfo(settings.TIMEZONE))
