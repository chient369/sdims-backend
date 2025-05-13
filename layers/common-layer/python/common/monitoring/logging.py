from fastapi import Request
from aws_lambda_powertools import Logger
from typing import Optional, Dict, Any, Callable
import time
import json
import os

# Initialize logger
logger = Logger(service="api")

class RequestLoggingMiddleware:
    def __init__(self, app):
        """
        Initialize logging middleware
        
        Args:
            app: FastAPI application instance
        """
        self.app = app
        
    async def __call__(self, request: Request, call_next):
        """
        Process request and log details
        
        Args:
            request: FastAPI request object
            call_next: Next middleware in chain
            
        Returns:
            Response from next middleware
        """
        # Start timing
        start_time = time.time()
        
        # Get request details
        method = request.method
        path = request.url.path
        query_params = dict(request.query_params)
        headers = dict(request.headers)
        client_host = request.client.host if request.client else None
        
        # Remove sensitive headers
        self._sanitize_headers(headers)
        
        # Log request
        logger.info(
            "Request started",
            extra={
                "method": method,
                "path": path,
                "query_params": query_params,
                "headers": headers,
                "client_host": client_host,
                "request_id": headers.get("x-request-id")
            }
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            logger.info(
                "Request completed",
                extra={
                    "method": method,
                    "path": path,
                    "status_code": response.status_code,
                    "duration": duration,
                    "request_id": headers.get("x-request-id")
                }
            )
            
            return response
            
        except Exception as e:
            # Log error
            logger.exception(
                "Request failed",
                extra={
                    "method": method,
                    "path": path,
                    "error": str(e),
                    "request_id": headers.get("x-request-id")
                }
            )
            raise
            
    def _sanitize_headers(self, headers: Dict[str, str]) -> None:
        """
        Remove sensitive information from headers
        
        Args:
            headers: Request headers dict
        """
        sensitive_headers = [
            "authorization",
            "x-api-key",
            "cookie"
        ]
        
        for header in sensitive_headers:
            if header in headers:
                headers[header] = "[REDACTED]"

def setup_logging():
    """
    Configure logging for the application
    """
    # Set log level from environment
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logger.setLevel(log_level)
    
    # Add custom formatting if needed
    logger.addHandler(get_custom_handler())
    
def get_custom_handler() -> Callable:
    """
    Create custom log handler with formatting
    
    Returns:
        Configured log handler
    """
    # TODO: Implement custom handler if needed
    pass

def log_error(
    error: Exception,
    request: Optional[Request] = None,
    context: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log error with context
    
    Args:
        error: Exception that occurred
        request: Optional request object
        context: Optional additional context
    """
    error_context = {
        "error_type": error.__class__.__name__,
        "error_message": str(error)
    }
    
    if request:
        error_context.update({
            "method": request.method,
            "path": request.url.path,
            "client_host": request.client.host if request.client else None,
            "request_id": request.headers.get("x-request-id")
        })
        
    if context:
        error_context.update(context)
        
    logger.exception(
        "Error occurred",
        extra=error_context
    ) 