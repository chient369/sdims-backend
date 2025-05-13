"""
Unit tests for common/validation.py
"""

import unittest
import json
import re
from datetime import datetime, timedelta
from common.validation import Validator, ValidationResult, ValidationError

class TestValidationResult(unittest.TestCase):
    """Test cases for ValidationResult class"""
    
    def test_init(self):
        """Test initialization"""
        result = ValidationResult()
        self.assertEqual(len(result.errors), 0)
        self.assertTrue(result.is_valid)
    
    def test_add_error(self):
        """Test add_error method"""
        result = ValidationResult()
        result.add_error('field1', 'Error message')
        
        self.assertEqual(len(result.errors), 1)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, 'field1')
        self.assertEqual(result.errors[0].message, 'Error message')
    
    def test_to_dict(self):
        """Test to_dict method"""
        result = ValidationResult()
        result.add_error('field1', 'Error 1')
        result.add_error('field1', 'Error 2')
        result.add_error('field2', 'Error 3')
        
        errors_dict = result.to_dict()
        self.assertEqual(len(errors_dict), 2)
        self.assertEqual(len(errors_dict['field1']), 2)
        self.assertEqual(errors_dict['field1'][0], 'Error 1')
        self.assertEqual(errors_dict['field1'][1], 'Error 2')
        self.assertEqual(errors_dict['field2'][0], 'Error 3')

class TestValidationError(unittest.TestCase):
    """Test cases for ValidationError class"""
    
    def test_init(self):
        """Test initialization"""
        error = ValidationError('field1', 'Error message')
        self.assertEqual(error.field, 'field1')
        self.assertEqual(error.message, 'Error message')
        self.assertEqual(str(error), 'Error message')

class TestValidator(unittest.TestCase):
    """Test cases for Validator class"""
    
    def test_validate_required(self):
        """Test validate_required method"""
        # All required fields present
        data = {'field1': 'value1', 'field2': 'value2', 'field3': 0}
        result = Validator.validate_required(data, ['field1', 'field2', 'field3'])
        self.assertTrue(result.is_valid)
        
        # Missing fields
        data = {'field1': 'value1'}
        result = Validator.validate_required(data, ['field1', 'field2', 'field3'])
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 2)
        
        # None value
        data = {'field1': 'value1', 'field2': None}
        result = Validator.validate_required(data, ['field1', 'field2'])
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].field, 'field2')
    
    def test_validate_string(self):
        """Test validate_string method"""
        # Valid string
        error = Validator.validate_string('test', 'field1')
        self.assertIsNone(error)
        
        # None value (skipped validation)
        error = Validator.validate_string(None, 'field1')
        self.assertIsNone(error)
        
        # Not a string
        error = Validator.validate_string(123, 'field1')
        self.assertIsNotNone(error)
        self.assertEqual(error.field, 'field1')
        
        # String too short
        error = Validator.validate_string('ab', 'field1', min_length=3)
        self.assertIsNotNone(error)
        
        # String too long
        error = Validator.validate_string('abcdef', 'field1', max_length=5)
        self.assertIsNotNone(error)
        
        # String matches pattern
        error = Validator.validate_string('abc123', 'field1', pattern=r'^[a-z0-9]+$')
        self.assertIsNone(error)
        
        # String doesn't match pattern
        error = Validator.validate_string('abc-123', 'field1', pattern=r'^[a-z0-9]+$')
        self.assertIsNotNone(error)
        
        # Pattern as compiled regex
        pattern = re.compile(r'^[a-z0-9]+$')
        error = Validator.validate_string('abc123', 'field1', pattern=pattern)
        self.assertIsNone(error)
    
    def test_validate_number(self):
        """Test validate_number method"""
        # Valid number
        error = Validator.validate_number(123, 'field1')
        self.assertIsNone(error)
        
        error = Validator.validate_number(123.45, 'field1')
        self.assertIsNone(error)
        
        # None value (skipped validation)
        error = Validator.validate_number(None, 'field1')
        self.assertIsNone(error)
        
        # Not a number
        error = Validator.validate_number('abc', 'field1')
        self.assertIsNotNone(error)
        
        # Number convertible to int
        error = Validator.validate_number('123', 'field1', is_integer=True)
        self.assertIsNone(error)
        
        # Number convertible to float
        error = Validator.validate_number('123.45', 'field1')
        self.assertIsNone(error)
        
        # Float not convertible to int
        error = Validator.validate_number('123.45', 'field1', is_integer=True)
        self.assertIsNotNone(error)
        
        # Number too small
        error = Validator.validate_number(5, 'field1', min_value=10)
        self.assertIsNotNone(error)
        
        # Number too large
        error = Validator.validate_number(15, 'field1', max_value=10)
        self.assertIsNotNone(error)
    
    def test_validate_email(self):
        """Test validate_email method"""
        # Valid email
        error = Validator.validate_email('user@example.com', 'email')
        self.assertIsNone(error)
        
        # None value (skipped validation)
        error = Validator.validate_email(None, 'email')
        self.assertIsNone(error)
        
        # Not a string
        error = Validator.validate_email(123, 'email')
        self.assertIsNotNone(error)
        
        # Invalid email format
        error = Validator.validate_email('notanemail', 'email')
        self.assertIsNotNone(error)
        
        error = Validator.validate_email('user@', 'email')
        self.assertIsNotNone(error)
        
        error = Validator.validate_email('@example.com', 'email')
        self.assertIsNotNone(error)
    
    def test_validate_array(self):
        """Test validate_array method"""
        # Valid array
        result = Validator.validate_array([1, 2, 3], 'items')
        self.assertTrue(result.is_valid)
        
        # None value (skipped validation)
        result = Validator.validate_array(None, 'items')
        self.assertTrue(result.is_valid)
        
        # Not an array
        result = Validator.validate_array('not_an_array', 'items')
        self.assertFalse(result.is_valid)
        
        # Array too short
        result = Validator.validate_array([1], 'items', min_items=2)
        self.assertFalse(result.is_valid)
        
        # Array too long
        result = Validator.validate_array([1, 2, 3], 'items', max_items=2)
        self.assertFalse(result.is_valid)
        
        # Array with item validator
        def validate_positive(item, field):
            if item <= 0:
                return ValidationError(field, "Value must be positive")
            return None
            
        result = Validator.validate_array([1, 2, 3], 'items', item_validator=validate_positive)
        self.assertTrue(result.is_valid)
        
        result = Validator.validate_array([1, -2, 3], 'items', item_validator=validate_positive)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, 'items[1]')
    
    def test_validate_object(self):
        """Test validate_object method"""
        # Schema definition
        schema = {
            'name': {
                'type': 'string',
                'required': True,
                'min_length': 2,
                'max_length': 50
            },
            'age': {
                'type': 'integer',
                'required': True,
                'min_value': 0,
                'max_value': 120
            },
            'email': {
                'type': 'email',
                'required': True
            },
            'tags': {
                'type': 'array',
                'min_items': 1,
                'items': {
                    'type': 'string'
                }
            }
        }
        
        # Valid object
        valid_obj = {
            'name': 'John Doe',
            'age': 30,
            'email': 'john@example.com',
            'tags': ['tag1', 'tag2']
        }
        result = Validator.validate_object(valid_obj, 'user', schema)
        self.assertTrue(result.is_valid)
        
        # None value (skipped validation)
        result = Validator.validate_object(None, 'user', schema)
        self.assertTrue(result.is_valid)
        
        # Not an object
        result = Validator.validate_object('not_an_object', 'user', schema)
        self.assertFalse(result.is_valid)
        
        # Missing required fields
        invalid_obj = {
            'name': 'John Doe'
        }
        result = Validator.validate_object(invalid_obj, 'user', schema)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 2)  # Missing age and email
        
        # Invalid field values
        invalid_obj = {
            'name': 'J',  # Too short
            'age': 150,   # Too high
            'email': 'not-an-email',
            'tags': []    # Empty array
        }
        result = Validator.validate_object(invalid_obj, 'user', schema)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 4)
    
    def test_validate_json_body(self):
        """Test validate_json_body method"""
        # Schema definition
        schema = {
            'name': {
                'type': 'string',
                'required': True
            },
            'age': {
                'type': 'integer',
                'required': True
            }
        }
        
        # Valid body
        event = {
            'body': json.dumps({
                'name': 'John Doe',
                'age': 30
            })
        }
        result = Validator.validate_json_body(event, schema)
        self.assertTrue(result.is_valid)
        
        # Missing body
        event = {}
        result = Validator.validate_json_body(event, schema)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, 'body')
        
        # Invalid JSON
        event = {
            'body': 'not-json'
        }
        result = Validator.validate_json_body(event, schema)
        self.assertFalse(result.is_valid)
        
        # Invalid data
        event = {
            'body': json.dumps({
                'name': 'John Doe'
                # Missing age
            })
        }
        result = Validator.validate_json_body(event, schema)
        self.assertFalse(result.is_valid)
    
    def test_validate_query_parameters(self):
        """Test validate_query_parameters method"""
        # Schema definition
        schema = {
            'page': {
                'type': 'integer',
                'required': True,
                'min_value': 1
            },
            'limit': {
                'type': 'integer',
                'required': True,
                'min_value': 1,
                'max_value': 100
            }
        }
        
        # Valid query parameters
        event = {
            'queryStringParameters': {
                'page': '1',
                'limit': '10'
            }
        }
        result = Validator.validate_query_parameters(event, schema)
        self.assertTrue(result.is_valid)
        
        # Missing parameters
        event = {
            'queryStringParameters': {
                'page': '1'
                # Missing limit
            }
        }
        result = Validator.validate_query_parameters(event, schema)
        self.assertFalse(result.is_valid)
        
        # Invalid parameters
        event = {
            'queryStringParameters': {
                'page': '0',  # Less than min_value
                'limit': '200'  # Greater than max_value
            }
        }
        result = Validator.validate_query_parameters(event, schema)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 2)

if __name__ == '__main__':
    unittest.main() 