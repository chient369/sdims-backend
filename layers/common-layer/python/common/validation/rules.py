"""
Validation Rules

This module defines validation rules used in the validation framework.
"""

import re
from typing import Any, Dict, List, Optional, Pattern, Union, Callable
from datetime import datetime
from decimal import Decimal

class ValidationRule:
    """Base class for all validation rules"""
    
    def __init__(self):
        self.error_message = "Validation failed"
        self.error_code = None
    
    def validate(self, value: Any, field: str) -> Optional[str]:
        """
        Validate a value against this rule
        
        Args:
            value: The value to validate
            field: The field name being validated
            
        Returns:
            None if validation passes, error message otherwise
        """
        raise NotImplementedError("Subclasses must implement validate method")

class RequiredRule(ValidationRule):
    """Rule that requires a value to be present"""
    
    def __init__(self, message: str = None):
        """
        Initialize a required rule
        
        Args:
            message: Custom error message
        """
        super().__init__()
        self.error_message = message or "Trường này là bắt buộc"
        self.error_code = "REQUIRED"
    
    def validate(self, value: Any, field: str) -> Optional[str]:
        """
        Validate that a value is not None or empty
        
        Args:
            value: The value to validate
            field: The field name being validated
            
        Returns:
            None if validation passes, error message otherwise
        """
        if value is None:
            return self.error_message
            
        if isinstance(value, str) and value.strip() == "":
            return self.error_message
            
        if isinstance(value, (list, dict)) and len(value) == 0:
            return self.error_message
            
        return None

class StringRule(ValidationRule):
    """Rule for validating strings"""
    
    def __init__(self, 
                 min_length: int = None, 
                 max_length: int = None, 
                 pattern: Union[str, Pattern] = None,
                 enum: List[str] = None,
                 message: str = None):
        """
        Initialize a string rule
        
        Args:
            min_length: Minimum length
            max_length: Maximum length
            pattern: Regex pattern
            enum: List of allowed values
            message: Custom error message
        """
        super().__init__()
        self.min_length = min_length
        self.max_length = max_length
        
        if pattern and isinstance(pattern, str):
            self.pattern = re.compile(pattern)
        else:
            self.pattern = pattern
            
        self.enum = enum
        self.error_message = message
        self.error_code = "STRING"
    
    def validate(self, value: Any, field: str) -> Optional[str]:
        """
        Validate a string value
        
        Args:
            value: The value to validate
            field: The field name being validated
            
        Returns:
            None if validation passes, error message otherwise
        """
        if value is None:
            return None
            
        if not isinstance(value, str):
            return self.error_message or f"Trường '{field}' phải là chuỗi"
            
        if self.min_length is not None and len(value) < self.min_length:
            return self.error_message or f"Trường '{field}' phải có ít nhất {self.min_length} ký tự"
            
        if self.max_length is not None and len(value) > self.max_length:
            return self.error_message or f"Trường '{field}' không được vượt quá {self.max_length} ký tự"
            
        if self.pattern and not self.pattern.match(value):
            return self.error_message or f"Trường '{field}' không đúng định dạng"
            
        if self.enum and value not in self.enum:
            enum_str = ", ".join(self.enum)
            return self.error_message or f"Trường '{field}' phải là một trong các giá trị: {enum_str}"
            
        return None

class NumberRule(ValidationRule):
    """Rule for validating numbers"""
    
    def __init__(self, 
                 min_value: Union[int, float] = None, 
                 max_value: Union[int, float] = None, 
                 is_integer: bool = False,
                 message: str = None):
        """
        Initialize a number rule
        
        Args:
            min_value: Minimum value
            max_value: Maximum value
            is_integer: Whether the value must be an integer
            message: Custom error message
        """
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value
        self.is_integer = is_integer
        self.error_message = message
        self.error_code = "NUMBER"
    
    def validate(self, value: Any, field: str) -> Optional[str]:
        """
        Validate a numeric value
        
        Args:
            value: The value to validate
            field: The field name being validated
            
        Returns:
            None if validation passes, error message otherwise
        """
        if value is None:
            return None
            
        # Convert to number if string
        if isinstance(value, str):
            try:
                if self.is_integer:
                    value = int(value)
                else:
                    value = float(value)
            except (ValueError, TypeError):
                return self.error_message or f"Trường '{field}' phải là số"
        
        # Handle Decimal type
        if isinstance(value, Decimal):
            if self.is_integer and value % 1 != 0:
                return self.error_message or f"Trường '{field}' phải là số nguyên"
            value = float(value)
            
        if self.is_integer and not isinstance(value, int):
            if isinstance(value, float) and value.is_integer():
                # Float with zero decimal part, acceptable as integer
                value = int(value)
            else:
                return self.error_message or f"Trường '{field}' phải là số nguyên"
                
        if not isinstance(value, (int, float)):
            return self.error_message or f"Trường '{field}' phải là số"
            
        if self.min_value is not None and value < self.min_value:
            return self.error_message or f"Trường '{field}' phải lớn hơn hoặc bằng {self.min_value}"
            
        if self.max_value is not None and value > self.max_value:
            return self.error_message or f"Trường '{field}' phải nhỏ hơn hoặc bằng {self.max_value}"
            
        return None

class BooleanRule(ValidationRule):
    """Rule for validating booleans"""
    
    def __init__(self, message: str = None):
        """
        Initialize a boolean rule
        
        Args:
            message: Custom error message
        """
        super().__init__()
        self.error_message = message
        self.error_code = "BOOLEAN"
    
    def validate(self, value: Any, field: str) -> Optional[str]:
        """
        Validate a boolean value
        
        Args:
            value: The value to validate
            field: The field name being validated
            
        Returns:
            None if validation passes, error message otherwise
        """
        if value is None:
            return None
            
        if isinstance(value, bool):
            return None
            
        # Handle string representations
        if isinstance(value, str):
            value_lower = value.lower()
            if value_lower in ('true', 'false', '1', '0', 'yes', 'no'):
                return None
                
        return self.error_message or f"Trường '{field}' phải là giá trị boolean"

class DateRule(ValidationRule):
    """Rule for validating dates"""
    
    def __init__(self, 
                 min_date: Union[datetime, str] = None, 
                 max_date: Union[datetime, str] = None, 
                 format: str = None,
                 message: str = None):
        """
        Initialize a date rule
        
        Args:
            min_date: Minimum date
            max_date: Maximum date
            format: Expected date format
            message: Custom error message
        """
        super().__init__()
        self.format = format
        self.error_message = message
        self.error_code = "DATE"
        
        # Convert string dates to datetime objects
        if min_date and isinstance(min_date, str):
            try:
                self.min_date = datetime.fromisoformat(min_date.replace('Z', '+00:00'))
            except ValueError:
                if format:
                    self.min_date = datetime.strptime(min_date, format)
                else:
                    raise ValueError(f"Invalid min_date format: {min_date}")
        else:
            self.min_date = min_date
            
        if max_date and isinstance(max_date, str):
            try:
                self.max_date = datetime.fromisoformat(max_date.replace('Z', '+00:00'))
            except ValueError:
                if format:
                    self.max_date = datetime.strptime(max_date, format)
                else:
                    raise ValueError(f"Invalid max_date format: {max_date}")
        else:
            self.max_date = max_date
    
    def validate(self, value: Any, field: str) -> Optional[str]:
        """
        Validate a date value
        
        Args:
            value: The value to validate
            field: The field name being validated
            
        Returns:
            None if validation passes, error message otherwise
        """
        if value is None:
            return None
            
        # Convert value to datetime
        if isinstance(value, str):
            try:
                if self.format:
                    date_value = datetime.strptime(value, self.format)
                else:
                    # Try common formats
                    try:
                        date_value = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except ValueError:
                        # Try other common formats
                        formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d']
                        for fmt in formats:
                            try:
                                date_value = datetime.strptime(value, fmt)
                                break
                            except ValueError:
                                continue
                        else:
                            return self.error_message or f"Trường '{field}' không đúng định dạng ngày tháng"
            except ValueError:
                return self.error_message or f"Trường '{field}' không đúng định dạng ngày tháng"
        elif isinstance(value, datetime):
            date_value = value
        else:
            return self.error_message or f"Trường '{field}' phải là ngày tháng"
            
        if self.min_date and date_value < self.min_date:
            min_date_str = self.min_date.strftime('%Y-%m-%d') if self.min_date else ""
            return self.error_message or f"Trường '{field}' phải sau hoặc bằng ngày {min_date_str}"
            
        if self.max_date and date_value > self.max_date:
            max_date_str = self.max_date.strftime('%Y-%m-%d') if self.max_date else ""
            return self.error_message or f"Trường '{field}' phải trước hoặc bằng ngày {max_date_str}"
            
        return None

class EnumRule(ValidationRule):
    """Rule for validating against an enumeration of values"""
    
    def __init__(self, allowed_values: List[Any], message: str = None):
        """
        Initialize an enum rule
        
        Args:
            allowed_values: List of allowed values
            message: Custom error message
        """
        super().__init__()
        self.allowed_values = allowed_values
        self.error_message = message
        self.error_code = "ENUM"
    
    def validate(self, value: Any, field: str) -> Optional[str]:
        """
        Validate that a value is in the allowed list
        
        Args:
            value: The value to validate
            field: The field name being validated
            
        Returns:
            None if validation passes, error message otherwise
        """
        if value is None:
            return None
            
        if value not in self.allowed_values:
            values_str = ", ".join(str(v) for v in self.allowed_values)
            return self.error_message or f"Trường '{field}' phải là một trong các giá trị: {values_str}"
            
        return None

class ArrayRule(ValidationRule):
    """Rule for validating arrays/lists"""
    
    def __init__(self, 
                 min_items: int = None, 
                 max_items: int = None, 
                 unique_items: bool = False,
                 item_validator: Union[ValidationRule, List[ValidationRule]] = None,
                 message: str = None):
        """
        Initialize an array rule
        
        Args:
            min_items: Minimum number of items
            max_items: Maximum number of items
            unique_items: Whether items must be unique
            item_validator: Validator to apply to each item
            message: Custom error message
        """
        super().__init__()
        self.min_items = min_items
        self.max_items = max_items
        self.unique_items = unique_items
        self.item_validator = item_validator
        self.error_message = message
        self.error_code = "ARRAY"
    
    def validate(self, value: Any, field: str) -> Optional[str]:
        """
        Validate an array value
        
        Args:
            value: The value to validate
            field: The field name being validated
            
        Returns:
            None if validation passes, error message otherwise
        """
        if value is None:
            return None
            
        if not isinstance(value, (list, tuple)):
            return self.error_message or f"Trường '{field}' phải là mảng"
            
        if self.min_items is not None and len(value) < self.min_items:
            return self.error_message or f"Trường '{field}' phải có ít nhất {self.min_items} phần tử"
            
        if self.max_items is not None and len(value) > self.max_items:
            return self.error_message or f"Trường '{field}' không được vượt quá {self.max_items} phần tử"
            
        if self.unique_items and len(value) != len(set(str(x) for x in value)):
            return self.error_message or f"Trường '{field}' không được chứa các phần tử trùng lặp"
            
        # Validate each item
        if self.item_validator:
            validators = self.item_validator if isinstance(self.item_validator, list) else [self.item_validator]
            
            for i, item in enumerate(value):
                for validator in validators:
                    error = validator.validate(item, f"{field}[{i}]")
                    if error:
                        return error
            
        return None

class ObjectRule(ValidationRule):
    """Rule for validating objects/dictionaries"""
    
    def __init__(self, 
                 properties: Dict[str, Union[ValidationRule, List[ValidationRule]]] = None,
                 required_properties: List[str] = None,
                 additional_properties: bool = True,
                 message: str = None):
        """
        Initialize an object rule
        
        Args:
            properties: Dictionary of property validators
            required_properties: List of required property names
            additional_properties: Whether additional properties are allowed
            message: Custom error message
        """
        super().__init__()
        self.properties = properties or {}
        self.required_properties = required_properties or []
        self.additional_properties = additional_properties
        self.error_message = message
        self.error_code = "OBJECT"
    
    def validate(self, value: Any, field: str) -> Optional[str]:
        """
        Validate an object value
        
        Args:
            value: The value to validate
            field: The field name being validated
            
        Returns:
            None if validation passes, error message otherwise
        """
        if value is None:
            return None
            
        if not isinstance(value, dict):
            return self.error_message or f"Trường '{field}' phải là đối tượng"
            
        # Check required properties
        for prop in self.required_properties:
            if prop not in value or value[prop] is None:
                return self.error_message or f"Thuộc tính '{prop}' là bắt buộc trong '{field}'"
                
        # Check additional properties
        if not self.additional_properties:
            extra_props = set(value.keys()) - set(self.properties.keys())
            if extra_props:
                props_str = ", ".join(extra_props)
                return self.error_message or f"Thuộc tính không được phép: {props_str} trong '{field}'"
                
        # Validate each property
        for prop_name, prop_value in value.items():
            if prop_name in self.properties:
                validators = self.properties[prop_name]
                validators = validators if isinstance(validators, list) else [validators]
                
                for validator in validators:
                    error = validator.validate(prop_value, f"{field}.{prop_name}")
                    if error:
                        return error
            
        return None

class EmailRule(ValidationRule):
    """Rule for validating email addresses"""
    
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")
    
    def __init__(self, message: str = None):
        """
        Initialize an email rule
        
        Args:
            message: Custom error message
        """
        super().__init__()
        self.error_message = message
        self.error_code = "EMAIL"
    
    def validate(self, value: Any, field: str) -> Optional[str]:
        """
        Validate an email address
        
        Args:
            value: The value to validate
            field: The field name being validated
            
        Returns:
            None if validation passes, error message otherwise
        """
        if value is None:
            return None
            
        if not isinstance(value, str):
            return self.error_message or f"Trường '{field}' phải là chuỗi"
            
        if not self.EMAIL_PATTERN.match(value):
            return self.error_message or f"Trường '{field}' không đúng định dạng email"
            
        return None

class URLRule(ValidationRule):
    """Rule for validating URLs"""
    
    URL_PATTERN = re.compile(r"^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(/[-\w%.]+)*(?:\?\S+)?$")
    
    def __init__(self, message: str = None):
        """
        Initialize a URL rule
        
        Args:
            message: Custom error message
        """
        super().__init__()
        self.error_message = message
        self.error_code = "URL"
    
    def validate(self, value: Any, field: str) -> Optional[str]:
        """
        Validate a URL
        
        Args:
            value: The value to validate
            field: The field name being validated
            
        Returns:
            None if validation passes, error message otherwise
        """
        if value is None:
            return None
            
        if not isinstance(value, str):
            return self.error_message or f"Trường '{field}' phải là chuỗi"
            
        if not self.URL_PATTERN.match(value):
            return self.error_message or f"Trường '{field}' không đúng định dạng URL"
            
        return None

class PhoneRule(ValidationRule):
    """Rule for validating phone numbers"""
    
    PHONE_PATTERN = re.compile(r"^\+?[0-9]{10,15}$")
    
    def __init__(self, message: str = None):
        """
        Initialize a phone rule
        
        Args:
            message: Custom error message
        """
        super().__init__()
        self.error_message = message
        self.error_code = "PHONE"
    
    def validate(self, value: Any, field: str) -> Optional[str]:
        """
        Validate a phone number
        
        Args:
            value: The value to validate
            field: The field name being validated
            
        Returns:
            None if validation passes, error message otherwise
        """
        if value is None:
            return None
            
        if not isinstance(value, str):
            return self.error_message or f"Trường '{field}' phải là chuỗi"
            
        if not self.PHONE_PATTERN.match(value):
            return self.error_message or f"Trường '{field}' không đúng định dạng số điện thoại"
            
        return None 