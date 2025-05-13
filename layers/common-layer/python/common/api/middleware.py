"""
API Gateway Middleware System.

This module provides the middleware framework for processing requests
before and after the main handler execution.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional
from aws_lambda_powertools import Logger
from .api_handler import RequestContext, APIResponse

# Initialize logger
logger = Logger()

class Middleware(ABC):
    """
    Abstract base class for all middleware implementations.
    """
    
    @abstractmethod
    async def process(self, context: RequestContext, next_handler: Callable) -> Any:
        """
        Process the request/response chain.
        
        Args:
            context: The request context
            next_handler: The next handler in the chain
            
        Returns:
            The response from the handler chain
        """
        pass

class MiddlewareChain:
    """
    Manages the execution of middleware chain.
    """
    
    def __init__(self, middlewares: List[Middleware]):
        self.middlewares = middlewares
        
    async def execute(self, context: RequestContext, handler: Callable) -> Any:
        """
        Execute the middleware chain.
        
        Args:
            context: The request context
            handler: The final handler function
            
        Returns:
            The response from the handler chain
        """
        
        async def create_chain(index: int) -> Callable:
            if index >= len(self.middlewares):
                return handler
                
            middleware = self.middlewares[index]
            next_handler = await create_chain(index + 1)
            
            return lambda ctx: middleware.process(ctx, next_handler)
            
        chain = await create_chain(0)
        return await chain(context)

class LoggingMiddleware(Middleware):
    """
    Middleware for request/response logging.
    """
    
    async def process(self, context: RequestContext, next_handler: Callable) -> Any:
        method = context.method
        path = context.path
        
        logger.info(f"Request: {method} {path}", extra={
            'path_params': context.path_params,
            'query_params': context.query_params,
            'headers': {k: v for k, v in context.headers.items() if k.lower() != 'authorization'}
        })
        
        try:
            response = await next_handler(context)
            
            if isinstance(response, dict):
                status_code = response.get('statusCode', 200)
            elif isinstance(response, APIResponse):
                status_code = response.status_code
            else:
                status_code = 200
                
            logger.info(f"Response: {status_code}", extra={
                'method': method,
                'path': path,
                'status_code': status_code
            })
            
            return response
            
        except Exception as e:
            logger.error(f"Error in request: {method} {path}", extra={
                'error': str(e),
                'method': method,
                'path': path
            })
            raise

class TracingMiddleware(Middleware):
    """
    Middleware for request tracing.
    """
    
    async def process(self, context: RequestContext, next_handler: Callable) -> Any:
        trace_id = context.get_header('X-Trace-Id')
        if not trace_id:
            trace_id = context.context.aws_request_id
            context.set_header('X-Trace-Id', trace_id)
            
        logger.append_keys(trace_id=trace_id)
        
        try:
            response = await next_handler(context)
            
            if isinstance(response, dict):
                response.setdefault('headers', {})['X-Trace-Id'] = trace_id
            elif isinstance(response, APIResponse):
                response.headers['X-Trace-Id'] = trace_id
                
            return response
            
        except Exception as e:
            logger.error(f"Error in request trace: {trace_id}", extra={
                'error': str(e),
                'trace_id': trace_id
            })
            raise

class CORSMiddleware(Middleware):
    """
    Middleware for handling CORS headers.
    """
    
    def __init__(
        self,
        allow_origins: List[str] = None,
        allow_methods: List[str] = None,
        allow_headers: List[str] = None,
        max_age: int = 86400
    ):
        self.allow_origins = allow_origins or ['*']
        self.allow_methods = allow_methods or ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
        self.allow_headers = allow_headers or [
            'Content-Type',
            'Authorization',
            'X-Api-Key',
            'X-Amz-Date',
            'X-Amz-Security-Token'
        ]
        self.max_age = max_age
        
    async def process(self, context: RequestContext, next_handler: Callable) -> Any:
        # Handle preflight requests
        if context.method == 'OPTIONS':
            return APIResponse(
                status_code=200,
                headers={
                    'Access-Control-Allow-Origin': ','.join(self.allow_origins),
                    'Access-Control-Allow-Methods': ','.join(self.allow_methods),
                    'Access-Control-Allow-Headers': ','.join(self.allow_headers),
                    'Access-Control-Max-Age': str(self.max_age)
                }
            )
            
        response = await next_handler(context)
        
        # Add CORS headers to response
        if isinstance(response, dict):
            response.setdefault('headers', {}).update({
                'Access-Control-Allow-Origin': ','.join(self.allow_origins),
                'Access-Control-Allow-Methods': ','.join(self.allow_methods)
            })
        elif isinstance(response, APIResponse):
            response.headers.update({
                'Access-Control-Allow-Origin': ','.join(self.allow_origins),
                'Access-Control-Allow-Methods': ','.join(self.allow_methods)
            })
            
        return response

class SecurityHeadersMiddleware(Middleware):
    """
    Middleware for adding security headers.
    """
    
    async def process(self, context: RequestContext, next_handler: Callable) -> Any:
        response = await next_handler(context)
        
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'",
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
        
        if isinstance(response, dict):
            response.setdefault('headers', {}).update(security_headers)
        elif isinstance(response, APIResponse):
            response.headers.update(security_headers)
            
        return response

class RateLimitingMiddleware(Middleware):
    """
    Middleware for basic rate limiting.
    """
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        # Note: In a production environment, use Redis or DynamoDB for rate limiting
        
    async def process(self, context: RequestContext, next_handler: Callable) -> Any:
        # Implement rate limiting logic here
        # This is a placeholder for actual implementation
        return await next_handler(context)

class ErrorHandlingMiddleware(Middleware):
    """
    Middleware for consistent error handling.
    """
    
    async def process(self, context: RequestContext, next_handler: Callable) -> Any:
        try:
            return await next_handler(context)
        except Exception as e:
            logger.error(f"Unhandled error in request", extra={
                'error': str(e),
                'method': context.method,
                'path': context.path
            })
            
            # Convert to APIResponse with appropriate error format
            return APIResponse(
                status_code=500,
                body={
                    'status': 'error',
                    'code': 'E6000',
                    'message': 'Internal server error',
                    'traceId': context.context.aws_request_id
                }
            ) 