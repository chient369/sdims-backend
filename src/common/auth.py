"""
Authentication utilities for SDIMS backend.
"""
from typing import Any, Dict, List, Optional, Tuple, Union
import os
import json
import time
import boto3
import jwt
from aws_lambda_powertools import Logger

logger = Logger(service="auth-utils")

class AuthUtility:
    """
    Utility class for authentication operations.
    Handles JWT token generation, validation, and user authentication.
    """
    
    def __init__(
        self,
        jwt_secret: str,
        token_expiry: int = 3600,  # 1 hour in seconds
        refresh_token_expiry: int = 604800,  # 7 days in seconds
    ):
        """
        Initialize authentication utility.
        
        Args:
            jwt_secret: Secret key for JWT token generation/validation
            token_expiry: Token expiration time in seconds
            refresh_token_expiry: Refresh token expiration time in seconds
        """
        self.jwt_secret = jwt_secret
        self.token_expiry = token_expiry
        self.refresh_token_expiry = refresh_token_expiry
        logger.info("Initialized authentication utility")
        
    def generate_token(self, user_id: str, user_role: str) -> Dict[str, str]:
        """
        Generate JWT token for a user.
        
        Args:
            user_id: User ID
            user_role: User role
            
        Returns:
            Dictionary containing token and refresh token
        """
        try:
            current_time = int(time.time())
            
            # Create token payload
            token_payload = {
                'sub': user_id,
                'role': user_role,
                'iat': current_time,
                'exp': current_time + self.token_expiry
            }
            
            # Create refresh token payload
            refresh_payload = {
                'sub': user_id,
                'type': 'refresh',
                'iat': current_time,
                'exp': current_time + self.refresh_token_expiry
            }
            
            # Generate tokens
            token = jwt.encode(token_payload, self.jwt_secret, algorithm='HS256')
            refresh_token = jwt.encode(refresh_payload, self.jwt_secret, algorithm='HS256')
            
            logger.info(f"Generated token for user {user_id}")
            
            return {
                'token': token,
                'refresh_token': refresh_token,
                'expires_in': self.token_expiry
            }
        except Exception as e:
            logger.error(f"Error generating token: {str(e)}")
            raise
    
    def validate_token(self, token: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate a JWT token.
        
        Args:
            token: JWT token to validate
            
        Returns:
            Tuple of (is_valid, payload)
        """
        try:
            # Decode and validate token
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            
            # Check if token is expired
            if int(time.time()) > payload.get('exp', 0):
                logger.warning(f"Token expired for user {payload.get('sub')}")
                return False, None
                
            logger.info(f"Successfully validated token for user {payload.get('sub')}")
            return True, payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token validation failed: Token expired")
            return False, None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token validation failed: {str(e)}")
            return False, None
        except Exception as e:
            logger.error(f"Error validating token: {str(e)}")
            return False, None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, str]]:
        """
        Generate a new access token using a refresh token.
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            Dictionary containing new token or None if refresh token is invalid
        """
        try:
            # Validate refresh token
            is_valid, payload = self.validate_token(refresh_token)
            
            if not is_valid or payload is None:
                logger.warning("Refresh token validation failed")
                return None
                
            # Check if it's a refresh token
            if payload.get('type') != 'refresh':
                logger.warning("Invalid token type for refresh operation")
                return None
                
            # Get user ID from payload
            user_id = payload.get('sub')
            
            # TODO: Retrieve user role from database based on user_id
            # For now, we'll use a default role
            user_role = "user"
            
            # Generate new access token
            current_time = int(time.time())
            token_payload = {
                'sub': user_id,
                'role': user_role,
                'iat': current_time,
                'exp': current_time + self.token_expiry
            }
            
            token = jwt.encode(token_payload, self.jwt_secret, algorithm='HS256')
            
            logger.info(f"Refreshed access token for user {user_id}")
            
            return {
                'token': token,
                'expires_in': self.token_expiry
            }
        except Exception as e:
            logger.error(f"Error refreshing access token: {str(e)}")
            return None
    
    def generate_policy(
        self, 
        principal_id: str, 
        effect: str, 
        resource: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate IAM policy document for API Gateway authorization.
        
        Args:
            principal_id: Principal ID (usually user ID)
            effect: Allow or Deny
            resource: Resource ARN
            context: Context to pass to the target function
            
        Returns:
            IAM policy document
        """
        policy = {
            'principalId': principal_id,
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [{
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': resource
                }]
            }
        }
        
        # Add context if provided
        if context:
            policy['context'] = context
            
        return policy
        
    def get_jwt_from_header(self, authorization_header: Optional[str]) -> Optional[str]:
        """
        Extract JWT token from Authorization header.
        
        Args:
            authorization_header: Authorization header value
            
        Returns:
            JWT token or None if not found
        """
        if not authorization_header:
            logger.warning("Authorization header is missing")
            return None
            
        parts = authorization_header.split()
        
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            logger.warning("Invalid Authorization header format")
            return None
            
        return parts[1] 