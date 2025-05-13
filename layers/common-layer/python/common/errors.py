"""
Error Handling Utilities for SDIMS

This module provides error handling utilities.
"""

from typing import Dict, Any, List, Optional, Union

class ApplicationError(Exception):
    """Base exception for application errors"""
    
    def __init__(self, message: str, status_code: int = 500, error_code: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

class BadRequestError(ApplicationError):
    """Exception for bad requests"""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message, 400, error_code or 'E2000')

class ValidationError(BadRequestError):
    """Exception for validation errors"""
    
    def __init__(self, message: str, details: Optional[Dict[str, List[str]]] = None, error_code: Optional[str] = None):
        self.details = details
        super().__init__(message, error_code or 'E2001')

class UnauthorizedError(ApplicationError):
    """Exception for unauthorized access"""
    
    def __init__(self, message: str = "Unauthorized", error_code: Optional[str] = None):
        super().__init__(message, 401, error_code or 'E1000')

class ForbiddenError(ApplicationError):
    """Exception for forbidden access"""
    
    def __init__(self, message: str = "Forbidden", error_code: Optional[str] = None):
        super().__init__(message, 403, error_code or 'E1002')

class NotFoundError(ApplicationError):
    """Exception for resource not found"""
    
    def __init__(self, message: str = "Resource not found", error_code: Optional[str] = None):
        super().__init__(message, 404, error_code or 'E3000')

class ResourceNotFoundError(NotFoundError):
    """Exception for specific resource not found"""
    
    def __init__(self, resource_type: str, resource_id: Optional[str] = None, error_code: Optional[str] = None):
        message = f"{resource_type} not found"
        if resource_id:
            message = f"{resource_type} with ID '{resource_id}' not found"
        super().__init__(message, error_code or 'E3001')

class ConflictError(ApplicationError):
    """Exception for resource conflict"""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message, 409, error_code or 'E4004')

class DuplicateResourceError(ConflictError):
    """Exception for duplicate resource"""
    
    def __init__(self, resource_type: str, identifier: str, field: str = 'ID', error_code: Optional[str] = None):
        message = f"{resource_type} with {field} '{identifier}' already exists"
        super().__init__(message, error_code or 'E4001')

class InternalServerError(ApplicationError):
    """Exception for internal server errors"""
    
    def __init__(self, message: str = "Internal server error", error_code: Optional[str] = None):
        super().__init__(message, 500, error_code or 'E5000')

class DatabaseError(ApplicationError):
    """Exception for database errors"""
    
    def __init__(self, message: str = "Database error occurred", error_code: Optional[str] = None):
        super().__init__(message, 500, error_code or 'E5001')

class ServiceUnavailableError(ApplicationError):
    """Exception for service unavailable"""
    
    def __init__(self, message: str = "Service temporarily unavailable", error_code: Optional[str] = None):
        super().__init__(message, 503, error_code or 'E5003')

def handle_error(error: Exception) -> Dict[str, Any]:
    """
    Handle exceptions and return appropriate API response
    
    Args:
        error: Exception to handle
            
    Returns:
        API Gateway response
    """
    from common.response import Response
    from common.logger import Logger
    
    logger = Logger(service="error-handler")
    
    if isinstance(error, ApplicationError):
        if isinstance(error, ValidationError) and error.details:
            return Response.error(
                message=error.message,
                status_code=error.status_code,
                error_code=error.error_code,
                details=error.details
            )
        return Response.error(
            message=error.message,
            status_code=error.status_code,
            error_code=error.error_code
        )
    
    # Handle unexpected errors
    logger.error("Unexpected error", exc=error)
    return Response.error(
        message="Internal server error",
        status_code=500,
        error_code="E6000"
    )

def http_error_handler(func):
    """
    Decorator for handling errors in Lambda handlers
    
    Args:
        func: Lambda handler function
            
    Returns:
        Decorated function
    """
    def wrapper(event, context):
        try:
            return func(event, context)
        except Exception as error:
            return handle_error(error)
    return wrapper 