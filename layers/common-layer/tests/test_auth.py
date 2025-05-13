"""
Unit tests for auth module.
"""

import time
import pytest
import jwt
from common.auth import (
    verify_token,
    generate_token,
    check_permission,
    AuthUtils
)
from common.errors import AuthenticationError, AuthorizationError

def test_verify_token():
    """Test token verification"""
    secret_key = 'test_secret'
    payload = {
        'sub': 'user123',
        'permissions': ['read', 'write'],
        'exp': int(time.time()) + 3600
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    # Valid token
    result = verify_token(token, secret_key)
    assert result['sub'] == 'user123'
    assert 'read' in result['permissions']
    
    # Invalid token
    with pytest.raises(AuthenticationError):
        verify_token('invalid_token', secret_key)
        
    # Expired token
    expired_payload = payload.copy()
    expired_payload['exp'] = int(time.time()) - 3600
    expired_token = jwt.encode(expired_payload, secret_key, algorithm='HS256')
    
    with pytest.raises(AuthenticationError) as exc:
        verify_token(expired_token, secret_key)
    assert 'expired' in str(exc.value)

def test_generate_token():
    """Test token generation"""
    secret_key = 'test_secret'
    user_id = 'user123'
    permissions = ['read', 'write']
    expiry = 3600
    
    token = generate_token(user_id, permissions, secret_key, expiry)
    payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    
    assert payload['sub'] == user_id
    assert payload['permissions'] == permissions
    assert payload['exp'] - payload['iat'] == expiry

def test_check_permission():
    """Test permission checking"""
    user_permissions = ['users:read', 'users:write', 'admin:*']
    
    # Direct match
    check_permission('users:read', user_permissions)
    
    # Wildcard match
    check_permission('admin:create', user_permissions)
    
    # Missing permission
    with pytest.raises(AuthorizationError) as exc:
        check_permission('projects:read', user_permissions)
    assert 'Missing required permission' in str(exc.value)

def test_auth_utils():
    """Test AuthUtils class"""
    # Test password hashing
    password = 'test_password'
    hashed = AuthUtils.generate_password_hash(password)
    assert AuthUtils.verify_password(hashed, password)
    assert not AuthUtils.verify_password(hashed, 'wrong_password')
    
    # Test permission checking
    user_permissions = ['users:read', 'users:write', 'admin:*']
    
    assert AuthUtils.check_permission(user_permissions, 'users:read')
    assert AuthUtils.check_permission(user_permissions, 'admin:create')  # Wildcard match
    assert not AuthUtils.check_permission(user_permissions, 'projects:read')
    
    # Test role checking
    user_roles = ['user', 'editor']
    assert AuthUtils.has_role(user_roles, 'editor')
    assert AuthUtils.has_role(user_roles, ['admin', 'editor'])
    assert not AuthUtils.has_role(user_roles, 'admin')
    
    # Test token extraction
    valid_header = 'Bearer test_token'
    assert AuthUtils.extract_token_from_header(valid_header) == 'test_token'
    
    with pytest.raises(AuthenticationError):
        AuthUtils.extract_token_from_header(None)
        
    with pytest.raises(AuthenticationError):
        AuthUtils.extract_token_from_header('Invalid format') 