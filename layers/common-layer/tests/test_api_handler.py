"""
Unit tests for API handler module.
"""

import json
import pytest
from common.api.api_handler import RequestContext, APIResponse, api_handler
from common.errors import ValidationError, APIError

def test_request_context():
    """Test RequestContext initialization"""
    event = {
        'httpMethod': 'GET',
        'path': '/test',
        'headers': {'Content-Type': 'application/json'},
        'queryStringParameters': {'param': 'value'},
        'pathParameters': {'id': '123'}
    }
    context = type('LambdaContext', (), {'aws_request_id': '123'})()
    
    req_context = RequestContext(
        event=event,
        context=context,
        path_params={'id': '123'},
        query_params={'param': 'value'},
        headers={'Content-Type': 'application/json'}
    )
    
    assert req_context.method == 'GET'
    assert req_context.path == '/test'
    assert req_context.get_header('Content-Type') == 'application/json'
    assert req_context.path_params == {'id': '123'}
    assert req_context.query_params == {'param': 'value'}

def test_api_response():
    """Test APIResponse formatting"""
    response = APIResponse(
        status_code=200,
        body={'message': 'success'},
        headers={'Custom-Header': 'value'}
    )
    
    result = response.to_dict()
    assert result['statusCode'] == 200
    assert json.loads(result['body']) == {'message': 'success'}
    assert result['headers']['Custom-Header'] == 'value'
    assert result['headers']['Content-Type'] == 'application/json'

def test_api_handler_decorator():
    """Test api_handler decorator"""
    schema = {
        'type': 'object',
        'properties': {
            'body': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'}
                },
                'required': ['name']
            }
        }
    }
    
    @api_handler(schema=schema)
    def handler(request_context):
        return {'message': 'success'}
        
    # Test successful request
    event = {
        'body': json.dumps({'name': 'test'}),
        'headers': {}
    }
    context = type('LambdaContext', (), {'aws_request_id': '123'})()
    
    result = handler(event, context)
    assert result['statusCode'] == 200
    assert json.loads(result['body'])['message'] == 'success'
    
    # Test validation error
    event['body'] = json.dumps({})
    result = handler(event, context)
    assert result['statusCode'] == 400
    assert json.loads(result['body'])['code'] == 'E2000'

def test_error_handling():
    """Test error handling in api_handler"""
    @api_handler()
    def handler(request_context):
        raise APIError('E1001', 'Test error', 401)
        
    event = {'headers': {}}
    context = type('LambdaContext', (), {'aws_request_id': '123'})()
    
    result = handler(event, context)
    assert result['statusCode'] == 401
    body = json.loads(result['body'])
    assert body['code'] == 'E1001'
    assert body['message'] == 'Test error' 