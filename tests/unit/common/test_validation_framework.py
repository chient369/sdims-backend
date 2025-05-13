"""
Test cases for the validation framework
"""

import pytest
import json
from datetime import datetime
from common.validation import (
    validate_request, RequiredRule, StringRule, NumberRule, 
    BooleanRule, EmailRule, DateRule, EnumRule, ArrayRule, 
    ObjectRule, URLRule, PhoneRule, SchemaValidator,
    ValidationError, ValidationResult
)
from common.errors import ValidationError as ApplicationValidationError

# Test ValidationError
def test_validation_error():
    """Test ValidationError class"""
    error = ValidationError("name", "Name is required", "REQUIRED")
    error_dict = error.to_dict()
    
    assert error.field == "name"
    assert error.message == "Name is required"
    assert error.code == "REQUIRED"
    assert error_dict["field"] == "name"
    assert error_dict["message"] == "Name is required"
    assert error_dict["code"] == "REQUIRED"
    
    # Test without code
    error = ValidationError("email", "Invalid email")
    error_dict = error.to_dict()
    
    assert error.field == "email"
    assert error.message == "Invalid email"
    assert error.code is None
    assert error_dict["field"] == "email"
    assert error_dict["message"] == "Invalid email"
    assert "code" not in error_dict

# Test ValidationResult
def test_validation_result():
    """Test ValidationResult class"""
    result = ValidationResult()
    
    assert result.is_valid == True
    assert len(result.errors) == 0
    
    # Add an error
    result.add_error("name", "Name is required", "REQUIRED")
    
    assert result.is_valid == False
    assert len(result.errors) == 1
    assert result.errors[0].field == "name"
    assert result.errors[0].message == "Name is required"
    assert result.errors[0].code == "REQUIRED"
    
    # Test to_dict
    result_dict = result.to_dict()
    
    assert result_dict["valid"] == False
    assert len(result_dict["errors"]) == 1
    assert result_dict["errors"][0]["field"] == "name"
    assert result_dict["errors"][0]["message"] == "Name is required"
    assert result_dict["errors"][0]["code"] == "REQUIRED"
    
    # Test get_error_messages
    error_messages = result.get_error_messages()
    
    assert "name" in error_messages
    assert len(error_messages["name"]) == 1
    assert error_messages["name"][0] == "Name is required"
    
    # Add another error for the same field
    result.add_error("name", "Name must be a string", "STRING")
    
    assert result.is_valid == False
    assert len(result.errors) == 2
    
    error_messages = result.get_error_messages()
    assert len(error_messages["name"]) == 2
    assert "Name is required" in error_messages["name"]
    assert "Name must be a string" in error_messages["name"]
    
    # Test get_errors_list
    errors_list = result.get_errors_list()
    
    assert len(errors_list) == 2
    assert errors_list[0]["field"] == "name"
    assert errors_list[0]["message"] == "Name is required"
    assert errors_list[0]["code"] == "REQUIRED"
    assert errors_list[1]["field"] == "name"
    assert errors_list[1]["message"] == "Name must be a string"
    assert errors_list[1]["code"] == "STRING"

# Test ValidationResult merge
def test_validation_result_merge():
    """Test ValidationResult merge method"""
    result1 = ValidationResult()
    result1.add_error("name", "Name is required", "REQUIRED")
    
    result2 = ValidationResult()
    result2.add_error("email", "Invalid email", "EMAIL")
    
    result1.merge(result2)
    
    assert result1.is_valid == False
    assert len(result1.errors) == 2
    assert result1.errors[0].field == "name"
    assert result1.errors[1].field == "email"

# Test RequiredRule
def test_required_rule():
    """Test RequiredRule validation"""
    rule = RequiredRule()
    
    # Valid cases
    assert rule.validate("Test", "name") is None
    assert rule.validate(123, "number") is None
    assert rule.validate(True, "flag") is None
    assert rule.validate([1, 2, 3], "array") is None
    assert rule.validate({"key": "value"}, "object") is None
    
    # Invalid cases
    assert rule.validate(None, "name") is not None
    assert rule.validate("", "name") is not None
    assert rule.validate("  ", "name") is not None
    assert rule.validate([], "array") is not None
    assert rule.validate({}, "object") is not None

# Test StringRule
def test_string_rule():
    """Test StringRule validation"""
    rule = StringRule(min_length=2, max_length=10)
    
    # Valid cases
    assert rule.validate("Test", "name") is None
    assert rule.validate("AB", "name") is None
    assert rule.validate("ABCDEFGHIJ", "name") is None
    
    # Invalid cases
    assert rule.validate(None, "name") is None  # None is allowed
    assert rule.validate(123, "name") is not None
    assert rule.validate("A", "name") is not None
    assert rule.validate("ABCDEFGHIJK", "name") is not None
    
    # Test with pattern
    pattern_rule = StringRule(pattern=r"^[A-Z][a-z]+$")
    
    assert pattern_rule.validate("Test", "name") is None
    assert pattern_rule.validate("Name", "name") is None
    assert pattern_rule.validate("test", "name") is not None
    assert pattern_rule.validate("123", "name") is not None
    
    # Test with enum
    enum_rule = StringRule(enum=["admin", "user", "guest"])
    
    assert enum_rule.validate("admin", "role") is None
    assert enum_rule.validate("user", "role") is None
    assert enum_rule.validate("guest", "role") is None
    assert enum_rule.validate("editor", "role") is not None

# Test NumberRule
def test_number_rule():
    """Test NumberRule validation"""
    rule = NumberRule(min_value=1, max_value=100, is_integer=True)
    
    # Valid cases
    assert rule.validate(1, "age") is None
    assert rule.validate(50, "age") is None
    assert rule.validate(100, "age") is None
    assert rule.validate("50", "age") is None  # String numbers should be converted
    
    # Invalid cases
    assert rule.validate(None, "age") is None  # None is allowed
    assert rule.validate(0, "age") is not None
    assert rule.validate(101, "age") is not None
    assert rule.validate(50.5, "age") is not None  # Not an integer
    assert rule.validate("abc", "age") is not None
    
    # Test decimal
    decimal_rule = NumberRule(min_value=0, max_value=1)
    
    assert decimal_rule.validate(0, "percentage") is None
    assert decimal_rule.validate(0.5, "percentage") is None
    assert decimal_rule.validate(1, "percentage") is None
    assert decimal_rule.validate(1.1, "percentage") is not None

# Test EmailRule
def test_email_rule():
    """Test EmailRule validation"""
    rule = EmailRule()
    
    # Valid cases
    assert rule.validate("test@example.com", "email") is None
    assert rule.validate("user.name+tag@example.co.uk", "email") is None
    
    # Invalid cases
    assert rule.validate(None, "email") is None  # None is allowed
    assert rule.validate("not-an-email", "email") is not None
    assert rule.validate("user@", "email") is not None
    assert rule.validate("user@.com", "email") is not None
    assert rule.validate(123, "email") is not None

# Test DateRule
def test_date_rule():
    """Test DateRule validation"""
    rule = DateRule()
    
    # Valid cases
    assert rule.validate("2023-01-01", "date") is None
    assert rule.validate("2023-01-01T12:00:00", "date") is None
    assert rule.validate("01/01/2023", "date") is None
    assert rule.validate(datetime.now(), "date") is None
    
    # Invalid cases
    assert rule.validate(None, "date") is None  # None is allowed
    assert rule.validate("not-a-date", "date") is not None
    assert rule.validate("2023-13-01", "date") is not None
    assert rule.validate(123, "date") is not None
    
    # Test with min/max date
    min_max_rule = DateRule(min_date="2023-01-01", max_date="2023-12-31")
    
    assert min_max_rule.validate("2023-06-15", "date") is None
    assert min_max_rule.validate("2023-01-01", "date") is None
    assert min_max_rule.validate("2023-12-31", "date") is None
    assert min_max_rule.validate("2022-12-31", "date") is not None
    assert min_max_rule.validate("2024-01-01", "date") is not None

# Test EnumRule
def test_enum_rule():
    """Test EnumRule validation"""
    rule = EnumRule(["pending", "approved", "rejected"])
    
    # Valid cases
    assert rule.validate("pending", "status") is None
    assert rule.validate("approved", "status") is None
    assert rule.validate("rejected", "status") is None
    
    # Invalid cases
    assert rule.validate(None, "status") is None  # None is allowed
    assert rule.validate("cancelled", "status") is not None
    assert rule.validate(123, "status") is not None

# Test ArrayRule
def test_array_rule():
    """Test ArrayRule validation"""
    rule = ArrayRule(min_items=1, max_items=5)
    
    # Valid cases
    assert rule.validate([1], "items") is None
    assert rule.validate([1, 2, 3], "items") is None
    assert rule.validate([1, 2, 3, 4, 5], "items") is None
    
    # Invalid cases
    assert rule.validate(None, "items") is None  # None is allowed
    assert rule.validate([], "items") is not None
    assert rule.validate([1, 2, 3, 4, 5, 6], "items") is not None
    assert rule.validate("not-an-array", "items") is not None
    
    # Test with unique items
    unique_rule = ArrayRule(unique_items=True)
    
    assert unique_rule.validate([1, 2, 3], "items") is None
    assert unique_rule.validate(["a", "b", "c"], "items") is None
    assert unique_rule.validate([1, 2, 2], "items") is not None
    assert unique_rule.validate(["a", "b", "a"], "items") is not None
    
    # Test with item validator
    item_rule = ArrayRule(item_validator=NumberRule(min_value=0))
    
    assert item_rule.validate([1, 2, 3], "items") is None
    assert item_rule.validate([0, 10, 20], "items") is None
    assert item_rule.validate([-1, 2, 3], "items") is not None
    assert item_rule.validate([1, "two", 3], "items") is not None

# Test ObjectRule
def test_object_rule():
    """Test ObjectRule validation"""
    rule = ObjectRule(
        properties={
            "name": StringRule(),
            "age": NumberRule(is_integer=True)
        },
        required_properties=["name"]
    )
    
    # Valid cases
    assert rule.validate({"name": "Test"}, "user") is None
    assert rule.validate({"name": "Test", "age": 30}, "user") is None
    assert rule.validate({"name": "Test", "age": 30, "extra": "field"}, "user") is None
    
    # Invalid cases
    assert rule.validate(None, "user") is None  # None is allowed
    assert rule.validate({}, "user") is not None
    assert rule.validate({"age": 30}, "user") is not None
    assert rule.validate({"name": 123}, "user") is not None
    assert rule.validate({"name": "Test", "age": "thirty"}, "user") is not None
    
    # Test with additional_properties=False
    strict_rule = ObjectRule(
        properties={
            "name": StringRule(),
            "age": NumberRule(is_integer=True)
        },
        required_properties=["name"],
        additional_properties=False
    )
    
    assert strict_rule.validate({"name": "Test"}, "user") is None
    assert strict_rule.validate({"name": "Test", "age": 30}, "user") is None
    assert strict_rule.validate({"name": "Test", "age": 30, "extra": "field"}, "user") is not None

# Test PhoneRule
def test_phone_rule():
    """Test PhoneRule validation"""
    rule = PhoneRule()
    
    # Valid cases
    assert rule.validate("1234567890", "phone") is None
    assert rule.validate("+1234567890", "phone") is None
    assert rule.validate("+841234567890", "phone") is None
    
    # Invalid cases
    assert rule.validate(None, "phone") is None  # None is allowed
    assert rule.validate("123", "phone") is not None
    assert rule.validate("abc", "phone") is not None
    assert rule.validate(123456789, "phone") is not None

# Test URLRule
def test_url_rule():
    """Test URLRule validation"""
    rule = URLRule()
    
    # Valid cases
    assert rule.validate("http://example.com", "url") is None
    assert rule.validate("https://example.com", "url") is None
    assert rule.validate("http://example.com/path", "url") is None
    assert rule.validate("https://example.com/path?query=value", "url") is None
    
    # Invalid cases
    assert rule.validate(None, "url") is None  # None is allowed
    assert rule.validate("example.com", "url") is not None
    assert rule.validate("ftp://example.com", "url") is not None
    assert rule.validate(123, "url") is not None

# Test SchemaValidator
def test_schema_validator():
    """Test SchemaValidator class"""
    schema = {
        "name": [RequiredRule(), StringRule(min_length=2, max_length=50)],
        "email": [RequiredRule(), EmailRule()],
        "age": [NumberRule(min_value=18, is_integer=True)],
        "role": [EnumRule(["admin", "user", "guest"])]
    }
    
    validator = SchemaValidator(schema)
    
    # Valid data
    valid_data = {
        "name": "Test User",
        "email": "test@example.com",
        "age": 30,
        "role": "user"
    }
    
    result = validator.validate(valid_data)
    assert result.is_valid == True
    
    # Invalid data
    invalid_data = {
        "name": "T",
        "email": "not-an-email",
        "age": 17,
        "role": "editor"
    }
    
    result = validator.validate(invalid_data)
    assert result.is_valid == False
    assert len(result.errors) == 4
    
    # Missing required fields
    missing_data = {
        "age": 30,
        "role": "user"
    }
    
    result = validator.validate(missing_data)
    assert result.is_valid == False
    assert len(result.errors) == 2
    
    # Test validate_event
    event = {
        "body": json.dumps({
            "name": "Test User",
            "email": "test@example.com"
        }),
        "queryStringParameters": {
            "role": "admin"
        },
        "pathParameters": {
            "id": "123"
        }
    }
    
    event_schema = {
        "body": {
            "name": [RequiredRule(), StringRule()],
            "email": [RequiredRule(), EmailRule()]
        },
        "query_string": {
            "role": [EnumRule(["admin", "user", "guest"])]
        },
        "path_parameters": {
            "id": [RequiredRule(), StringRule(pattern=r"^\d+$")]
        }
    }
    
    result = SchemaValidator.validate_event(event, event_schema)
    assert result.is_valid == True
    
    # Invalid event
    invalid_event = {
        "body": json.dumps({
            "name": "",
            "email": "not-an-email"
        }),
        "queryStringParameters": {
            "role": "editor"
        },
        "pathParameters": {
            "id": "abc"
        }
    }
    
    result = SchemaValidator.validate_event(invalid_event, event_schema)
    assert result.is_valid == False
    assert len(result.errors) > 0

# Test validate_request decorator
def test_validate_request_decorator():
    """Test validate_request decorator"""
    schema = {
        "body": {
            "name": [RequiredRule(), StringRule()],
            "email": [RequiredRule(), EmailRule()]
        }
    }
    
    # Create a mock handler function
    def mock_handler(event, context):
        return {"statusCode": 200, "body": json.dumps({"message": "Success"})}
    
    # Create a decorated handler
    decorated_handler = validate_request(schema)(mock_handler)
    
    # Create a mock context
    class MockContext:
        def __init__(self):
            self.data = {}
    
    context = MockContext()
    
    # Test with valid event
    valid_event = {
        "body": json.dumps({
            "name": "Test User",
            "email": "test@example.com"
        })
    }
    
    response = decorated_handler(valid_event, context)
    assert response["statusCode"] == 200
    
    # Test with invalid event
    invalid_event = {
        "body": json.dumps({
            "name": "",
            "email": "not-an-email"
        })
    }
    
    with pytest.raises(ApplicationValidationError):
        decorated_handler(invalid_event, context)
    
    # Test with bypass_validation
    bypass_decorated_handler = validate_request(schema, bypass_validation=True)(mock_handler)
    
    response = bypass_decorated_handler(invalid_event, context)
    assert response["statusCode"] == 200 