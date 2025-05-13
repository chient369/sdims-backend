"""
Response Utilities for SDIMS

This module provides utilities for handling API Gateway responses.
"""

import json
from typing import Dict, Any, List, Optional, Union

class Response:
    """
    Class for handling API Gateway responses
    """
    
    @staticmethod
    def success(data: Any = None, status_code: int = 200) -> Dict[str, Any]:
        """
        Create a successful API response
        
        Args:
            data: Data to include in the response
            status_code: HTTP status code
                
        Returns:
            API Gateway response
        """
        body = {}
        if data is not None:
            body = data
                
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps(body, default=Response._json_serializer)
        }
    
    @staticmethod
    def error(message: str, status_code: int = 400, error_code: Optional[str] = None, details: Optional[Any] = None) -> Dict[str, Any]:
        """
        Create an error API response
        
        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Custom error code
            details: Additional error details
                
        Returns:
            API Gateway response
        """
        body = {
            'message': message
        }
        
        if error_code:
            body['code'] = error_code
            
        if details:
            body['details'] = details
                
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps(body, default=Response._json_serializer)
        }
    
    @staticmethod
    def paginated(items: List[Any], count: int, page: int, page_size: int, 
                 has_more: bool = False, status_code: int = 200, 
                 next_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a paginated API response
        
        Args:
            items: List of items for the current page
            count: Total number of items across all pages
            page: Current page number (1-based)
            page_size: Number of items per page
            has_more: Whether there are more pages
            status_code: HTTP status code
            next_token: Token for retrieving the next page (if applicable)
                
        Returns:
            API Gateway response with pagination metadata
        """
        body = {
            'items': items,
            'pagination': {
                'total': count,
                'page': page,
                'pageSize': page_size,
                'hasMore': has_more
            }
        }
        
        if next_token:
            body['pagination']['nextToken'] = next_token
            
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps(body, default=Response._json_serializer)
        }
    
    @staticmethod
    def redirect(location: str, status_code: int = 302) -> Dict[str, Any]:
        """
        Create a redirect response
        
        Args:
            location: URL to redirect to
            status_code: HTTP status code (301, 302, 307, 308)
                
        Returns:
            API Gateway response for redirection
        """
        return {
            'statusCode': status_code,
            'headers': {
                'Location': location,
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'
            },
            'body': ''
        }
    
    @staticmethod
    def binary(body: bytes, content_type: str = 'application/octet-stream', status_code: int = 200) -> Dict[str, Any]:
        """
        Create a binary response
        
        Args:
            body: Binary content
            content_type: Content type of the binary data
            status_code: HTTP status code
                
        Returns:
            API Gateway response with binary data
        """
        import base64
        
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': content_type,
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'
            },
            'body': base64.b64encode(body).decode('utf-8'),
            'isBase64Encoded': True
        }
    
    @staticmethod
    def _json_serializer(obj: Any) -> Any:
        """
        Custom JSON serializer for objects not serializable by default json code
        
        Args:
            obj: Object to serialize
                
        Returns:
            JSON serializable object
        """
        from decimal import Decimal
        import datetime
        
        if isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            return float(obj)
        elif isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
            return obj.to_dict()
        
        raise TypeError(f"Type {type(obj)} not serializable") 