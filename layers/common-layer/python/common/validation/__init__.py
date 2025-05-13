"""
Validation Framework for SDIMS

This package provides a comprehensive API validation framework.
"""

from .decorator import validate_request
from .rules import (
    RequiredRule, StringRule, NumberRule, BooleanRule, EmailRule,
    DateRule, EnumRule, ArrayRule, ObjectRule, URLRule, PhoneRule
)
from .schema_validator import SchemaValidator
from .validation_error import ValidationError
from .validation_result import ValidationResult

__all__ = [
    'validate_request',
    'RequiredRule', 'StringRule', 'NumberRule', 'BooleanRule', 'EmailRule',
    'DateRule', 'EnumRule', 'ArrayRule', 'ObjectRule', 'URLRule', 'PhoneRule',
    'SchemaValidator',
    'ValidationError',
    'ValidationResult'
] 