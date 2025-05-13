"""
Authentication lambda function for SDIMS backend.
"""
import os
import json
from typing import Dict, Any

import boto3
from aws_lambda_powertools import Logger

from src.common.auth import AuthUtility
from src.common.errors import UnauthorizedError, ValidationError, handle_lambda_error
from src.common.utils import parse_json_body, format_response

logger = Logger(service="auth-service")

# Environment variables
JWT_SECRET = os.environ.get("JWT_SECRET", "your-secret-key")  # In production, use AWS Secrets Manager

# Initialize AuthUtility
auth_util = AuthUtility(jwt_secret=JWT_SECRET)


@handle_lambda_error
def login_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Login handler for authentication.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response with token
    """
    logger.info("Processing login request")
    
    # Parse request body
    body = parse_json_body(event.get("body"))
    
    # Validate inputs
    username = body.get("username")
    password = body.get("password")
    
    if not username or not password:
        logger.warning("Login failed: Missing username or password")
        raise ValidationError("Username and password are required")
    
    # TODO: Replace this with actual DB lookup in DynamoDB
    # This is a placeholder implementation
    if username == "admin" and password == "password":
        user_id = "user-123"
        user_role = "admin"
    else:
        logger.warning(f"Login failed: Invalid credentials for username {username}")
        raise UnauthorizedError("Invalid username or password")
    
    # Generate token
    token_data = auth_util.generate_token(user_id, user_role)
    
    logger.info(f"Login successful for user {username}")
    
    # Return token
    return format_response(
        status_code=200,
        body={
            "token": token_data["token"],
            "refresh_token": token_data["refresh_token"],
            "expires_in": token_data["expires_in"],
            "user": {
                "id": user_id,
                "username": username,
                "role": user_role
            }
        }
    )


@handle_lambda_error
def logout_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Logout handler.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    logger.info("Processing logout request")
    
    # For JWT-based authentication, no server-side action is needed
    # The client should discard the token
    
    return format_response(
        status_code=200,
        body={"message": "Successfully logged out"}
    ) 