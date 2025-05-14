import jwt
import time
import uuid
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta

# Secret key should be stored in environment variables or AWS Parameter Store
# in a real application
DEFAULT_SECRET_KEY = "this_is_a_temporary_secret_key_replace_in_production"
DEFAULT_ALGORITHM = "HS256"
DEFAULT_TOKEN_EXPIRY = 3600  # 1 hour in seconds
DEFAULT_REFRESH_TOKEN_EXPIRY = 7 * 24 * 3600  # 7 days in seconds


def create_token(user_id: str, 
                username: str, 
                permissions: List[str],
                secret_key: str = DEFAULT_SECRET_KEY,
                algorithm: str = DEFAULT_ALGORITHM,
                expiry: int = DEFAULT_TOKEN_EXPIRY,
                additional_claims: Optional[Dict[str, Any]] = None) -> str:
    """
    Create a JWT token for authentication.
    
    Args:
        user_id: User ID to include in token
        username: Username to include in token
        permissions: List of permission strings
        secret_key: Secret key for signing the token
        algorithm: Algorithm to use for signing
        expiry: Token expiry time in seconds
        additional_claims: Additional claims to include in the token
        
    Returns:
        str: JWT token
    """
    current_time = int(time.time())
    
    payload = {
        "sub": user_id,
        "username": username,
        "permissions": permissions,
        "iat": current_time,
        "exp": current_time + expiry,
        "jti": str(uuid.uuid4())
    }
    
    # Add any additional claims
    if additional_claims:
        payload.update(additional_claims)
    
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def create_refresh_token(user_id: str,
                        secret_key: str = DEFAULT_SECRET_KEY,
                        algorithm: str = DEFAULT_ALGORITHM,
                        expiry: int = DEFAULT_REFRESH_TOKEN_EXPIRY) -> str:
    """
    Create a refresh token.
    
    Args:
        user_id: User ID to include in token
        secret_key: Secret key for signing the token
        algorithm: Algorithm to use for signing
        expiry: Token expiry time in seconds
        
    Returns:
        str: JWT refresh token
    """
    current_time = int(time.time())
    
    payload = {
        "sub": user_id,
        "type": "refresh",
        "iat": current_time,
        "exp": current_time + expiry,
        "jti": str(uuid.uuid4())
    }
    
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def verify_token(token: str, 
                secret_key: str = DEFAULT_SECRET_KEY,
                algorithm: str = DEFAULT_ALGORITHM) -> Dict[str, Any]:
    """
    Verify a JWT token and return its payload if valid.
    
    Args:
        token: JWT token to verify
        secret_key: Secret key used for signing
        algorithm: Algorithm used for signing
        
    Returns:
        Dict: Token payload if valid
        
    Raises:
        jwt.InvalidTokenError: If token is invalid
        jwt.ExpiredSignatureError: If token has expired
    """
    return jwt.decode(token, secret_key, algorithms=[algorithm])


def is_token_expired(token: str, 
                    secret_key: str = DEFAULT_SECRET_KEY,
                    algorithm: str = DEFAULT_ALGORITHM) -> bool:
    """
    Check if a token has expired.
    
    Args:
        token: JWT token to check
        secret_key: Secret key used for signing
        algorithm: Algorithm used for signing
        
    Returns:
        bool: True if token has expired, False otherwise
    """
    try:
        verify_token(token, secret_key, algorithm)
        return False
    except jwt.ExpiredSignatureError:
        return True
    except jwt.InvalidTokenError:
        # Invalid tokens are considered expired
        return True 