"""
Validation Utilities for SDIMS

This module provides utilities for validating input data.
"""

import re
import json
from typing import Dict, Any, List, Optional, Union, Callable, Pattern
from datetime import datetime

class ValidationError(Exception):
    """Exception raised for validation errors"""
    
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(self.message)

class ValidationResult:
    """Class to hold validation results"""
    
    def __init__(self):
        self.errors: List[ValidationError] = []
        
    def add_error(self, field: str, message: str) -> None:
        """
        Add a validation error
        
        Args:
            field: Field name that failed validation
            message: Error message
        """
        self.errors.append(ValidationError(field, message))
        
    @property
    def is_valid(self) -> bool:
        """
        Check if validation passed
        
        Returns:
            True if no errors, False otherwise
        """
        return len(self.errors) == 0
        
    def to_dict(self) -> Dict[str, List[str]]:
        """
        Convert validation errors to dictionary
        
        Returns:
            Dictionary with field names as keys and list of error messages as values
        """
        result: Dict[str, List[str]] = {}
        for error in self.errors:
            if error.field not in result:
                result[error.field] = []
            result[error.field].append(error.message)
        return result

class Validator:
    """
    Class for validating request inputs
    """
    
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    URL_PATTERN = re.compile(r"^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(/[-\w%.]+)*(?:\?\S+)?$")
    PHONE_PATTERN = re.compile(r"^\+?[0-9]{10,15}$")
    
    @staticmethod
    def validate_required(data: Dict[str, Any], required_fields: List[str]) -> ValidationResult:
        """
        Validate that all required fields are present
        
        Args:
            data: Data to validate
            required_fields: List of fields that must be present
                
        Returns:
            ValidationResult with any validation errors
        """
        result = ValidationResult()
        for field in required_fields:
            if field not in data or data[field] is None:
                result.add_error(field, f"Field '{field}' is required")
        return result
    
    @staticmethod
    def validate_string(value: Any, field: str, min_length: int = 0, 
                      max_length: Optional[int] = None, 
                      pattern: Optional[Union[str, Pattern]] = None) -> Optional[ValidationError]:
        """
        Validate a string field
        
        Args:
            value: Value to validate
            field: Field name for the error message
            min_length: Minimum length of the string
            max_length: Maximum length of the string
            pattern: Regular expression pattern the string must match
                
        Returns:
            ValidationError if validation fails, None otherwise
        """
        if value is None:
            return None
            
        if not isinstance(value, str):
            return ValidationError(field, f"Field '{field}' must be a string")
            
        if len(value) < min_length:
            return ValidationError(field, f"Field '{field}' must be at least {min_length} characters")
            
        if max_length is not None and len(value) > max_length:
            return ValidationError(field, f"Field '{field}' must be at most {max_length} characters")
            
        if pattern is not None:
            if isinstance(pattern, str):
                pattern = re.compile(pattern)
                
            if not pattern.match(value):
                return ValidationError(field, f"Field '{field}' has invalid format")
                
        return None
    
    @staticmethod
    def validate_number(value: Any, field: str, 
                      min_value: Optional[Union[int, float]] = None, 
                      max_value: Optional[Union[int, float]] = None,
                      is_integer: bool = False) -> Optional[ValidationError]:
        """
        Validate a numeric field
        
        Args:
            value: Value to validate
            field: Field name for the error message
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            is_integer: Whether the value must be an integer
                
        Returns:
            ValidationError if validation fails, None otherwise
        """
        if value is None:
            return None
            
        if is_integer and not isinstance(value, int):
            try:
                value = int(value)
            except (ValueError, TypeError):
                return ValidationError(field, f"Field '{field}' must be an integer")
        elif not isinstance(value, (int, float)):
            try:
                value = float(value)
            except (ValueError, TypeError):
                return ValidationError(field, f"Field '{field}' must be a number")
                
        if min_value is not None and value < min_value:
            return ValidationError(field, f"Field '{field}' must be at least {min_value}")
            
        if max_value is not None and value > max_value:
            return ValidationError(field, f"Field '{field}' must be at most {max_value}")
            
        return None
    
    @staticmethod
    def validate_boolean(value: Any, field: str) -> Optional[ValidationError]:
        """
        Validate a boolean field
        
        Args:
            value: Value to validate
            field: Field name for the error message
                
        Returns:
            ValidationError if validation fails, None otherwise
        """
        if value is None:
            return None
            
        if not isinstance(value, bool):
            # Handle string representations if needed
            if isinstance(value, str):
                value_lower = value.lower()
                if value_lower in ('true', 'false', '1', '0', 'yes', 'no'):
                    return None
                    
            return ValidationError(field, f"Field '{field}' must be a boolean")
            
        return None
    
    @staticmethod
    def validate_date(value: Any, field: str, 
                    min_date: Optional[datetime] = None, 
                    max_date: Optional[datetime] = None,
                    format: Optional[str] = None) -> Optional[ValidationError]:
        """
        Validate a date field
        
        Args:
            value: Value to validate
            field: Field name for the error message
            min_date: Minimum allowed date
            max_date: Maximum allowed date
            format: Expected date format (for string dates)
                
        Returns:
            ValidationError if validation fails, None otherwise
        """
        if value is None:
            return None
            
        if isinstance(value, str):
            try:
                if format:
                    value = datetime.strptime(value, format)
                else:
                    # Try common formats
                    for fmt in ('%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%fZ'):
                        try:
                            value = datetime.strptime(value, fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        return ValidationError(field, f"Field '{field}' has invalid date format")
            except ValueError:
                return ValidationError(field, f"Field '{field}' has invalid date format")
                
        if not isinstance(value, datetime):
            return ValidationError(field, f"Field '{field}' must be a valid date")
            
        if min_date is not None and value < min_date:
            return ValidationError(field, f"Field '{field}' must be on or after {min_date.isoformat()}")
            
        if max_date is not None and value > max_date:
            return ValidationError(field, f"Field '{field}' must be on or before {max_date.isoformat()}")
            
        return None
    
    @staticmethod
    def validate_email(value: Any, field: str) -> Optional[ValidationError]:
        """
        Validate an email field
        
        Args:
            value: Value to validate
            field: Field name for the error message
                
        Returns:
            ValidationError if validation fails, None otherwise
        """
        if value is None:
            return None
            
        result = Validator.validate_string(value, field)
        if result:
            return result
            
        if not Validator.EMAIL_PATTERN.match(value):
            return ValidationError(field, f"Field '{field}' must be a valid email address")
            
        return None
    
    @staticmethod
    def validate_url(value: Any, field: str) -> Optional[ValidationError]:
        """
        Validate a URL field
        
        Args:
            value: Value to validate
            field: Field name for the error message
                
        Returns:
            ValidationError if validation fails, None otherwise
        """
        if value is None:
            return None
            
        result = Validator.validate_string(value, field)
        if result:
            return result
            
        if not Validator.URL_PATTERN.match(value):
            return ValidationError(field, f"Field '{field}' must be a valid URL")
            
        return None
    
    @staticmethod
    def validate_phone(value: Any, field: str) -> Optional[ValidationError]:
        """
        Validate a phone number field
        
        Args:
            value: Value to validate
            field: Field name for the error message
                
        Returns:
            ValidationError if validation fails, None otherwise
        """
        if value is None:
            return None
            
        result = Validator.validate_string(value, field)
        if result:
            return result
            
        if not Validator.PHONE_PATTERN.match(value):
            return ValidationError(field, f"Field '{field}' must be a valid phone number")
            
        return None
    
    @staticmethod
    def validate_enum(value: Any, field: str, allowed_values: List[Any]) -> Optional[ValidationError]:
        """
        Validate that a value is one of a set of allowed values
        
        Args:
            value: Value to validate
            field: Field name for the error message
            allowed_values: List of allowed values
                
        Returns:
            ValidationError if validation fails, None otherwise
        """
        if value is None:
            return None
            
        if value not in allowed_values:
            values_str = ', '.join([str(v) for v in allowed_values])
            return ValidationError(field, f"Field '{field}' must be one of: {values_str}")
            
        return None
    
    @staticmethod
    def validate_array(value: Any, field: str, 
                     min_items: int = 0, 
                     max_items: Optional[int] = None,
                     item_validator: Optional[Callable[[Any, str], Optional[ValidationError]]] = None) -> ValidationResult:
        """
        Validate an array field
        
        Args:
            value: Value to validate
            field: Field name for the error message
            min_items: Minimum number of items
            max_items: Maximum number of items
            item_validator: Function to validate each item
                
        Returns:
            ValidationResult with any validation errors
        """
        result = ValidationResult()
        
        if value is None:
            return result
            
        if not isinstance(value, list):
            result.add_error(field, f"Field '{field}' must be an array")
            return result
            
        if len(value) < min_items:
            result.add_error(field, f"Field '{field}' must have at least {min_items} items")
            
        if max_items is not None and len(value) > max_items:
            result.add_error(field, f"Field '{field}' must have at most {max_items} items")
            
        if item_validator and len(value) > 0:
            for i, item in enumerate(value):
                item_field = f"{field}[{i}]"
                item_error = item_validator(item, item_field)
                if item_error:
                    result.add_error(item_error.field, item_error.message)
                    
        return result
    
    @staticmethod
    def validate_object(value: Any, field: str, schema: Dict[str, Dict[str, Any]]) -> ValidationResult:
        """
        Validate an object against a schema
        
        Args:
            value: Value to validate
            field: Field name for the error message
            schema: Schema defining the expected structure and validation rules
                
        Returns:
            ValidationResult with any validation errors
        """
        result = ValidationResult()
        
        if value is None:
            return result
            
        if not isinstance(value, dict):
            result.add_error(field, f"Field '{field}' must be an object")
            return result
            
        # Check required fields
        required_fields = [f for f, rules in schema.items() if rules.get('required', False)]
        for req_field in required_fields:
            if req_field not in value or value[req_field] is None:
                result.add_error(f"{field}.{req_field}", f"Field '{req_field}' is required")
                
        # Validate each field according to its rules
        for key, field_value in value.items():
            if key in schema:
                rules = schema[key]
                field_path = f"{field}.{key}"
                
                # Apply type-specific validation
                field_type = rules.get('type')
                
                if field_type == 'string':
                    error = Validator.validate_string(
                        field_value, 
                        field_path,
                        min_length=rules.get('min_length', 0),
                        max_length=rules.get('max_length'),
                        pattern=rules.get('pattern')
                    )
                    if error:
                        result.add_error(error.field, error.message)
                        
                elif field_type == 'number' or field_type == 'integer':
                    error = Validator.validate_number(
                        field_value,
                        field_path,
                        min_value=rules.get('min_value'),
                        max_value=rules.get('max_value'),
                        is_integer=(field_type == 'integer')
                    )
                    if error:
                        result.add_error(error.field, error.message)
                        
                elif field_type == 'boolean':
                    error = Validator.validate_boolean(field_value, field_path)
                    if error:
                        result.add_error(error.field, error.message)
                        
                elif field_type == 'date':
                    error = Validator.validate_date(
                        field_value,
                        field_path,
                        min_date=rules.get('min_date'),
                        max_date=rules.get('max_date'),
                        format=rules.get('format')
                    )
                    if error:
                        result.add_error(error.field, error.message)
                        
                elif field_type == 'email':
                    error = Validator.validate_email(field_value, field_path)
                    if error:
                        result.add_error(error.field, error.message)
                        
                elif field_type == 'url':
                    error = Validator.validate_url(field_value, field_path)
                    if error:
                        result.add_error(error.field, error.message)
                        
                elif field_type == 'phone':
                    error = Validator.validate_phone(field_value, field_path)
                    if error:
                        result.add_error(error.field, error.message)
                        
                elif field_type == 'enum':
                    error = Validator.validate_enum(
                        field_value, 
                        field_path, 
                        allowed_values=rules.get('values', [])
                    )
                    if error:
                        result.add_error(error.field, error.message)
                        
                elif field_type == 'array':
                    item_validator = None
                    if 'items' in rules:
                        item_rules = rules['items']
                        item_type = item_rules.get('type')
                        
                        # Create a validator function for the items
                        def create_item_validator(item_type, item_rules):
                            def validate_item(item, item_field):
                                if item_type == 'string':
                                    return Validator.validate_string(
                                        item, item_field, 
                                        min_length=item_rules.get('min_length', 0),
                                        max_length=item_rules.get('max_length'),
                                        pattern=item_rules.get('pattern')
                                    )
                                elif item_type == 'number' or item_type == 'integer':
                                    return Validator.validate_number(
                                        item, item_field,
                                        min_value=item_rules.get('min_value'),
                                        max_value=item_rules.get('max_value'),
                                        is_integer=(item_type == 'integer')
                                    )
                                # Add other types as needed
                                return None
                            return validate_item
                            
                        item_validator = create_item_validator(item_type, item_rules)
                        
                    array_result = Validator.validate_array(
                        field_value,
                        field_path,
                        min_items=rules.get('min_items', 0),
                        max_items=rules.get('max_items'),
                        item_validator=item_validator
                    )
                    
                    for error in array_result.errors:
                        result.add_error(error.field, error.message)
                        
                elif field_type == 'object' and 'properties' in rules:
                    # Recursive validation for nested objects
                    nested_result = Validator.validate_object(
                        field_value,
                        field_path,
                        rules['properties']
                    )
                    
                    for error in nested_result.errors:
                        result.add_error(error.field, error.message)
                        
        return result
    
    @staticmethod
    def validate_json_body(event: Dict[str, Any], schema: Dict[str, Dict[str, Any]]) -> ValidationResult:
        """
        Validate JSON body from API Gateway event
        
        Args:
            event: API Gateway event
            schema: Schema defining the expected structure and validation rules
                
        Returns:
            ValidationResult with any validation errors
        """
        result = ValidationResult()
        
        # Extract and parse body
        body = event.get('body')
        if not body:
            result.add_error('body', 'Request body is required')
            return result
            
        try:
            if isinstance(body, str):
                body = json.loads(body)
        except json.JSONDecodeError:
            result.add_error('body', 'Invalid JSON format')
            return result
            
        # Validate body against schema
        body_result = Validator.validate_object(body, 'body', schema)
        for error in body_result.errors:
            result.add_error(error.field, error.message)
            
        return result
    
    @staticmethod
    def validate_query_parameters(event: Dict[str, Any], schema: Dict[str, Dict[str, Any]]) -> ValidationResult:
        """
        Validate query parameters from API Gateway event
        
        Args:
            event: API Gateway event
            schema: Schema defining the expected structure and validation rules
                
        Returns:
            ValidationResult with any validation errors
        """
        result = ValidationResult()
        
        # Extract query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        
        # Validate query parameters against schema
        params_result = Validator.validate_object(query_params, 'queryStringParameters', schema)
        for error in params_result.errors:
            result.add_error(error.field, error.message)
            
        return result 