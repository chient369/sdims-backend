from typing import List, Dict, Any, Optional


class BaseError(Exception):
    """Base error class for all application exceptions."""
    
    def __init__(self, message: str = "An error occurred", error_code: str = "INTERNAL_ERROR", status_code: int = 500):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(BaseError):
    """Error raised when input validation fails."""
    
    def __init__(self, message: str = "Validation error", errors: Optional[List[Dict[str, Any]]] = None):
        super().__init__(message=message, error_code="VALIDATION_ERROR", status_code=400)
        self.errors = errors or []


class AuthorizationError(BaseError):
    """Error raised when user doesn't have permission."""
    
    def __init__(self, message: str = "You don't have permission to perform this action"):
        super().__init__(message=message, error_code="AUTHORIZATION_ERROR", status_code=403)


class AuthenticationError(BaseError):
    """Error raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message=message, error_code="AUTHENTICATION_ERROR", status_code=401)


class NotFoundException(BaseError):
    """Error raised when a resource is not found."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, error_code="RESOURCE_NOT_FOUND", status_code=404)


class DatabaseError(BaseError):
    """Error raised when database operations fail."""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message=message, error_code="DATABASE_ERROR", status_code=500)
        
        
class RateLimitError(BaseError):
    """Error raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message=message, error_code="RATE_LIMIT_ERROR", status_code=429)


class BusinessLogicError(BaseError):
    """Error raised for business logic violations."""
    
    def __init__(self, message: str = "Business rule violation", error_code: str = "BUSINESS_LOGIC_ERROR", status_code: int = 400):
        super().__init__(message=message, error_code=error_code, status_code=status_code)


class AccountLockedError(AuthenticationError):
    """Error raised when account is locked."""
    
    def __init__(self, message: str = "Account is locked"):
        super().__init__(message)
        self.error_code = "ACCOUNT_LOCKED" 