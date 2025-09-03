from typing import Any, Optional
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK


def response_helper(
    success: bool,
    data: Optional[Any] = None,
    message: str = "",
    error: str = "",
    status_code=HTTP_200_OK,
) -> JSONResponse:
    return JSONResponse(
        content={
            "success": success,
            "data": data,
            "message": message,
            "error": error,
        },
        status_code=status_code,
    )
