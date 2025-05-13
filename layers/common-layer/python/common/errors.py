"""
Custom exceptions for API Gateway integration.

This module defines custom exceptions that can be used across the application
to handle various error scenarios in a consistent way.
"""

from typing import Any, Dict, List, Optional

class APIError(Exception):
    """
    Base class for API errors.
    """
    
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

class ValidationError(APIError):
    """
    Error raised when request validation fails.
    """
    
    def __init__(
        self,
        message: str,
        errors: Optional[List[Dict[str, str]]] = None
    ):
        super().__init__(
            code='E2000',
            message=message,
            status_code=400,
            details={'errors': errors or []}
        )

class AuthenticationError(APIError):
    """
    Error raised when authentication fails.
    """
    
    def __init__(self, message: str = 'Authentication failed'):
        super().__init__(
            code='E1001',
            message=message,
            status_code=401
        )

class AuthorizationError(APIError):
    """
    Error raised when authorization fails.
    """
    
    def __init__(self, message: str = 'Insufficient permissions'):
        super().__init__(
            code='E1002',
            message=message,
            status_code=403
        )

class ResourceNotFoundError(APIError):
    """
    Error raised when a requested resource is not found.
    """
    
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            code='E3000',
            message=f'{resource} not found with ID: {resource_id}',
            status_code=404
        )

class ResourceConflictError(APIError):
    """
    Error raised when there is a conflict with existing resource.
    """
    
    def __init__(self, message: str):
        super().__init__(
            code='E4000',
            message=message,
            status_code=409
        )

class BusinessLogicError(APIError):
    """
    Error raised when a business rule is violated.
    """
    
    def __init__(self, message: str):
        super().__init__(
            code='E4005',
            message=message,
            status_code=422
        )

class ExternalServiceError(APIError):
    """
    Error raised when an external service call fails.
    """
    
    def __init__(
        self,
        service: str,
        message: str,
        original_error: Optional[Exception] = None
    ):
        super().__init__(
            code='E5003',
            message=f'Error calling {service}: {message}',
            status_code=502,
            details={'original_error': str(original_error) if original_error else None}
        )

class DatabaseError(APIError):
    """
    Error raised when a database operation fails.
    """
    
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(
            code='E6001',
            message=f'Database error: {message}',
            status_code=500,
            details={'original_error': str(original_error) if original_error else None}
        )

class FileOperationError(APIError):
    """
    Error raised when a file operation fails.
    """
    
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(
            code='E6002',
            message=f'File operation error: {message}',
            status_code=500,
            details={'original_error': str(original_error) if original_error else None}
        )

class RateLimitExceededError(APIError):
    """
    Error raised when rate limit is exceeded.
    """
    
    def __init__(self, limit: int, reset_time: int):
        super().__init__(
            code='E1006',
            message='Rate limit exceeded',
            status_code=429,
            details={
                'limit': limit,
                'reset_time': reset_time
            }
        )

class InvalidTokenError(APIError):
    """
    Error raised when JWT token is invalid.
    """
    
    def __init__(self, message: str = 'Invalid token'):
        super().__init__(
            code='E1000',
            message=message,
            status_code=401
        )

class ServiceUnavailableError(APIError):
    """
    Error raised when service is temporarily unavailable.
    """
    
    def __init__(self, message: str = 'Service temporarily unavailable'):
        super().__init__(
            code='E6003',
            message=message,
            status_code=503
        ) 