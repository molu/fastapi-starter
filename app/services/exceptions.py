from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException


class BadRequestException(HTTPException):
    def __init__(self, msg: str = "Bad Request"):
        self.msg = msg
        self.status_code = status.HTTP_400_BAD_REQUEST


class UnauthorizedException(HTTPException):
    def __init__(self, msg: str = "Unauthorized", headers: dict = {}):
        self.msg = msg
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.headers = headers


class ForbiddenException(HTTPException):
    def __init__(self, msg: str = "Forbidden"):
        self.msg = msg
        self.status_code = status.HTTP_403_FORBIDDEN


class ConflictException(HTTPException):
    def __init__(self, msg: str = "Conflict"):
        self.msg = msg
        self.status_code = status.HTTP_409_CONFLICT


class NotFoundException(HTTPException):
    def __init__(self, msg: str = "Not Found"):
        self.msg = msg
        self.status_code = status.HTTP_404_NOT_FOUND


class InternalServerErrorException(HTTPException):
    def __init__(self, msg: str = "Internal Server Error"):
        self.msg = msg
        self.status_code = status.HTTP_404_NOT_FOUND


async def bad_request_exception_handler(
    request: Request, exc: BadRequestException
) -> JSONResponse:
    return JSONResponse(
        content={"msg": exc.msg},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


async def unauthorized_exception_handler(
    request: Request, exc: UnauthorizedException
) -> JSONResponse:
    return JSONResponse(
        content={"msg": exc.msg},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


async def forbidden_exception_handler(
    request: Request, exc: ForbiddenException
) -> JSONResponse:
    return JSONResponse(
        content={"msg": exc.msg},
        status_code=status.HTTP_403_FORBIDDEN,
    )


async def not_found_exception_handler(
    request: Request, exc: NotFoundException
) -> JSONResponse:
    return JSONResponse(
        content={"msg": exc.msg},
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def conflict_exception_handler(
    request: Request, exc: ConflictException
) -> JSONResponse:
    return JSONResponse(
        content={"msg": exc.msg},
        status_code=status.HTTP_409_CONFLICT,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = exc.errors()
    response: dict = {"msg": []}
    for error in errors:
        msg = {error["loc"][-1]: error["msg"]}
        response["msg"].append(msg)
    return JSONResponse(
        response,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def internal_server_error_handler(
    request: Request, exc: InternalServerErrorException
) -> JSONResponse:
    return JSONResponse(
        content={"msg": exc.msg},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


exception_handlers = {
    BadRequestException: bad_request_exception_handler,
    UnauthorizedException: unauthorized_exception_handler,
    ForbiddenException: forbidden_exception_handler,
    NotFoundException: not_found_exception_handler,
    ConflictException: conflict_exception_handler,
    RequestValidationError: validation_exception_handler,
    InternalServerErrorException: internal_server_error_handler,
}
