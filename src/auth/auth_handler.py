"""
Combined auth handler for SDIMS backend.
This handler processes all authentication endpoints:
- /api/v1/auth/login
- /api/v1/auth/logout
- /api/v1/auth/me
- /api/v1/auth/refresh-token
"""
import os
import json
import time
from typing import Dict, Any, Optional

import boto3
from aws_lambda_powertools import Logger

from common.auth import AuthUtils, TokenType, TokenExpiredError, InvalidTokenError
from common.dynamodb import DynamoDBRepository
from common.errors import UnauthorizedError, ValidationError, ResourceNotFoundError, BadRequestError
from common.response import format_response, ApiError

logger = Logger(service="auth-service")

# Initialize DynamoDB repository
dynamodb = DynamoDBRepository()
token_blacklist_repo = DynamoDBRepository()

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main handler for all auth endpoints.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    try:
        # Get the path and HTTP method
        path = event.get('path', '')
        http_method = event.get('httpMethod', '').upper()
        
        logger.info(f"Processing auth request: {http_method} {path}")
        
        # Route to appropriate handler based on path and method
        if path.endswith('/auth/login') and http_method == 'POST':
            return handle_login(event)
        elif path.endswith('/auth/logout') and http_method == 'POST':
            return handle_logout(event)
        elif path.endswith('/auth/me') and http_method == 'GET':
            return handle_me(event)
        elif path.endswith('/auth/refresh-token') and http_method == 'POST':
            return handle_refresh_token(event)
        else:
            # If path doesn't match any of the above
            logger.warning(f"Unknown route: {http_method} {path}")
            return format_response(
                status_code=404,
                body=ApiError(
                    code="E4004",
                    message="Route not found"
                )
            )
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        return format_response(
            status_code=400,
            body=ApiError(
                code="E1000",
                message=str(e)
            )
        )
    except UnauthorizedError as e:
        logger.warning(f"Unauthorized: {str(e)}")
        return format_response(
            status_code=401,
            body=ApiError(
                code="E1003",
                message=str(e)
            )
        )
    except ResourceNotFoundError as e:
        logger.warning(f"Resource not found: {str(e)}")
        return format_response(
            status_code=404,
            body=ApiError(
                code="E4000",
                message=str(e)
            )
        )
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        return format_response(
            status_code=500,
            body=ApiError(
                code="E5000",
                message="Đã xảy ra lỗi khi xử lý yêu cầu"
            )
        )

def handle_login(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle login request
    
    Args:
        event: API Gateway event
        
    Returns:
        API Gateway response
    """
    # Parse request body
    try:
        if not event.get("body"):
            raise ValidationError("Request body is required")
            
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        logger.warning("Invalid JSON in request body")
        raise ValidationError("Invalid request format")
    
    # Get username and password from request
    username = body.get("username")
    password = body.get("password")
    remember_me = body.get("remember_me", False)
    
    if not username:
        raise ValidationError("Username is required")
    
    if not password:
        raise ValidationError("Password is required")
    
    # Get user by username or email
    user = get_user_by_username_or_email(username)
    
    if not user:
        logger.warning(f"User not found: {username}")
        return format_response(
            status_code=401,
            body=ApiError(
                code="E1005",
                message="Sai tên đăng nhập hoặc mật khẩu"
            )
        )
    
    # Check if account is active
    if not user.get('is_active', False):
        logger.warning(f"Inactive account: {username}")
        return format_response(
            status_code=401,
            body=ApiError(
                code="E1004",
                message="Tài khoản bị khóa"
            )
        )
    
    # Verify password
    if not AuthUtils.verify_password(user.get('password_hash', ''), password):
        logger.warning(f"Invalid password for user: {username}")
        return format_response(
            status_code=401,
            body=ApiError(
                code="E1005",
                message="Sai tên đăng nhập hoặc mật khẩu"
            )
        )
    
    # Get user role and permissions
    role, permissions = get_user_role_and_permissions(user['id'])
    
    # Update last login timestamp
    update_last_login(user['id'])
    
    # Create tokens
    access_expires_in = 86400 if remember_me else 3600  # 24 hours if remember_me, otherwise 1 hour
    refresh_expires_in = 30 * 86400 if remember_me else 7 * 86400  # 30 days if remember_me, otherwise 7 days
    
    tokens = AuthUtils.create_tokens(
        user_id=user['id'],
        name=user.get('full_name', ''),
        email=user.get('email', ''),
        roles=[role],
        permissions=permissions,
        access_expires_in=access_expires_in,
        refresh_expires_in=refresh_expires_in
    )
    
    # Return tokens and user info
    return format_response(
        status_code=200,
        body={
            "status": "success",
            "code": 200,
            "data": {
                "token": tokens['accessToken'],
                "refresh_token": tokens['refreshToken'],
                "token_type": "Bearer",
                "expires_in": access_expires_in,
                "user": {
                    "id": user['id'],
                    "username": user.get('username', ''),
                    "email": user.get('email', ''),
                    "fullname": user.get('full_name', ''),
                    "role": role
                }
            }
        }
    )

def handle_logout(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle logout request
    
    Args:
        event: API Gateway event
        
    Returns:
        API Gateway response
    """
    # Get authorization header
    headers = event.get('headers', {})
    authorization = headers.get('Authorization') or headers.get('authorization')
    
    if not authorization:
        logger.warning("Missing Authorization header")
        return format_response(
            status_code=200,
            body={
                "status": "success",
                "message": "Đăng xuất thành công"
            }
        )
    
    try:
        # Extract token from header
        token = AuthUtils.extract_token_from_header(authorization)
        
        # Blacklist the token
        blacklist_token(token)
        
        # Attempt to get refresh token from request body
        try:
            body = json.loads(event.get("body", "{}"))
            refresh_token = body.get("refresh_token")
            
            if refresh_token:
                # Also blacklist the refresh token if provided
                blacklist_token(refresh_token)
        except:
            # Ignore errors in processing request body
            pass
        
        return format_response(
            status_code=200,
            body={
                "status": "success",
                "message": "Đăng xuất thành công"
            }
        )
    except Exception as e:
        logger.exception(f"Error during logout: {str(e)}")
        # Still return success even if there's an error
        return format_response(
            status_code=200,
            body={
                "status": "success",
                "message": "Đăng xuất thành công"
            }
        )

def handle_me(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle me request to get current user info
    
    Args:
        event: API Gateway event
        
    Returns:
        API Gateway response
    """
    # The user claims should be available from the authorizer
    context = event.get('requestContext', {})
    authorizer = context.get('authorizer', {})
    
    # Check if claims are available
    if not authorizer:
        raise UnauthorizedError("Unauthorized")
    
    # Extract user information from claims
    user_id = authorizer.get('sub')
    
    if not user_id:
        raise UnauthorizedError("Invalid user claims")
    
    # Get user from database
    user = get_user_by_id(user_id)
    
    if not user:
        raise ResourceNotFoundError("User not found")
    
    # Get user role and permissions
    role, permissions = get_user_role_and_permissions(user_id)
    
    # Return user info
    return format_response(
        status_code=200,
        body={
            "status": "success",
            "data": {
                "user": {
                    "id": user['id'],
                    "username": user.get('username', ''),
                    "email": user.get('email', ''),
                    "fullname": user.get('full_name', ''),
                    "role": role,
                    "permissions": permissions
                }
            }
        }
    )

def handle_refresh_token(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle refresh token request
    
    Args:
        event: API Gateway event
        
    Returns:
        API Gateway response
    """
    # Parse request body
    try:
        if not event.get("body"):
            raise ValidationError("Request body is required")
            
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        logger.warning("Invalid JSON in request body")
        raise ValidationError("Invalid request format")
    
    # Get refresh token from request
    refresh_token = body.get("refreshToken")
    
    if not refresh_token:
        logger.warning("Refresh token is missing in request")
        raise ValidationError("Refresh token is required")
    
    # Use token rotation strategy
    use_token_rotation = os.environ.get("USE_TOKEN_ROTATION", "true").lower() == "true"
    
    # Refresh tokens
    try:
        # Verify refresh token
        payload = AuthUtils.verify_token(refresh_token, required_type=TokenType.REFRESH)
        
        # Check if refresh token is blacklisted
        if is_token_blacklisted(refresh_token):
            logger.warning(f"Refresh token has been revoked: {refresh_token[:10]}...")
            raise UnauthorizedError("Refresh token has been revoked")
        
        # Extract user information from payload
        user_id = payload.get('sub')
        name = payload.get('name')
        email = payload.get('email')
        roles = payload.get('roles', [])
        permissions = payload.get('permissions', [])
        
        # Access token expiration time (1 hour)
        access_expires_in = 3600
        
        # Refresh token expiration time (7 days)
        refresh_expires_in = 86400 * 7
        
        if use_token_rotation:
            # Create new access and refresh tokens
            new_tokens = AuthUtils.create_tokens(
                user_id=user_id,
                name=name,
                email=email,
                roles=roles,
                permissions=permissions,
                access_expires_in=access_expires_in,
                refresh_expires_in=refresh_expires_in
            )
            
            # Blacklist the old refresh token
            blacklist_token(refresh_token, payload.get('exp'))
            
            logger.info(f"Token refreshed with rotation for user {user_id}")
            
            # Return new tokens
            return format_response(
                status_code=200,
                body={
                    "status": "success",
                    "data": {
                        "accessToken": new_tokens['accessToken'],
                        "refreshToken": new_tokens['refreshToken'],
                        "expiresIn": access_expires_in,
                        "refreshExpiresIn": refresh_expires_in
                    }
                }
            )
        else:
            # Create only new access token
            access_token = AuthUtils.create_token(
                user_id=user_id,
                name=name, 
                email=email,
                roles=roles,
                permissions=permissions,
                token_type=TokenType.ACCESS,
                expires_in=access_expires_in
            )
            
            logger.info(f"Access token refreshed for user {user_id}")
            
            # Return new access token only
            return format_response(
                status_code=200,
                body={
                    "status": "success",
                    "data": {
                        "accessToken": access_token,
                        "expiresIn": access_expires_in
                    }
                }
            )
    except TokenExpiredError:
        logger.warning("Refresh token has expired")
        return format_response(
            status_code=401,
            body=ApiError(
                code="E1002",
                message="Refresh token đã hết hạn"
            )
        )
    except InvalidTokenError as e:
        logger.warning(f"Invalid refresh token: {str(e)}")
        return format_response(
            status_code=401,
            body=ApiError(
                code="E1001",
                message="Refresh token không hợp lệ"
            )
        )

# Helper functions used in the handlers
def get_user_by_username_or_email(username_or_email: str) -> Optional[Dict[str, Any]]:
    """
    Get user by username or email
    
    Args:
        username_or_email: Username or email
        
    Returns:
        User object or None if not found
    """
    # Try to find user by username
    result = dynamodb.query(
        key_condition_expression="PK = :pk AND begins_with(SK, :sk_prefix)",
        expression_attribute_values={
            ":pk": f"USER",
            ":sk_prefix": f"PROFILE#"
        },
        filter_expression="username = :username OR email = :email",
        expression_attribute_values={
            ":username": username_or_email,
            ":email": username_or_email
        }
    )
    
    items = result.get('Items', [])
    
    if not items:
        return None
    
    return items[0]

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get user by ID
    
    Args:
        user_id: User ID
        
    Returns:
        User object or None if not found
    """
    result = dynamodb.get_item({
        "PK": f"USER",
        "SK": f"PROFILE#{user_id}"
    })
    
    return result

def get_user_role_and_permissions(user_id: str) -> tuple:
    """
    Get user role and permissions
    
    Args:
        user_id: User ID
        
    Returns:
        Tuple of (role, permissions)
    """
    # Get user roles
    result = dynamodb.query(
        key_condition_expression="PK = :pk AND begins_with(SK, :sk_prefix)",
        expression_attribute_values={
            ":pk": f"USER#{user_id}",
            ":sk_prefix": "ROLE#"
        }
    )
    
    role_items = result.get('Items', [])
    
    if not role_items:
        return ('user', [])  # Default role and empty permissions
    
    # Assume user has one role for simplicity
    role = role_items[0].get('role', 'user')
    
    # Get permissions for the role
    result = dynamodb.query(
        key_condition_expression="PK = :pk AND begins_with(SK, :sk_prefix)",
        expression_attribute_values={
            ":pk": f"ROLE#{role}",
            ":sk_prefix": "PERMISSION#"
        }
    )
    
    permission_items = result.get('Items', [])
    permissions = [item.get('permission') for item in permission_items if item.get('permission')]
    
    return (role, permissions)

def update_last_login(user_id: str) -> None:
    """
    Update user's last login timestamp
    
    Args:
        user_id: User ID
        
    Returns:
        None
    """
    dynamodb.update_item(
        key={
            "PK": f"USER",
            "SK": f"PROFILE#{user_id}"
        },
        update_expression="SET last_login = :timestamp",
        expression_attribute_values={
            ":timestamp": int(time.time())
        }
    )

def is_token_blacklisted(token: str) -> bool:
    """
    Check if a token is blacklisted.
    
    Args:
        token: The token to check
        
    Returns:
        True if token is blacklisted, False otherwise
    """
    try:
        # Calculate a hash of the token to use as key
        token_hash = AuthUtils.generate_token_hash(token)
        
        # Check if token is in blacklist
        result = token_blacklist_repo.get_item({
            "PK": f"BLACKLIST#TOKEN",
            "SK": f"TOKEN#{token_hash}"
        })
        
        return result is not None
    except Exception as e:
        logger.error(f"Error checking token blacklist: {str(e)}")
        # In case of error, default to not blacklisted to avoid locking users out
        return False

def blacklist_token(token: str, expiry_time: Optional[int] = None) -> None:
    """
    Add a token to the blacklist.
    
    Args:
        token: The token to blacklist
        expiry_time: The timestamp when the token expires
        
    Returns:
        None
    """
    try:
        # Calculate a hash of the token to use as key
        token_hash = AuthUtils.generate_token_hash(token)
        
        # Add token to blacklist
        token_blacklist_repo.put_item({
            "PK": f"BLACKLIST#TOKEN",
            "SK": f"TOKEN#{token_hash}",
            "TokenHash": token_hash,
            "ExpiryTime": expiry_time,
            "CreatedAt": int(AuthUtils.get_current_timestamp())
        })
        
        logger.info(f"Token added to blacklist: {token_hash}")
    except Exception as e:
        logger.error(f"Error adding token to blacklist: {str(e)}")
        # Continue execution even if blacklisting fails
        pass 