"""
API Gateway Response Formatter Module.

This module provides utilities for formatting responses in a consistent way
across all API endpoints.
"""

import base64
import json
from typing import Any, Dict, List, Optional, Union
from ..errors import APIError

def format_success_response(
    data: Any = None,
    message: str = None,
    status_code: int = 200,
    headers: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Format a successful response.
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
        headers: Additional headers
        
    Returns:
        Formatted response dictionary
    """
    body = {
        'status': 'success'
    }
    
    if data is not None:
        body['data'] = data
        
    if message:
        body['message'] = message
        
    return create_response(body, status_code, headers)

def format_error_response(
    error: Union[APIError, Exception],
    status_code: int = None,
    headers: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Format an error response.
    
    Args:
        error: Error object
        status_code: HTTP status code
        headers: Additional headers
        
    Returns:
        Formatted error response dictionary
    """
    if isinstance(error, APIError):
        body = {
            'status': 'error',
            'code': error.code,
            'message': error.message
        }
        status_code = error.status_code
    else:
        body = {
            'status': 'error',
            'code': 'E6000',
            'message': str(error)
        }
        status_code = status_code or 500
        
    return create_response(body, status_code, headers)

def format_validation_error(
    errors: List[Dict[str, str]],
    message: str = 'Validation error',
    headers: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Format a validation error response.
    
    Args:
        errors: List of validation errors
        message: Error message
        headers: Additional headers
        
    Returns:
        Formatted validation error response
    """
    body = {
        'status': 'error',
        'code': 'E2000',
        'message': message,
        'errors': errors
    }
    
    return create_response(body, 400, headers)

def format_paginated_response(
    items: List[Any],
    total: int,
    page: int,
    limit: int,
    message: str = None,
    headers: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Format a paginated response.
    
    Args:
        items: List of items
        total: Total number of items
        page: Current page number
        limit: Items per page
        message: Optional message
        headers: Additional headers
        
    Returns:
        Formatted paginated response
    """
    total_pages = (total + limit - 1) // limit
    
    body = {
        'status': 'success',
        'data': {
            'items': items,
            'pagination': {
                'total': total,
                'page': page,
                'limit': limit,
                'pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }
    }
    
    if message:
        body['message'] = message
        
    return create_response(body, 200, headers)

def format_binary_response(
    content: bytes,
    content_type: str,
    filename: str = None,
    headers: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Format a binary response (e.g., file download).
    
    Args:
        content: Binary content
        content_type: Content type
        filename: Optional filename for download
        headers: Additional headers
        
    Returns:
        Formatted binary response
    """
    headers = headers or {}
    headers['Content-Type'] = content_type
    
    if filename:
        headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        
    return {
        'statusCode': 200,
        'headers': headers,
        'body': base64.b64encode(content).decode('utf-8'),
        'isBase64Encoded': True
    }

def create_response(
    body: Any,
    status_code: int = 200,
    headers: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Create an API Gateway response object.
    
    Args:
        body: Response body
        status_code: HTTP status code
        headers: Additional headers
        
    Returns:
        API Gateway response dictionary
    """
    headers = headers or {}
    headers.update({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    })
    
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(body)
    }

def format_no_content_response(headers: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Format a 204 No Content response.
    
    Args:
        headers: Additional headers
        
    Returns:
        No content response dictionary
    """
    return create_response(None, 204, headers)

def format_created_response(
    data: Any = None,
    message: str = None,
    headers: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Format a 201 Created response.
    
    Args:
        data: Created resource data
        message: Success message
        headers: Additional headers
        
    Returns:
        Created response dictionary
    """
    return format_success_response(data, message, 201, headers)

def format_accepted_response(
    message: str = 'Request accepted',
    headers: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Format a 202 Accepted response.
    
    Args:
        message: Acceptance message
        headers: Additional headers
        
    Returns:
        Accepted response dictionary
    """
    body = {
        'status': 'success',
        'message': message
    }
    
    return create_response(body, 202, headers)

def format_not_modified_response(headers: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Format a 304 Not Modified response.
    
    Args:
        headers: Additional headers
        
    Returns:
        Not modified response dictionary
    """
    return create_response(None, 304, headers)

def format_redirect_response(
    location: str,
    permanent: bool = False,
    headers: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Format a redirect response.
    
    Args:
        location: Redirect URL
        permanent: Whether the redirect is permanent
        headers: Additional headers
        
    Returns:
        Redirect response dictionary
    """
    headers = headers or {}
    headers['Location'] = location
    
    return create_response(
        None,
        301 if permanent else 302,
        headers
    ) 