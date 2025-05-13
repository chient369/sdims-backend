"""
API Gateway Request Parser Module.

This module provides utilities for parsing and validating API Gateway requests.
"""

import base64
import json
from typing import Any, Dict, Optional, Tuple, Union
from ..errors import ValidationError

def parse_path_parameters(event: Dict[str, Any]) -> Dict[str, str]:
    """
    Parse path parameters from API Gateway event.
    
    Args:
        event: API Gateway event
        
    Returns:
        Dictionary of path parameters
    """
    return event.get('pathParameters') or {}

def parse_query_parameters(event: Dict[str, Any]) -> Dict[str, str]:
    """
    Parse query string parameters from API Gateway event.
    
    Args:
        event: API Gateway event
        
    Returns:
        Dictionary of query parameters
    """
    return event.get('queryStringParameters') or {}

def parse_headers(event: Dict[str, Any]) -> Dict[str, str]:
    """
    Parse headers from API Gateway event.
    
    Args:
        event: API Gateway event
        
    Returns:
        Dictionary of headers
    """
    headers = event.get('headers') or {}
    return {k.lower(): v for k, v in headers.items()}

def parse_body(event: Dict[str, Any]) -> Optional[Any]:
    """
    Parse request body from API Gateway event.
    
    Args:
        event: API Gateway event
        
    Returns:
        Parsed body or None
    """
    body = event.get('body')
    if not body:
        return None
        
    is_base64 = event.get('isBase64Encoded', False)
    if is_base64:
        try:
            body = base64.b64decode(body).decode('utf-8')
        except Exception as e:
            raise ValidationError(f"Failed to decode base64 body: {str(e)}")
            
    content_type = parse_headers(event).get('content-type', '')
    
    if 'application/json' in content_type:
        try:
            return json.loads(body)
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON in request body: {str(e)}")
            
    elif 'application/x-www-form-urlencoded' in content_type:
        return parse_form_urlencoded(body)
        
    elif 'multipart/form-data' in content_type:
        boundary = get_multipart_boundary(content_type)
        return parse_multipart_form_data(body, boundary)
        
    return body

def parse_form_urlencoded(body: str) -> Dict[str, str]:
    """
    Parse application/x-www-form-urlencoded body.
    
    Args:
        body: Form urlencoded string
        
    Returns:
        Dictionary of form fields
    """
    from urllib.parse import parse_qs
    result = {}
    
    try:
        parsed = parse_qs(body, keep_blank_values=True)
        for key, values in parsed.items():
            result[key] = values[0] if len(values) == 1 else values
    except Exception as e:
        raise ValidationError(f"Failed to parse form data: {str(e)}")
        
    return result

def get_multipart_boundary(content_type: str) -> str:
    """
    Extract boundary from multipart/form-data content type.
    
    Args:
        content_type: Content-Type header value
        
    Returns:
        Boundary string
    """
    import re
    match = re.search(r'boundary=([^;]+)', content_type)
    if not match:
        raise ValidationError("No boundary found in multipart/form-data content type")
    return match.group(1)

def parse_multipart_form_data(body: str, boundary: str) -> Dict[str, Any]:
    """
    Parse multipart/form-data body.
    
    Args:
        body: Multipart form data string
        boundary: Form boundary
        
    Returns:
        Dictionary of form fields and files
    """
    result = {'fields': {}, 'files': {}}
    
    try:
        parts = body.split(f'--{boundary}')
        for part in parts[1:-1]:  # Skip first empty part and last boundary
            if not part.strip():
                continue
                
            # Split headers and content
            headers_raw, content = part.split('\r\n\r\n', 1)
            headers = parse_multipart_headers(headers_raw)
            
            # Get content disposition
            cd = headers.get('content-disposition', '')
            if not cd:
                continue
                
            # Parse content disposition
            cd_parts = {}
            for item in cd.split(';'):
                item = item.strip()
                if '=' in item:
                    k, v = item.split('=', 1)
                    cd_parts[k] = v.strip('"')
                    
            name = cd_parts.get('name')
            if not name:
                continue
                
            # Handle file upload
            if 'filename' in cd_parts:
                result['files'][name] = {
                    'filename': cd_parts['filename'],
                    'content_type': headers.get('content-type', 'application/octet-stream'),
                    'content': content.strip()
                }
            else:
                result['fields'][name] = content.strip()
                
    except Exception as e:
        raise ValidationError(f"Failed to parse multipart form data: {str(e)}")
        
    return result

def parse_multipart_headers(headers_raw: str) -> Dict[str, str]:
    """
    Parse headers from multipart form data part.
    
    Args:
        headers_raw: Raw headers string
        
    Returns:
        Dictionary of headers
    """
    headers = {}
    
    for line in headers_raw.split('\r\n'):
        line = line.strip()
        if not line:
            continue
            
        if ':' in line:
            name, value = line.split(':', 1)
            headers[name.strip().lower()] = value.strip()
            
    return headers

def get_client_ip(event: Dict[str, Any]) -> str:
    """
    Get client IP address from API Gateway event.
    
    Args:
        event: API Gateway event
        
    Returns:
        Client IP address
    """
    headers = parse_headers(event)
    
    # Check X-Forwarded-For header
    forwarded_for = headers.get('x-forwarded-for')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
        
    # Check source IP from API Gateway
    request_context = event.get('requestContext', {})
    return request_context.get('identity', {}).get('sourceIp', 'unknown')

def get_user_agent(event: Dict[str, Any]) -> str:
    """
    Get user agent from API Gateway event.
    
    Args:
        event: API Gateway event
        
    Returns:
        User agent string
    """
    headers = parse_headers(event)
    return headers.get('user-agent', 'unknown')

def get_request_id(event: Dict[str, Any]) -> str:
    """
    Get request ID from API Gateway event.
    
    Args:
        event: API Gateway event
        
    Returns:
        Request ID
    """
    request_context = event.get('requestContext', {})
    return request_context.get('requestId', 'unknown') 