import json
import os
import logging
import re
from typing import Dict, Any, List
import jwt
from aws_lambda_powertools import Logger

from repositories.token_repository import TokenRepository

# Set up logger
logger = Logger(service="api-authorizer")

# Get JWT secret from environment variable
JWT_SECRET = os.environ.get("JWT_SECRET", "this_is_a_temporary_secret_key_replace_in_production")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")

# Public routes that don't require authentication
PUBLIC_ROUTES = [
    "/api/v1/auth/login",
    "/api/v1/auth/refresh-token"
]

def has_permission(required_permission: str, user_permissions: List[str]) -> bool:
    """
    Check if a user has a required permission.
    
    Args:
        required_permission: The required permission (e.g. "employee:read:all")
        user_permissions: List of user's permissions
        
    Returns:
        bool: True if the user has the permission, False otherwise
    """
    # If the user has the exact permission, return True
    if required_permission in user_permissions:
        return True
    
    # Parse the permission into resource, action, and scope
    parts = required_permission.split(":")
    if len(parts) < 2:
        return False
    
    resource = parts[0]
    action = parts[1]
    scope = parts[2] if len(parts) > 2 else None
    
    # Check for broader permissions (without scope)
    if f"{resource}:{action}" in user_permissions:
        return True
    
    # If scope is provided, check for broader scopes
    if scope:
        # Define scope hierarchy (all > team > own)
        if scope == "team" and f"{resource}:{action}:all" in user_permissions:
            return True
        
        if scope == "own" and (
            f"{resource}:{action}:all" in user_permissions or 
            f"{resource}:{action}:team" in user_permissions
        ):
            return True
            
        if scope == "assigned" and (
            f"{resource}:{action}:all" in user_permissions
        ):
            return True
    
    return False


def generate_policy(principal_id: str, effect: str, resource: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generate an IAM policy for API Gateway.
    
    Args:
        principal_id: User ID
        effect: 'Allow' or 'Deny'
        resource: API Gateway resource ARN
        context: Additional context to pass to the request
        
    Returns:
        Dict: IAM policy document
    """
    policy = {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource
                }
            ]
        }
    }
    
    if context:
        policy["context"] = context
    
    return policy


def extract_token_from_header(auth_header: str) -> str:
    """
    Extract JWT token from Authorization header.
    
    Args:
        auth_header: Authorization header value
        
    Returns:
        str: JWT token
        
    Raises:
        Exception: If no token can be extracted
    """
    if not auth_header:
        raise Exception("Missing Authorization header")
        
    match = re.match(r"^Bearer\s+(.+)$", auth_header)
    if not match:
        raise Exception("Invalid Authorization header format")
        
    return match.group(1)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for API Gateway custom authorizer.
    
    Args:
        event: Event data from API Gateway
        context: Lambda context
        
    Returns:
        Dict: IAM policy document
    """
    try:
        # Check if it's a public route that doesn't require authentication
        if "path" in event:
            path = event["path"]
            if path in PUBLIC_ROUTES:
                return generate_policy(
                    principal_id="public",
                    effect="Allow",
                    resource=event.get("methodArn", "*")
                )
                
        # Get the Authorization header
        auth_header = event.get("headers", {}).get("Authorization") or event.get("authorizationToken")
        if not auth_header:
            logger.warning("Missing Authorization header")
            raise Exception("Unauthorized")
            
        # Extract token
        token = extract_token_from_header(auth_header)
        
        # Verify token
        try:
            # Decode the JWT token
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            
            # Check if token is blacklisted
            token_repository = TokenRepository()
            if "jti" in payload and token_repository.is_token_blacklisted(payload["jti"]):
                logger.warning(f"Blacklisted token used: {payload['jti']}")
                raise Exception("Token revoked")
                
            # Extract user ID and permissions
            user_id = payload.get("sub")
            if not user_id:
                logger.warning("Token missing user ID (sub claim)")
                raise Exception("Invalid token")
                
            # Path-based authorization (optional)
            # If you want to check permissions based on API path, you can add that logic here
            # Example: Check if user has permission to access this resource based on method and path
            
            # Return policy with user context
            return generate_policy(
                principal_id=user_id,
                effect="Allow",
                resource=event.get("methodArn", "*"),
                context={
                    "userId": user_id,
                    "username": payload.get("username", ""),
                    "permissions": json.dumps(payload.get("permissions", [])),
                    "role": payload.get("role", "")
                }
            )
        except jwt.ExpiredSignatureError:
            logger.warning("Expired token")
            raise Exception("Token expired")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            raise Exception("Invalid token")
    except Exception as e:
        logger.error(f"Authorization failed: {str(e)}")
        return generate_policy(
            principal_id="unauthorized",
            effect="Deny",
            resource=event.get("methodArn", "*")
        ) 