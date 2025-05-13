"""
Validation Catalog

This module provides predefined validation schemas and rules for common use cases.
"""

from .rules import (
    RequiredRule, StringRule, NumberRule, BooleanRule, EmailRule,
    DateRule, EnumRule, ArrayRule, ObjectRule, URLRule, PhoneRule
)

class CommonValidations:
    """
    Class with common validation rules
    """
    
    # ID validations
    UUID = [StringRule(pattern=r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", message="ID không hợp lệ")]
    RESOURCE_ID = [StringRule(pattern=r"^[A-Za-z0-9-_]+$", min_length=1, max_length=50, message="ID không hợp lệ")]
    
    # Basic type validations
    STRING_SHORT = [StringRule(max_length=50)]
    STRING_MEDIUM = [StringRule(max_length=255)]
    STRING_LONG = [StringRule(max_length=1000)]
    STRING_MULTILINE = [StringRule(max_length=5000)]
    
    # Common field validations
    EMAIL = [EmailRule(message="Email không đúng định dạng")]
    PHONE = [PhoneRule(message="Số điện thoại không hợp lệ")]
    URL = [URLRule(message="URL không hợp lệ")]
    DATE = [DateRule(message="Ngày tháng không hợp lệ")]
    DATETIME = [DateRule(message="Ngày giờ không hợp lệ")]
    BOOLEAN = [BooleanRule()]
    
    # Number validations
    INTEGER = [NumberRule(is_integer=True)]
    POSITIVE_INTEGER = [NumberRule(is_integer=True, min_value=1)]
    NON_NEGATIVE_INTEGER = [NumberRule(is_integer=True, min_value=0)]
    DECIMAL = [NumberRule()]
    PERCENTAGE = [NumberRule(min_value=0, max_value=100)]
    
    # Array validations
    ARRAY = [ArrayRule()]
    NON_EMPTY_ARRAY = [ArrayRule(min_items=1)]
    
    @classmethod
    def required(cls, validation_rules=None):
        """
        Make a field required with additional validation rules
        
        Args:
            validation_rules: Additional validation rules
            
        Returns:
            List of validation rules with RequiredRule as the first rule
        """
        if validation_rules is None:
            return [RequiredRule()]
            
        return [RequiredRule()] + (validation_rules if isinstance(validation_rules, list) else [validation_rules])
    
    @classmethod
    def enum(cls, allowed_values, message=None, required=False):
        """
        Create an enum validation
        
        Args:
            allowed_values: List of allowed values
            message: Custom error message
            required: Whether the field is required
            
        Returns:
            List of validation rules
        """
        rules = [EnumRule(allowed_values, message)]
        
        if required:
            rules.insert(0, RequiredRule())
            
        return rules
    
    @classmethod
    def string(cls, min_length=None, max_length=None, pattern=None, message=None, required=False):
        """
        Create a string validation
        
        Args:
            min_length: Minimum length
            max_length: Maximum length
            pattern: Regex pattern
            message: Custom error message
            required: Whether the field is required
            
        Returns:
            List of validation rules
        """
        rules = [StringRule(min_length=min_length, max_length=max_length, pattern=pattern, message=message)]
        
        if required:
            rules.insert(0, RequiredRule())
            
        return rules
    
    @classmethod
    def number(cls, min_value=None, max_value=None, is_integer=False, message=None, required=False):
        """
        Create a number validation
        
        Args:
            min_value: Minimum value
            max_value: Maximum value
            is_integer: Whether the value must be an integer
            message: Custom error message
            required: Whether the field is required
            
        Returns:
            List of validation rules
        """
        rules = [NumberRule(min_value=min_value, max_value=max_value, is_integer=is_integer, message=message)]
        
        if required:
            rules.insert(0, RequiredRule())
            
        return rules
    
    @classmethod
    def array(cls, min_items=None, max_items=None, unique_items=False, item_validator=None, message=None, required=False):
        """
        Create an array validation
        
        Args:
            min_items: Minimum number of items
            max_items: Maximum number of items
            unique_items: Whether items must be unique
            item_validator: Validator to apply to each item
            message: Custom error message
            required: Whether the field is required
            
        Returns:
            List of validation rules
        """
        rules = [ArrayRule(min_items=min_items, max_items=max_items, unique_items=unique_items, 
                           item_validator=item_validator, message=message)]
        
        if required:
            rules.insert(0, RequiredRule())
            
        return rules
    
    @classmethod
    def object(cls, properties=None, required_properties=None, additional_properties=True, message=None, required=False):
        """
        Create an object validation
        
        Args:
            properties: Dictionary of property validators
            required_properties: List of required property names
            additional_properties: Whether additional properties are allowed
            message: Custom error message
            required: Whether the field is required
            
        Returns:
            List of validation rules
        """
        rules = [ObjectRule(properties=properties, required_properties=required_properties, 
                            additional_properties=additional_properties, message=message)]
        
        if required:
            rules.insert(0, RequiredRule())
            
        return rules

# Common Schemas
class SchemaTemplates:
    """
    Class with common schema templates
    """
    
    # Pagination parameters
    PAGINATION_PARAMS = {
        "page": CommonValidations.number(min_value=1, is_integer=True),
        "size": CommonValidations.number(min_value=1, max_value=100, is_integer=True),
        "sort": CommonValidations.string(max_length=100),
        "order": CommonValidations.enum(["asc", "desc", "ASC", "DESC"]),
    }
    
    # Date range parameters
    DATE_RANGE_PARAMS = {
        "start_date": [DateRule()],
        "end_date": [DateRule()],
    }
    
    # Simple search parameters
    SEARCH_PARAMS = {
        "q": CommonValidations.string(max_length=100),
        "fields": CommonValidations.string(max_length=255),
    }
    
    # Filter parameters
    FILTER_PARAMS = {
        "filter": CommonValidations.string(max_length=500),
    }
    
    # Email params
    EMAIL_SCHEMA = {
        "email": CommonValidations.required(CommonValidations.EMAIL),
    }
    
    # User ID params
    USER_ID_PARAMS = {
        "user_id": CommonValidations.required(CommonValidations.UUID),
    }
    
    # ID path parameter
    ID_PATH_PARAM = {
        "id": CommonValidations.required(CommonValidations.RESOURCE_ID),
    }
    
    # Boolean flag parameter
    BOOLEAN_FLAG_PARAM = {
        "flag": [BooleanRule()],
        "enabled": [BooleanRule()],
    }
    
    @classmethod
    def combine(cls, *schemas):
        """
        Combine multiple schemas into one
        
        Args:
            *schemas: Schemas to combine
            
        Returns:
            Combined schema
        """
        combined = {}
        
        for schema in schemas:
            combined.update(schema)
            
        return combined 