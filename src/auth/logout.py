"""
Logout lambda function for SDIMS backend.

Handles user logout and token blacklisting.
"""
import os
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from aws_lambda_powertools import Logger
from boto3.dynamodb.conditions import Key

from common.dynamodb import DynamoDBRepository
from common.errors import UnauthorizedError, ValidationError, handle_lambda_error
from common.response import format_response

logger = Logger(service="auth-logout")

# Environment variables
JWT_SECRET = os.environ.get("JWT_SECRET", "your-secret-key")  # In production, use AWS Secrets Manager
TABLE_NAME = os.environ.get("TABLE_NAME")

# Initialize DynamoDB repository
dynamodb_repo = DynamoDBRepository(table_name=TABLE_NAME)

# Constants
TOKEN_BLACKLIST_PK_PREFIX = "TOKEN_BLACKLIST"
TOKEN_BLACKLIST_SK_PREFIX = "TOKEN"


def _extract_token(event: Dict[str, Any]) -> str:
    """
    Extract JWT token from request.
    
    Args:
        event: API Gateway event
        
    Returns:
        JWT token string
        
    Raises:
        UnauthorizedError: If token is missing or invalid
    """
    authorization_header = event.get("headers", {}).get("Authorization")
    
    if not authorization_header:
        logger.warning("Missing Authorization header")
        raise UnauthorizedError("Missing Authorization header")
    
    parts = authorization_header.split()
    
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.warning("Invalid Authorization header format")
        raise UnauthorizedError("Authorization header must be in format: Bearer <token>")
    
    return parts[1]


def _get_token_jti(token: str) -> str:
    """
    Generate a unique identifier for the token.
    Since we don't have jti in our token, we use a hash of the token as the identifier.
    
    Args:
        token: JWT token
        
    Returns:
        Token JTI (unique identifier)
    """
    import hashlib
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


def _add_token_to_blacklist(token: str, token_jti: str, expires_at: Optional[int] = None) -> None:
    """
    Add token to blacklist in DynamoDB.
    
    Args:
        token: JWT token
        token_jti: Token unique identifier
        expires_at: Timestamp when token expires (epoch seconds)
    
    Returns:
        None
    """
    if not expires_at:
        # If expiration time not provided, default to 24 hours
        expires_at = int(time.time()) + 86400  # 24 hours in seconds
    
    # Create item for blacklisted token
    item = {
        "PK": f"{TOKEN_BLACKLIST_PK_PREFIX}#{token_jti}",
        "SK": f"{TOKEN_BLACKLIST_SK_PREFIX}#{token_jti}",
        "token_jti": token_jti,
        "token_hash": token_jti,  # For additional verification if needed
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": expires_at,
        "ttl": expires_at,  # DynamoDB TTL attribute for automatic deletion
        "GSI1PK": TOKEN_BLACKLIST_PK_PREFIX,
        "GSI1SK": f"{TOKEN_BLACKLIST_SK_PREFIX}#{expires_at}"
    }
    
    # Store in DynamoDB
    dynamodb_repo.put_item(item)
    logger.info(f"Token added to blacklist with JTI: {token_jti[:8]}...")


def _get_token_expiry(token: str) -> Optional[int]:
    """
    Extract token expiry from JWT token without verifying signature.
    
    Args:
        token: JWT token
        
    Returns:
        Token expiry timestamp (epoch seconds) or None if unable to parse
    """
    try:
        # Split the token to get the payload
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # Decode the payload (without verification)
        import base64
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + "==").decode('utf-8'))
        
        # Return the expiration timestamp
        return payload.get('exp')
    except Exception as e:
        logger.warning(f"Error extracting token expiry: {str(e)}")
        return None


def _is_token_blacklisted(token_jti: str) -> bool:
    """
    Check if token is blacklisted.
    
    Args:
        token_jti: Token unique identifier
        
    Returns:
        True if token is blacklisted, False otherwise
    """
    key = {
        "PK": f"{TOKEN_BLACKLIST_PK_PREFIX}#{token_jti}",
        "SK": f"{TOKEN_BLACKLIST_SK_PREFIX}#{token_jti}"
    }
    
    item = dynamodb_repo.get_item(key)
    return item is not None


@handle_lambda_error
def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Logout handler for authentication.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    logger.info("Processing logout request")
    
    try:
        # Extract token from request
        token = _extract_token(event)
        
        # Generate token JTI (unique identifier)
        token_jti = _get_token_jti(token)
        
        # Check if token is already blacklisted
        if _is_token_blacklisted(token_jti):
            logger.info(f"Token already blacklisted: {token_jti[:8]}...")
            return format_response(
                status_code=200,
                body={"message": "Đăng xuất thành công"}
            )
        
        # Get token expiration time (if possible)
        expires_at = _get_token_expiry(token)
        
        # Add token to blacklist
        _add_token_to_blacklist(token, token_jti, expires_at)
        
        logger.info(f"Successfully logged out token: {token_jti[:8]}...")
        
        return format_response(
            status_code=200,
            body={"message": "Đăng xuất thành công"}
        )
    except UnauthorizedError as e:
        logger.warning(f"Logout failed: {str(e)}")
        return format_response(
            status_code=401,
            body={
                "status": "error",
                "code": "E1000",
                "message": "Token không hợp lệ hoặc đã hết hạn"
            }
        )
    except Exception as e:
        logger.exception(f"Unexpected error during logout: {str(e)}")
        return format_response(
            status_code=500,
            body={
                "status": "error",
                "code": "E6000",
                "message": "Lỗi hệ thống không xác định"
            }
        ) 