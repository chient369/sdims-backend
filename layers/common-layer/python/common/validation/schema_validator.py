"""
Schema Validator

This module defines the SchemaValidator class for validating data against schemas.
"""

import json
from typing import Dict, Any, List, Optional, Union
from .validation_result import ValidationResult
from .validation_error import ValidationError
from .rules import ValidationRule

class SchemaValidator:
    """
    Class for validating data against a schema definition
    """
    
    def __init__(self, schema: Dict[str, Dict[str, Any]]):
        """
        Initialize a schema validator
        
        Args:
            schema: Schema definition
        """
        self.schema = schema
    
    def validate(self, data: Dict[str, Any], context: str = None) -> ValidationResult:
        """
        Validate data against the schema
        
        Args:
            data: Data to validate
            context: Optional context for error messages
            
        Returns:
            ValidationResult with any validation errors
        """
        result = ValidationResult()
        
        if data is None:
            result.add_error("", "Dữ liệu không hợp lệ", "INVALID_DATA")
            return result
            
        for field_name, field_rules in self.schema.items():
            field_path = f"{context}.{field_name}" if context else field_name
            
            # Skip if the field has no rules defined
            if not field_rules:
                continue
                
            # Get the value from the data
            field_value = data.get(field_name)
            
            # Validate against each rule
            for rule in field_rules:
                if isinstance(rule, ValidationRule):
                    error = rule.validate(field_value, field_path)
                    if error:
                        result.add_error(field_path, error, rule.error_code)
                        break  # Stop on first error for this field
        
        return result
    
    @classmethod
    def validate_event(cls, event: Dict[str, Any], schema: Dict[str, Dict[str, List[ValidationRule]]]) -> ValidationResult:
        """
        Validate an API Gateway event against a schema
        
        Args:
            event: API Gateway event
            schema: Schema definition with sections like 'body', 'query_string', 'path_parameters'
            
        Returns:
            ValidationResult with any validation errors
        """
        result = ValidationResult()
        
        # Validate body if schema defines it
        if 'body' in schema:
            body_schema = schema['body']
            body = cls._parse_body(event)
            
            if body_schema and body is not None:
                body_validator = cls(body_schema)
                body_result = body_validator.validate(body, 'body')
                result.merge(body_result)
        
        # Validate query string parameters if schema defines them
        if 'query_string' in schema:
            qs_schema = schema['query_string']
            qs_params = cls._get_query_string_parameters(event)
            
            if qs_schema and qs_params is not None:
                qs_validator = cls(qs_schema)
                qs_result = qs_validator.validate(qs_params, 'queryStringParameters')
                result.merge(qs_result)
        
        # Validate path parameters if schema defines them
        if 'path_parameters' in schema:
            path_schema = schema['path_parameters']
            path_params = cls._get_path_parameters(event)
            
            if path_schema and path_params is not None:
                path_validator = cls(path_schema)
                path_result = path_validator.validate(path_params, 'pathParameters')
                result.merge(path_result)
        
        # Validate headers if schema defines them
        if 'headers' in schema:
            headers_schema = schema['headers']
            headers = cls._get_headers(event)
            
            if headers_schema and headers is not None:
                headers_validator = cls(headers_schema)
                headers_result = headers_validator.validate(headers, 'headers')
                result.merge(headers_result)
        
        return result
    
    @staticmethod
    def _parse_body(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse the request body from an API Gateway event
        
        Args:
            event: API Gateway event
            
        Returns:
            Parsed body as dictionary or None
        """
        body = event.get('body')
        
        if body is None:
            return None
            
        # If body is a string, try to parse as JSON
        if isinstance(body, str):
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return None
                
        return body
    
    @staticmethod
    def _get_query_string_parameters(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get query string parameters from an API Gateway event
        
        Args:
            event: API Gateway event
            
        Returns:
            Query string parameters as dictionary or None
        """
        params = event.get('queryStringParameters')
        
        if params is None:
            return {}
            
        return params
    
    @staticmethod
    def _get_path_parameters(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get path parameters from an API Gateway event
        
        Args:
            event: API Gateway event
            
        Returns:
            Path parameters as dictionary or None
        """
        params = event.get('pathParameters')
        
        if params is None:
            return {}
            
        return params
    
    @staticmethod
    def _get_headers(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get headers from an API Gateway event
        
        Args:
            event: API Gateway event
            
        Returns:
            Headers as dictionary or None
        """
        headers = event.get('headers')
        
        if headers is None:
            return {}
            
        return headers 