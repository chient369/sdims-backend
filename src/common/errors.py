"""
Custom exceptions and error handling for SDIMS backend.
"""
from typing import Any, Dict, Optional, Union, List
import json
from aws_lambda_powertools import Logger

logger = Logger(service="error-handler")

class SDIMSError(Exception):
    """Base exception class for SDIMS errors."""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = 500, 
        error_code: str = "INTERNAL_ERROR"
    ):
        """
        Initialize SDIMS error.
        
        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Internal error code
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


class BadRequestError(SDIMSError):
    """Exception for bad request errors."""
    
    def __init__(self, message: str, error_code: str = "BAD_REQUEST"):
        """
        Initialize bad request error.
        
        Args:
            message: Error message
            error_code: Internal error code
        """
        super().__init__(message, 400, error_code)


class UnauthorizedError(SDIMSError):
    """Exception for unauthorized errors."""
    
    def __init__(self, message: str = "Unauthorized", error_code: str = "UNAUTHORIZED"):
        """
        Initialize unauthorized error.
        
        Args:
            message: Error message
            error_code: Internal error code
        """
        super().__init__(message, 401, error_code)


class ForbiddenError(SDIMSError):
    """Exception for forbidden errors."""
    
    def __init__(self, message: str = "Forbidden", error_code: str = "FORBIDDEN"):
        """
        Initialize forbidden error.
        
        Args:
            message: Error message
            error_code: Internal error code
        """
        super().__init__(message, 403, error_code)


class NotFoundError(SDIMSError):
    """Exception for not found errors."""
    
    def __init__(self, message: str = "Resource not found", error_code: str = "NOT_FOUND"):
        """
        Initialize not found error.
        
        Args:
            message: Error message
            error_code: Internal error code
        """
        super().__init__(message, 404, error_code)


class ConflictError(SDIMSError):
    """Exception for conflict errors."""
    
    def __init__(self, message: str, error_code: str = "CONFLICT"):
        """
        Initialize conflict error.
        
        Args:
            message: Error message
            error_code: Internal error code
        """
        super().__init__(message, 409, error_code)


class ValidationError(BadRequestError):
    """Exception for validation errors."""
    
    def __init__(
        self, 
        message: str = "Validation error", 
        error_code: str = "VALIDATION_ERROR",
        details: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Initialize validation error.
        
        Args:
            message: Error message
            error_code: Internal error code
            details: Detailed validation errors
        """
        super().__init__(message, error_code)
        self.details = details


class DatabaseError(SDIMSError):
    """Exception for database errors."""
    
    def __init__(self, message: str, error_code: str = "DATABASE_ERROR"):
        """
        Initialize database error.
        
        Args:
            message: Error message
            error_code: Internal error code
        """
        super().__init__(message, 500, error_code)


class ExternalServiceError(SDIMSError):
    """Exception for external service errors."""
    
    def __init__(
        self, 
        message: str, 
        service: str, 
        error_code: str = "EXTERNAL_SERVICE_ERROR"
    ):
        """
        Initialize external service error.
        
        Args:
            message: Error message
            service: Name of the external service
            error_code: Internal error code
        """
        super().__init__(f"{service} service error: {message}", 502, error_code)
        self.service = service


def format_error_response(error: Union[SDIMSError, Exception]) -> Dict[str, Any]:
    """
    Format error response for API Gateway.
    
    Args:
        error: Exception that occurred
        
    Returns:
        Formatted error response
    """
    if isinstance(error, SDIMSError):
        status_code = error.status_code
        body = {
            "error": {
                "code": error.error_code,
                "message": error.message
            }
        }
        
        # Add validation error details if available
        if isinstance(error, ValidationError) and error.details:
            body["error"]["details"] = error.details
            
    else:
        # For unexpected errors, return a generic error
        logger.exception("Unexpected error occurred", exc_info=error)
        status_code = 500
        body = {
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred"
            }
        }
    
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def handle_lambda_error(func):
    """
    Decorator to handle errors in Lambda functions.
    
    Args:
        func: Lambda handler function
        
    Returns:
        Wrapped function that handles errors
    """
    def wrapper(event, context):
        try:
            return func(event, context)
        except SDIMSError as e:
            logger.warning(f"Application error: {str(e)}", exc_info=True)
            return format_error_response(e)
        except Exception as e:
            logger.exception("Unexpected error", exc_info=True)
            return format_error_response(e)
    
    return wrapper 