"""
Refresh token lambda function for SDIMS backend.
"""
import os
import json
from typing import Dict, Any, Optional

import boto3
from aws_lambda_powertools import Logger

from common.auth import AuthUtils, TokenType, TokenExpiredError, InvalidTokenError
from common.dynamodb import DynamoDBRepository
from common.errors import UnauthorizedError, ValidationError
from common.response import format_response, ApiError

logger = Logger(service="auth-refresh-token")

# Initialize DynamoDB repository for token blacklist
token_blacklist_repo = DynamoDBRepository()

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Refresh token handler.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response with new tokens
    """
    try:
        logger.info("Processing refresh token request")
        
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
        return refresh_user_token(refresh_token, use_token_rotation)
        
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
    except UnauthorizedError as e:
        logger.warning(f"Unauthorized: {str(e)}")
        return format_response(
            status_code=401,
            body=ApiError(
                code="E1003",
                message=str(e)
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
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        return format_response(
            status_code=500,
            body=ApiError(
                code="E5000",
                message="Đã xảy ra lỗi khi xử lý yêu cầu"
            )
        )

def refresh_user_token(refresh_token: str, use_token_rotation: bool = True) -> Dict[str, Any]:
    """
    Refresh user token using the refresh token.
    
    Args:
        refresh_token: The refresh token to use
        use_token_rotation: Whether to use token rotation strategy
        
    Returns:
        API Gateway response with new tokens
    """
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
    except (TokenExpiredError, InvalidTokenError, UnauthorizedError) as e:
        # Re-raise for consistent error handling in handler
        raise
    except Exception as e:
        logger.exception(f"Error refreshing token: {str(e)}")
        raise UnauthorizedError("Failed to refresh token")

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