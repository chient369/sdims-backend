"""
Unit tests for validation module.
"""

import pytest
from common.validation import (
    validate_schema,
    validate_required_fields,
    validate_field_type,
    validate_enum,
    validate_string_length,
    validate_numeric_range
)
from common.errors import ValidationError

def test_validate_schema():
    """Test JSON schema validation"""
    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'age': {'type': 'integer'}
        },
        'required': ['name']
    }
    
    # Valid data
    data = {'name': 'test', 'age': 25}
    validate_schema(data, schema)
    
    # Missing required field
    with pytest.raises(ValidationError) as exc:
        validate_schema({}, schema)
    assert 'required' in str(exc.value)
    
    # Invalid type
    with pytest.raises(ValidationError) as exc:
        validate_schema({'name': 'test', 'age': 'invalid'}, schema)
    assert 'integer' in str(exc.value)

def test_validate_required_fields():
    """Test required fields validation"""
    data = {'field1': 'value1', 'field2': None}
    required_fields = ['field1', 'field2', 'field3']
    
    with pytest.raises(ValidationError) as exc:
        validate_required_fields(data, required_fields)
    
    errors = exc.value.details['errors']
    assert len(errors) == 2  # field2 is None, field3 is missing
    assert any(e['field'] == 'field2' for e in errors)
    assert any(e['field'] == 'field3' for e in errors)

def test_validate_field_type():
    """Test field type validation"""
    data = {
        'string_field': 'test',
        'int_field': 123,
        'float_field': 1.23,
        'null_field': None
    }
    
    # Valid types
    validate_field_type(data, 'string_field', str)
    validate_field_type(data, 'int_field', int)
    validate_field_type(data, 'float_field', float)
    validate_field_type(data, 'null_field', str, allow_none=True)
    
    # Invalid type
    with pytest.raises(ValidationError) as exc:
        validate_field_type(data, 'int_field', str)
    assert 'Expected type' in str(exc.value)
    
    # Non-existent field (should not raise)
    validate_field_type(data, 'missing_field', str)

def test_validate_enum():
    """Test enum validation"""
    data = {'status': 'active', 'type': 'user'}
    allowed_values = ['active', 'inactive']
    
    # Valid value
    validate_enum(data, 'status', allowed_values)
    
    # Invalid value
    with pytest.raises(ValidationError) as exc:
        validate_enum(data, 'type', allowed_values)
    assert 'must be one of' in str(exc.value)
    
    # Non-existent field (should not raise)
    validate_enum(data, 'missing_field', allowed_values)

def test_validate_string_length():
    """Test string length validation"""
    data = {
        'short': 'abc',
        'long': 'abcdef',
        'null_field': None
    }
    
    # Valid length
    validate_string_length(data, 'short', min_length=2, max_length=5)
    
    # Too short
    with pytest.raises(ValidationError) as exc:
        validate_string_length(data, 'short', min_length=5)
    assert 'at least' in str(exc.value)
    
    # Too long
    with pytest.raises(ValidationError) as exc:
        validate_string_length(data, 'long', max_length=5)
    assert 'at most' in str(exc.value)
    
    # Null field (should not raise)
    validate_string_length(data, 'null_field', min_length=1)

def test_validate_numeric_range():
    """Test numeric range validation"""
    data = {
        'int_value': 5,
        'float_value': 2.5,
        'string_value': 'invalid',
        'null_field': None
    }
    
    # Valid range
    validate_numeric_range(data, 'int_value', minimum=0, maximum=10)
    validate_numeric_range(data, 'float_value', minimum=2.0, maximum=3.0)
    
    # Out of range
    with pytest.raises(ValidationError) as exc:
        validate_numeric_range(data, 'int_value', minimum=10)
    assert 'greater than' in str(exc.value)
    
    with pytest.raises(ValidationError) as exc:
        validate_numeric_range(data, 'float_value', maximum=2.0)
    assert 'less than' in str(exc.value)
    
    # Invalid type
    with pytest.raises(ValidationError) as exc:
        validate_numeric_range(data, 'string_value', minimum=0)
    assert 'numeric value' in str(exc.value)
    
    # Null field (should not raise)
    validate_numeric_range(data, 'null_field', minimum=0) 