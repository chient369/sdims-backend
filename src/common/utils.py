"""
Common utilities for SDIMS backend.
"""
from typing import Any, Dict, List, Optional, Union
import json
import os
import uuid
import datetime
from aws_lambda_powertools import Logger

logger = Logger(service="common-utils")

def generate_id(prefix: str = "") -> str:
    """
    Generate a unique ID.
    
    Args:
        prefix: Optional prefix for the ID
        
    Returns:
        Unique ID string
    """
    unique_id = str(uuid.uuid4())
    return f"{prefix}{unique_id}" if prefix else unique_id


def parse_json_body(body: Optional[str]) -> Dict[str, Any]:
    """
    Parse JSON body from API Gateway event.
    
    Args:
        body: JSON string from event body
        
    Returns:
        Parsed JSON object
        
    Raises:
        ValueError: If body is None or not valid JSON
    """
    if not body:
        return {}
        
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON body: {str(e)}")
        raise ValueError("Invalid JSON body") from e


def format_response(
    status_code: int = 200,
    body: Optional[Union[Dict[str, Any], List[Any]]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Format API Gateway response.
    
    Args:
        status_code: HTTP status code
        body: Response body
        headers: Response headers
        
    Returns:
        Formatted API Gateway response
    """
    response = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    }
    
    # Add custom headers
    if headers:
        response["headers"].update(headers)
        
    # Add body if provided
    if body is not None:
        response["body"] = json.dumps(body)
        
    return response


def get_path_parameter(event: Dict[str, Any], param_name: str) -> Optional[str]:
    """
    Get path parameter from API Gateway event.
    
    Args:
        event: API Gateway event
        param_name: Name of the parameter
        
    Returns:
        Parameter value or None if not found
    """
    path_parameters = event.get("pathParameters") or {}
    return path_parameters.get(param_name)


def get_query_parameter(event: Dict[str, Any], param_name: str) -> Optional[str]:
    """
    Get query string parameter from API Gateway event.
    
    Args:
        event: API Gateway event
        param_name: Name of the parameter
        
    Returns:
        Parameter value or None if not found
    """
    query_params = event.get("queryStringParameters") or {}
    return query_params.get(param_name)


def get_header(event: Dict[str, Any], header_name: str) -> Optional[str]:
    """
    Get header from API Gateway event.
    
    Args:
        event: API Gateway event
        header_name: Name of the header
        
    Returns:
        Header value or None if not found
    """
    headers = event.get("headers") or {}
    return headers.get(header_name)


def iso_timestamp() -> str:
    """
    Get current timestamp in ISO 8601 format.
    
    Returns:
        Current timestamp string
    """
    return datetime.datetime.utcnow().isoformat() + "Z"


def get_stage_name() -> str:
    """
    Get current deployment stage name.
    
    Returns:
        Stage name (dev, staging, prod)
    """
    return os.environ.get("STAGE", "dev")


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder that handles datetime objects."""
    
    def default(self, obj: Any) -> Any:
        """
        Convert datetime objects to ISO format strings.
        
        Args:
            obj: Object to encode
            
        Returns:
            JSON serializable object
        """
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return super().default(obj) 