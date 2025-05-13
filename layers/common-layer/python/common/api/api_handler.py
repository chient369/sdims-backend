"""
API Gateway Integration Handler Module.

This module provides the core functionality for handling API Gateway requests
and responses in a standardized way across all Lambda functions.
"""

import functools
import json
import traceback
from typing import Any, Callable, Dict, List, Optional, Union
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from ..validation import validate_schema
from ..errors import APIError, ValidationError
from ..auth import verify_token, get_user_permissions

# Initialize logger and tracer
logger = Logger()
tracer = Tracer()

class RequestContext:
    """
    Request context object that holds parsed and validated request data.
    """
    
    def __init__(
        self,
        event: Dict[str, Any],
        context: LambdaContext,
        path_params: Dict[str, str] = None,
        query_params: Dict[str, str] = None,
        headers: Dict[str, str] = None,
        body: Any = None,
        user: Dict[str, Any] = None
    ):
        self.event = event
        self.context = context
        self.path_params = path_params or {}
        self.query_params = query_params or {}
        self.headers = headers or {}
        self.body = body
        self.user = user
        self.logger = logger
        
    @property
    def method(self) -> str:
        """Get HTTP method from event."""
        return self.event.get('httpMethod', '')
        
    @property
    def path(self) -> str:
        """Get request path from event."""
        return self.event.get('path', '')
    
    def get_header(self, name: str, default: str = None) -> Optional[str]:
        """Get header value by name."""
        return self.headers.get(name, default)
    
    def set_header(self, name: str, value: str):
        """Set header value."""
        self.headers[name] = value

class APIResponse:
    """
    Standardized API response object.
    """
    
    def __init__(
        self,
        status_code: int = 200,
        body: Any = None,
        headers: Dict[str, str] = None
    ):
        self.status_code = status_code
        self.body = body
        self.headers = headers or {}
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to API Gateway format."""
        return {
            'statusCode': self.status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
                **self.headers
            },
            'body': json.dumps(self.body) if self.body is not None else ''
        }

def api_handler(
    path: str = None,
    method: str = None,
    schema: Dict[str, Any] = None,
    requires_auth: bool = True,
    permissions: List[str] = None,
    cors: bool = True
) -> Callable:
    """
    Decorator for API Gateway Lambda handlers.
    
    Args:
        path: API path
        method: HTTP method
        schema: Request validation schema
        requires_auth: Whether authentication is required
        permissions: Required permissions
        cors: Whether to enable CORS
    """
    def decorator(handler_func: Callable) -> Callable:
        @functools.wraps(handler_func)
        @tracer.capture_lambda_handler
        @logger.inject_lambda_context
        def wrapper(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
            try:
                # Parse request
                headers = {k.lower(): v for k, v in event.get('headers', {}).items()}
                path_params = event.get('pathParameters', {})
                query_params = event.get('queryStringParameters', {})
                
                # Parse body if present
                body = None
                if event.get('body'):
                    try:
                        body = json.loads(event['body'])
                    except json.JSONDecodeError:
                        raise ValidationError('Invalid JSON in request body')
                
                # Validate schema if provided
                if schema:
                    validate_schema(
                        {
                            'headers': headers,
                            'path_params': path_params,
                            'query_params': query_params,
                            'body': body
                        },
                        schema
                    )
                
                # Handle authentication
                user = None
                if requires_auth:
                    auth_header = headers.get('authorization')
                    if not auth_header:
                        raise APIError('E1001', 'Authorization header is missing', 401)
                    
                    token = auth_header.replace('Bearer ', '')
                    user = verify_token(token)
                    
                    # Check permissions
                    if permissions:
                        user_permissions = get_user_permissions(user['id'])
                        if not any(p in user_permissions for p in permissions):
                            raise APIError('E1002', 'Insufficient permissions', 403)
                
                # Create request context
                request_context = RequestContext(
                    event=event,
                    context=context,
                    path_params=path_params,
                    query_params=query_params,
                    headers=headers,
                    body=body,
                    user=user
                )
                
                # Execute handler
                response = handler_func(request_context)
                
                # Convert response to standard format
                if isinstance(response, APIResponse):
                    return response.to_dict()
                else:
                    return APIResponse(body=response).to_dict()
                    
            except ValidationError as e:
                logger.warning(f"Validation error: {str(e)}")
                return APIResponse(
                    status_code=400,
                    body={
                        'status': 'error',
                        'code': 'E2000',
                        'message': str(e)
                    }
                ).to_dict()
                
            except APIError as e:
                logger.warning(f"API error: {str(e)}")
                return APIResponse(
                    status_code=e.status_code,
                    body={
                        'status': 'error',
                        'code': e.code,
                        'message': e.message
                    }
                ).to_dict()
                
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                logger.error(traceback.format_exc())
                return APIResponse(
                    status_code=500,
                    body={
                        'status': 'error',
                        'code': 'E6000',
                        'message': 'Internal server error',
                        'traceId': context.aws_request_id
                    }
                ).to_dict()
                
        return wrapper
    return decorator 