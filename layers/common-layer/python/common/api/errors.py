from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any, List
from aws_lambda_powertools import Logger

logger = Logger(service="error_handler")

class APIError(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        errors: Optional[List[Dict[str, str]]] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(status_code=status_code, detail=message, headers=headers)
        self.error_code = error_code
        self.errors = errors

class ValidationError(APIError):
    def __init__(self, message: str, errors: List[Dict[str, str]]):
        super().__init__(
            status_code=400,
            error_code="E2000",
            message=message,
            errors=errors
        )

class AuthenticationError(APIError):
    def __init__(self, message: str = "Token không hợp lệ hoặc đã hết hạn"):
        super().__init__(
            status_code=401,
            error_code="E1000",
            message=message
        )

class AuthorizationError(APIError):
    def __init__(self, message: str = "Không có quyền truy cập chức năng này"):
        super().__init__(
            status_code=403,
            error_code="E1002",
            message=message
        )

class NotFoundError(APIError):
    def __init__(self, message: str = "Không tìm thấy dữ liệu"):
        super().__init__(
            status_code=404,
            error_code="E3000",
            message=message
        )

class BusinessError(APIError):
    def __init__(self, message: str, error_code: str = "E4001"):
        super().__init__(
            status_code=400,
            error_code=error_code,
            message=message
        )

async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """
    Handle API errors and return standardized error response
    """
    error_response = {
        "status": "error",
        "code": exc.error_code,
        "message": exc.detail
    }
    
    if exc.errors:
        error_response["errors"] = exc.errors
        
    # Log error
    logger.error(f"API Error: {exc.error_code}", extra={
        "path": request.url.path,
        "method": request.method,
        "error_code": exc.error_code,
        "status_code": exc.status_code,
        "message": exc.detail
    })
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response,
        headers=exc.headers
    )

async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """
    Handle validation errors
    """
    return await api_error_handler(request, exc)

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle standard HTTP exceptions
    """
    error = APIError(
        status_code=exc.status_code,
        error_code="E6000",
        message=exc.detail,
        headers=exc.headers
    )
    return await api_error_handler(request, error)

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions
    """
    # Log unexpected error
    logger.exception("Unexpected error occurred", extra={
        "path": request.url.path,
        "method": request.method,
        "error": str(exc)
    })
    
    error = APIError(
        status_code=500,
        error_code="E6000",
        message="Lỗi hệ thống không xác định"
    )
    return await api_error_handler(request, error) 