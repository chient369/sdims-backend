"""
Unit tests for common/response.py
"""

import unittest
import json
from datetime import datetime
from decimal import Decimal
from common.response import Response

class TestResponse(unittest.TestCase):
    """Test cases for Response class"""
    
    def test_success_with_data(self):
        """Test success method with data"""
        data = {'message': 'Success', 'data': [1, 2, 3]}
        response = Response.success(data)
        
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        self.assertEqual(response['headers']['Access-Control-Allow-Origin'], '*')
        
        body = json.loads(response['body'])
        self.assertEqual(body, data)
    
    def test_success_without_data(self):
        """Test success method without data"""
        response = Response.success()
        
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        
        body = json.loads(response['body'])
        self.assertEqual(body, {})
    
    def test_success_with_custom_status(self):
        """Test success method with custom status code"""
        data = {'id': 'new-id'}
        response = Response.success(data, status_code=201)
        
        self.assertEqual(response['statusCode'], 201)
        body = json.loads(response['body'])
        self.assertEqual(body, data)
    
    def test_error_basic(self):
        """Test error method with basic parameters"""
        response = Response.error('Error message')
        
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'Error message')
        self.assertNotIn('code', body)
    
    def test_error_with_code(self):
        """Test error method with error code"""
        response = Response.error('Not found', status_code=404, error_code='E3000')
        
        self.assertEqual(response['statusCode'], 404)
        
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'Not found')
        self.assertEqual(body['code'], 'E3000')
    
    def test_error_with_details(self):
        """Test error method with details"""
        details = {'field1': ['Error 1', 'Error 2'], 'field2': ['Error 3']}
        response = Response.error('Validation error', status_code=400, error_code='E2001', details=details)
        
        self.assertEqual(response['statusCode'], 400)
        
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'Validation error')
        self.assertEqual(body['code'], 'E2001')
        self.assertEqual(body['details'], details)
    
    def test_paginated(self):
        """Test paginated method"""
        items = [{'id': 1, 'name': 'Item 1'}, {'id': 2, 'name': 'Item 2'}]
        response = Response.paginated(items, 10, 1, 2, True)
        
        self.assertEqual(response['statusCode'], 200)
        
        body = json.loads(response['body'])
        self.assertEqual(body['items'], items)
        self.assertEqual(body['pagination']['total'], 10)
        self.assertEqual(body['pagination']['page'], 1)
        self.assertEqual(body['pagination']['pageSize'], 2)
        self.assertEqual(body['pagination']['hasMore'], True)
    
    def test_paginated_with_token(self):
        """Test paginated method with next token"""
        items = [{'id': 1, 'name': 'Item 1'}, {'id': 2, 'name': 'Item 2'}]
        next_token = 'abc123'
        response = Response.paginated(items, 10, 1, 2, True, next_token=next_token)
        
        body = json.loads(response['body'])
        self.assertEqual(body['pagination']['nextToken'], next_token)
    
    def test_redirect(self):
        """Test redirect method"""
        location = 'https://example.com/new-location'
        response = Response.redirect(location)
        
        self.assertEqual(response['statusCode'], 302)
        self.assertEqual(response['headers']['Location'], location)
        self.assertEqual(response['body'], '')
    
    def test_redirect_custom_status(self):
        """Test redirect method with custom status code"""
        location = 'https://example.com/new-location'
        response = Response.redirect(location, status_code=301)
        
        self.assertEqual(response['statusCode'], 301)
        self.assertEqual(response['headers']['Location'], location)
    
    def test_binary(self):
        """Test binary method"""
        content = b'binary content'
        response = Response.binary(content)
        
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['headers']['Content-Type'], 'application/octet-stream')
        self.assertTrue(response['isBase64Encoded'])
        
        # Check that content was properly base64 encoded
        import base64
        decoded = base64.b64decode(response['body'].encode('utf-8'))
        self.assertEqual(decoded, content)
    
    def test_binary_with_content_type(self):
        """Test binary method with custom content type"""
        content = b'image content'
        response = Response.binary(content, content_type='image/jpeg')
        
        self.assertEqual(response['headers']['Content-Type'], 'image/jpeg')
    
    def test_json_serializer_decimal(self):
        """Test _json_serializer with Decimal"""
        data = {'amount': Decimal('10.5')}
        response = Response.success(data)
        
        body = json.loads(response['body'])
        self.assertEqual(body['amount'], 10.5)
        self.assertIsInstance(body['amount'], float)
        
        # Test integer conversion
        data = {'count': Decimal('10')}
        response = Response.success(data)
        
        body = json.loads(response['body'])
        self.assertEqual(body['count'], 10)
        self.assertIsInstance(body['count'], int)
    
    def test_json_serializer_datetime(self):
        """Test _json_serializer with datetime"""
        dt = datetime(2023, 1, 1, 12, 0, 0)
        data = {'timestamp': dt}
        response = Response.success(data)
        
        body = json.loads(response['body'])
        self.assertEqual(body['timestamp'], '2023-01-01T12:00:00')
    
    def test_json_serializer_custom_object(self):
        """Test _json_serializer with custom object that has to_dict method"""
        class TestObject:
            def to_dict(self):
                return {'test': 'value'}
        
        data = {'obj': TestObject()}
        response = Response.success(data)
        
        body = json.loads(response['body'])
        self.assertEqual(body['obj'], {'test': 'value'})
    
    def test_json_serializer_unsupported_type(self):
        """Test _json_serializer with unsupported type"""
        class Unsupported:
            pass
        
        data = {'obj': Unsupported()}
        with self.assertRaises(TypeError):
            Response.success(data)

if __name__ == '__main__':
    unittest.main() 