"""
API Gateway Authorizer lambda function for SDIMS backend.
"""
import os
from typing import Dict, Any, Optional

from aws_lambda_powertools import Logger
from common.dynamodb import DynamoDBRepository
from common.auth import AuthUtility
from auth.logout import _get_token_jti, _is_token_blacklisted

logger = Logger(service="auth-authorizer")

# Environment variables
JWT_SECRET = os.environ.get("JWT_SECRET", "your-secret-key")  # In production, use AWS Secrets Manager
TABLE_NAME = os.environ.get("TABLE_NAME")

# Initialize AuthUtility
auth_util = AuthUtility(jwt_secret=JWT_SECRET)

# Initialize DynamoDB repository
dynamodb_repo = DynamoDBRepository(table_name=TABLE_NAME)


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    API Gateway Authorizer lambda handler.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        IAM policy document
    """
    logger.info("Processing authorizer request")
    
    # Extract Authorization header
    authorization_header = event.get("headers", {}).get("Authorization")
    
    # For WebSocket connections
    if not authorization_header and "queryStringParameters" in event:
        authorization_header = f"Bearer {event.get('queryStringParameters', {}).get('token', '')}"
    
    # Extract token from header
    token = auth_util.get_jwt_from_header(authorization_header)
    
    if not token:
        logger.warning("Unauthorized: Missing or invalid Authorization header")
        return auth_util.generate_policy("user", "Deny", event["methodArn"])
    
    # Check if token is in blacklist
    token_jti = _get_token_jti(token)
    if _is_token_blacklisted(token_jti):
        logger.warning(f"Unauthorized: Token is blacklisted: {token_jti[:8]}...")
        return auth_util.generate_policy("user", "Deny", event["methodArn"])
    
    # Validate token
    is_valid, payload = auth_util.validate_token(token)
    
    if not is_valid or payload is None:
        logger.warning("Unauthorized: Invalid token")
        return auth_util.generate_policy("user", "Deny", event["methodArn"])
    
    # Extract user ID and role from token
    user_id = payload.get("sub")
    user_role = payload.get("role", "user")
    
    logger.info(f"Authorized user {user_id} with role {user_role}")
    
    # Generate policy
    context = {
        "userId": user_id,
        "userRole": user_role
    }
    
    return auth_util.generate_policy(user_id, "Allow", event["methodArn"], context) 