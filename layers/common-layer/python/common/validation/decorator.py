"""
Validation Decorator

This module provides the validate_request decorator for Lambda handlers.
"""

import functools
import logging
from typing import Dict, Any, List, Optional, Callable, Union
from .schema_validator import SchemaValidator
from .validation_result import ValidationResult
from ..errors import ValidationError as ApplicationValidationError

# Initialize logger
logger = logging.getLogger("validation-decorator")

def validate_request(schema: Dict[str, Dict[str, List]], error_code: str = "E2000", 
                     error_message: str = "Dữ liệu không hợp lệ", 
                     bypass_validation: bool = False,
                     context_key: str = "validated_data"):
    """
    Decorator to validate API Gateway event against a schema
    
    Args:
        schema: Schema definition with sections like 'body', 'query_string', 'path_parameters'
        error_code: Error code to use for validation errors
        error_message: Error message to use for validation errors
        bypass_validation: Whether to bypass validation (for testing/development)
        context_key: Key to store validated data in the Lambda context
        
    Returns:
        Decorator function
    """
    def decorator(handler: Callable):
        @functools.wraps(handler)
        def wrapper(event, context):
            # Skip validation if bypass_validation is True
            if bypass_validation:
                logger.warning("Bypassing request validation")
                return handler(event, context)
                
            # Validate the event against the schema
            result = SchemaValidator.validate_event(event, schema)
            
            # Check if validation passed
            if not result.is_valid:
                # Log validation errors
                error_details = result.get_errors_list()
                logger.error("Validation failed", extra={"errors": error_details})
                
                # Raise validation error
                raise ApplicationValidationError(
                    message=error_message,
                    details={"errors": error_details},
                    error_code=error_code
                )
            
            # Store validated data in context
            if not hasattr(context, "data"):
                context.data = {}
                
            context.data[context_key] = _extract_validated_data(event, schema)
            
            # Call the original handler
            return handler(event, context)
        
        return wrapper
    
    return decorator

def _extract_validated_data(event: Dict[str, Any], schema: Dict[str, Dict[str, List]]) -> Dict[str, Any]:
    """
    Extract validated data from the event
    
    Args:
        event: API Gateway event
        schema: Schema definition
        
    Returns:
        Dictionary with validated data
    """
    validated_data = {}
    
    # Extract body if present
    if 'body' in schema:
        body = SchemaValidator._parse_body(event)
        if body:
            validated_data['body'] = body
            
    # Extract query string parameters if present
    if 'query_string' in schema:
        qs_params = SchemaValidator._get_query_string_parameters(event)
        if qs_params:
            validated_data['query_string'] = qs_params
            
    # Extract path parameters if present
    if 'path_parameters' in schema:
        path_params = SchemaValidator._get_path_parameters(event)
        if path_params:
            validated_data['path_parameters'] = path_params
            
    # Extract headers if present
    if 'headers' in schema:
        headers = SchemaValidator._get_headers(event)
        if headers:
            validated_data['headers'] = headers
            
    return validated_data 