"""
Request Validation Module.

This module provides utilities for validating request data against JSON schemas
and other validation rules.
"""

import json
from typing import Any, Dict, List, Optional, Union
from jsonschema import validate as json_validate, ValidationError as JsonSchemaError
from .errors import ValidationError

def validate_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> None:
    """
    Validate data against a JSON schema.
    
    Args:
        data: Data to validate
        schema: JSON schema to validate against
        
    Raises:
        ValidationError: If validation fails
    """
    try:
        json_validate(instance=data, schema=schema)
    except JsonSchemaError as e:
        path = ' -> '.join(str(p) for p in e.path)
        error = {
            'field': path,
            'message': e.message
        }
        raise ValidationError(
            message='Schema validation failed',
            errors=[error]
        )

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """
    Validate that required fields are present in data.
    
    Args:
        data: Data to validate
        required_fields: List of required field names
        
    Raises:
        ValidationError: If any required field is missing
    """
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)
            
    if missing_fields:
        errors = [
            {
                'field': field,
                'message': 'This field is required'
            }
            for field in missing_fields
        ]
        raise ValidationError(
            message='Required fields missing',
            errors=errors
        )

def validate_field_type(
    data: Dict[str, Any],
    field: str,
    expected_type: Union[type, tuple],
    allow_none: bool = False
) -> None:
    """
    Validate that a field has the expected type.
    
    Args:
        data: Data containing the field
        field: Name of the field to validate
        expected_type: Expected Python type or tuple of types
        allow_none: Whether None is allowed as a value
        
    Raises:
        ValidationError: If field type is invalid
    """
    if field not in data:
        return
        
    value = data[field]
    if value is None and allow_none:
        return
        
    if not isinstance(value, expected_type):
        error = {
            'field': field,
            'message': f'Expected type {expected_type.__name__}, got {type(value).__name__}'
        }
        raise ValidationError(
            message='Invalid field type',
            errors=[error]
        )

def validate_enum(data: Dict[str, Any], field: str, allowed_values: List[Any]) -> None:
    """
    Validate that a field value is one of the allowed values.
    
    Args:
        data: Data containing the field
        field: Name of the field to validate
        allowed_values: List of allowed values
        
    Raises:
        ValidationError: If field value is not in allowed values
    """
    if field not in data:
        return
        
    value = data[field]
    if value not in allowed_values:
        error = {
            'field': field,
            'message': f'Value must be one of: {", ".join(str(v) for v in allowed_values)}'
        }
        raise ValidationError(
            message='Invalid enum value',
            errors=[error]
        )

def validate_string_length(
    data: Dict[str, Any],
    field: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None
) -> None:
    """
    Validate string field length.
    
    Args:
        data: Data containing the field
        field: Name of the field to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        
    Raises:
        ValidationError: If string length is invalid
    """
    if field not in data or data[field] is None:
        return
        
    value = str(data[field])
    length = len(value)
    
    if min_length is not None and length < min_length:
        error = {
            'field': field,
            'message': f'Must be at least {min_length} characters long'
        }
        raise ValidationError(
            message='String too short',
            errors=[error]
        )
        
    if max_length is not None and length > max_length:
        error = {
            'field': field,
            'message': f'Must be at most {max_length} characters long'
        }
        raise ValidationError(
            message='String too long',
            errors=[error]
        )

def validate_numeric_range(
    data: Dict[str, Any],
    field: str,
    minimum: Optional[Union[int, float]] = None,
    maximum: Optional[Union[int, float]] = None
) -> None:
    """
    Validate numeric field range.
    
    Args:
        data: Data containing the field
        field: Name of the field to validate
        minimum: Minimum allowed value
        maximum: Maximum allowed value
        
    Raises:
        ValidationError: If numeric value is out of range
    """
    if field not in data or data[field] is None:
        return
        
    value = data[field]
    if not isinstance(value, (int, float)):
        error = {
            'field': field,
            'message': 'Must be a numeric value'
        }
        raise ValidationError(
            message='Invalid numeric value',
            errors=[error]
        )
        
    if minimum is not None and value < minimum:
        error = {
            'field': field,
            'message': f'Must be greater than or equal to {minimum}'
        }
        raise ValidationError(
            message='Value too small',
            errors=[error]
        )
        
    if maximum is not None and value > maximum:
        error = {
            'field': field,
            'message': f'Must be less than or equal to {maximum}'
        }
        raise ValidationError(
            message='Value too large',
            errors=[error]
        ) 