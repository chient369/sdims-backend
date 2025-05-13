"""
Refresh token lambda function for SDIMS backend.
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
def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Refresh token handler.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response with new token
    """
    logger.info("Processing refresh token request")
    
    # Parse request body
    body = parse_json_body(event.get("body"))
    
    # Get refresh token from request
    refresh_token = body.get("refresh_token")
    
    if not refresh_token:
        logger.warning("Refresh token is missing in request")
        raise ValidationError("Refresh token is required")
    
    # Use refresh token to generate new access token
    token_data = auth_util.refresh_access_token(refresh_token)
    
    if not token_data:
        logger.warning("Failed to refresh token")
        raise UnauthorizedError("Invalid or expired refresh token")
    
    logger.info("Successfully refreshed token")
    
    # Return new token
    return format_response(
        status_code=200,
        body={
            "token": token_data["token"],
            "expires_in": token_data["expires_in"]
        }
    ) 