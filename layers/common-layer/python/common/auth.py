"""
Authentication Utilities for SDIMS

This module provides utilities for authentication and authorization.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional, Union, Tuple
import jwt
from datetime import datetime, timedelta

from common.logger import Logger

logger = Logger(service="auth-utils")

class TokenType:
    """Token types"""
    ACCESS = "access"
    REFRESH = "refresh"

class AuthError(Exception):
    """Base class for authentication errors"""
    pass

class TokenExpiredError(AuthError):
    """Exception for expired token"""
    def __init__(self, message: str = "Token has expired"):
        super().__init__(message)

class InvalidTokenError(AuthError):
    """Exception for invalid token"""
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message)

class UnauthorizedError(AuthError):
    """Exception for unauthorized access"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message)

class InsufficientPermissionsError(AuthError):
    """Exception for insufficient permissions"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message)

class AuthUtils:
    """
    Utilities for authentication and authorization
    """
    
    @staticmethod
    def get_jwt_secret() -> str:
        """
        Get JWT secret from environment variable
        
        Returns:
            JWT secret
        
        Raises:
            ValueError: If JWT_SECRET environment variable is not set
        """
        jwt_secret = os.environ.get('JWT_SECRET')
        if not jwt_secret:
            raise ValueError("JWT_SECRET environment variable is not set")
        return jwt_secret
    
    @staticmethod
    def create_token(user_id: str, name: str, email: str, 
                    roles: List[str], 
                    permissions: Optional[List[str]] = None,
                    token_type: str = TokenType.ACCESS,
                    expires_in: int = 3600) -> str:
        """
        Create JWT token
        
        Args:
            user_id: User ID
            name: User name
            email: User email
            roles: User roles
            permissions: User permissions
            token_type: Token type (access or refresh)
            expires_in: Token expiration time in seconds
                
        Returns:
            JWT token
        """
        current_time = int(time.time())
        jwt_secret = AuthUtils.get_jwt_secret()
        
        payload = {
            'sub': user_id,
            'name': name,
            'email': email,
            'roles': roles,
            'type': token_type,
            'iat': current_time,
            'exp': current_time + expires_in
        }
        
        if permissions:
            payload['permissions'] = permissions
            
        return jwt.encode(payload, jwt_secret, algorithm='HS256')
    
    @staticmethod
    def create_tokens(user_id: str, name: str, email: str, 
                     roles: List[str], 
                     permissions: Optional[List[str]] = None,
                     access_expires_in: int = 3600,
                     refresh_expires_in: int = 86400 * 7) -> Dict[str, str]:
        """
        Create access and refresh tokens
        
        Args:
            user_id: User ID
            name: User name
            email: User email
            roles: User roles
            permissions: User permissions
            access_expires_in: Access token expiration time in seconds
            refresh_expires_in: Refresh token expiration time in seconds
                
        Returns:
            Dictionary containing access and refresh tokens
        """
        access_token = AuthUtils.create_token(
            user_id, name, email, roles, permissions,
            token_type=TokenType.ACCESS,
            expires_in=access_expires_in
        )
        
        refresh_token = AuthUtils.create_token(
            user_id, name, email, roles, permissions,
            token_type=TokenType.REFRESH,
            expires_in=refresh_expires_in
        )
        
        return {
            'accessToken': access_token,
            'refreshToken': refresh_token,
            'expiresIn': access_expires_in
        }
    
    @staticmethod
    def verify_token(token: str, required_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Verify JWT token
        
        Args:
            token: JWT token
            required_type: Required token type (access or refresh)
                
        Returns:
            Token payload
        
        Raises:
            InvalidTokenError: If token is invalid
            TokenExpiredError: If token has expired
        """
        try:
            jwt_secret = AuthUtils.get_jwt_secret()
            payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
            
            # Check token type if required
            if required_type and payload.get('type') != required_type:
                raise InvalidTokenError(f"Expected {required_type} token, got {payload.get('type')}")
                
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            raise TokenExpiredError()
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            raise InvalidTokenError(str(e))
    
    @staticmethod
    def extract_token_from_header(authorization_header: Optional[str]) -> str:
        """
        Extract token from Authorization header
        
        Args:
            authorization_header: Authorization header
                
        Returns:
            JWT token
            
        Raises:
            InvalidTokenError: If token is missing or invalid
        """
        if not authorization_header:
            raise InvalidTokenError("Missing Authorization header")
            
        parts = authorization_header.split()
        
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise InvalidTokenError("Authorization header must be in format: Bearer <token>")
            
        return parts[1]
    
    @staticmethod
    def check_permission(user_permissions: List[str], required_permission: str) -> bool:
        """
        Check if user has a specific permission
        
        Args:
            user_permissions: List of user permissions
            required_permission: Required permission
                
        Returns:
            True if user has permission, False otherwise
        """
        # Check for direct match
        if required_permission in user_permissions:
            return True
            
        # Check for wildcard permissions
        parts = required_permission.split(':')
        if len(parts) >= 2:
            resource = parts[0]
            action = parts[1]
            
            # Check resource:* permission
            resource_wildcard = f"{resource}:*"
            if resource_wildcard in user_permissions:
                return True
                
            # Check *:action permission
            action_wildcard = f"*:{action}"
            if action_wildcard in user_permissions:
                return True
                
            # Check *:* permission (superuser)
            if "*:*" in user_permissions:
                return True
                
        return False
    
    @staticmethod
    def has_permissions(user_permissions: List[str], required_permissions: List[str]) -> bool:
        """
        Check if user has all required permissions
        
        Args:
            user_permissions: List of user permissions
            required_permissions: List of required permissions
                
        Returns:
            True if user has all required permissions, False otherwise
        """
        for permission in required_permissions:
            if not AuthUtils.check_permission(user_permissions, permission):
                return False
        return True
    
    @staticmethod
    def has_any_permission(user_permissions: List[str], required_permissions: List[str]) -> bool:
        """
        Check if user has any of the required permissions
        
        Args:
            user_permissions: List of user permissions
            required_permissions: List of required permissions
                
        Returns:
            True if user has any of the required permissions, False otherwise
        """
        for permission in required_permissions:
            if AuthUtils.check_permission(user_permissions, permission):
                return True
        return False
    
    @staticmethod
    def has_role(user_roles: List[str], required_roles: Union[str, List[str]]) -> bool:
        """
        Check if user has required role(s)
        
        Args:
            user_roles: User roles
            required_roles: Required role or list of roles
                
        Returns:
            True if user has any of the required roles, False otherwise
        """
        if isinstance(required_roles, str):
            required_roles = [required_roles]
            
        return any(role in required_roles for role in user_roles)
    
    @staticmethod
    def authorize(token_payload: Dict[str, Any], 
                 required_permissions: Optional[List[str]] = None,
                 required_roles: Optional[List[str]] = None,
                 require_all_permissions: bool = True) -> bool:
        """
        Authorize user based on token payload, required permissions and roles
        
        Args:
            token_payload: Token payload
            required_permissions: List of required permissions
            required_roles: List of required roles
            require_all_permissions: If True, user must have all required permissions
                
        Returns:
            True if authorized, False otherwise
            
        Raises:
            InsufficientPermissionsError: If user doesn't have required permissions
        """
        # Always authorized if no permissions or roles are required
        if not required_permissions and not required_roles:
            return True
            
        # Check roles if specified
        if required_roles:
            user_roles = token_payload.get('roles', [])
            if not AuthUtils.has_role(user_roles, required_roles):
                raise InsufficientPermissionsError(
                    f"User does not have required roles: {required_roles}"
                )
                
        # Check permissions if specified
        if required_permissions:
            user_permissions = token_payload.get('permissions', [])
            
            if require_all_permissions:
                if not AuthUtils.has_permissions(user_permissions, required_permissions):
                    raise InsufficientPermissionsError(
                        f"User does not have all required permissions: {required_permissions}"
                    )
            else:
                if not AuthUtils.has_any_permission(user_permissions, required_permissions):
                    raise InsufficientPermissionsError(
                        f"User does not have any of the required permissions: {required_permissions}"
                    )
                    
        return True
        
    @staticmethod
    def generate_password_hash(password: str) -> str:
        """
        Generate password hash
        
        Args:
            password: Plain text password
                
        Returns:
            Hashed password
        """
        import hashlib
        import os
        
        # Generate a random salt
        salt = os.urandom(32)
        
        # Hash the password with the salt
        pwdhash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        
        # Combine salt and hash
        return salt.hex() + ':' + pwdhash.hex()
    
    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        """
        Verify password against hash
        
        Args:
            stored_password: Stored password hash
            provided_password: Password to verify
                
        Returns:
            True if password matches, False otherwise
        """
        import hashlib
        
        try:
            # Extract salt and hash
            salt_hex, hash_hex = stored_password.split(':')
            
            # Convert hex to bytes
            salt = bytes.fromhex(salt_hex)
            
            # Hash the provided password with the extracted salt
            pwdhash = hashlib.pbkdf2_hmac(
                'sha256',
                provided_password.encode('utf-8'),
                salt,
                100000
            )
            
            # Compare the hashes
            return pwdhash.hex() == hash_hex
        except Exception as e:
            logger.error("Error verifying password", exc=e)
            return False 