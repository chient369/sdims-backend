"""
Login Lambda function for SDIMS backend.

This module handles user authentication and JWT token generation.
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.validation import validate_event_or_fail
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent

from common.dynamodb import DynamoDBRepository
from common.auth import AuthUtils
from common.errors import ValidationError, UnauthorizedError, handle_error
from common.response import Response
from common.validation import validate_schema

# Configure logger
logger = Logger(service="auth-login")

# Initialize DynamoDB repository
dynamodb = DynamoDBRepository()

# Login request schema
LOGIN_SCHEMA = {
    "type": "object",
    "required": ["username", "password"],
    "properties": {
        "username": {"type": "string", "minLength": 1},
        "password": {"type": "string", "minLength": 1},
        "remember_me": {"type": "boolean"}
    },
    "additionalProperties": False
}

def get_user_by_username_or_email(username: str) -> Optional[Dict[str, Any]]:
    """
    Get user by username or email from DynamoDB
    
    Args:
        username: Username or email
        
    Returns:
        User information if found, None otherwise
    """
    try:
        # Try to find by username first (GSI1)
        logger.info(f"Querying user by username: {username}")
        users = dynamodb.query(
            index_name="GSI1",
            key_condition_expression="GSI1PK = :gsi1pk AND GSI1SK = :gsi1sk",
            expression_attribute_values={
                ":gsi1pk": "USER",
                ":gsi1sk": username
            }
        )
        
        if users and len(users) > 0:
            return users[0]
            
        # If not found, try email (GSI2)
        logger.info(f"Querying user by email: {username}")
        users = dynamodb.query(
            index_name="GSI2",
            key_condition_expression="GSI2PK = :gsi2pk AND GSI2SK = :gsi2sk",
            expression_attribute_values={
                ":gsi2pk": "USER",
                ":gsi2sk": username
            }
        )
        
        if users and len(users) > 0:
            return users[0]
            
        return None
    except Exception as e:
        logger.error(f"Error querying user: {str(e)}")
        return None

def get_user_role_and_permissions(user_id: str) -> Tuple[str, list]:
    """
    Get user role and permissions
    
    Args:
        user_id: User ID
        
    Returns:
        Tuple of role name and permissions list
    """
    try:
        # Get user's role from USER_ROLE table using GSI1
        user_roles = dynamodb.query(
            key_condition_expression="PK = :pk AND begins_with(SK, :sk_prefix)",
            expression_attribute_values={
                ":pk": f"USER#{user_id}",
                ":sk_prefix": "ROLE#"
            }
        )
        
        if not user_roles or len(user_roles) == 0:
            logger.warning(f"No roles found for user {user_id}")
            return "user", []
            
        # We'll use the first role for simplicity
        # In a real system, you might need to handle multiple roles
        role_id = user_roles[0]["role_id"]
        
        # Get role details
        role = dynamodb.get_item(
            key={
                "PK": f"ROLE#{role_id}",
                "SK": f"METADATA#{role_id}"
            }
        )
        
        if not role:
            logger.warning(f"Role {role_id} not found")
            return "user", []
            
        role_name = role.get("name", "user")
        permissions = role.get("permissions", [])
        
        return role_name, permissions
    except Exception as e:
        logger.error(f"Error getting user role and permissions: {str(e)}")
        return "user", []

def update_last_login(user_id: str) -> None:
    """
    Update user's last login timestamp
    
    Args:
        user_id: User ID
    """
    try:
        dynamodb.update_item(
            key={
                "PK": f"USER#{user_id}",
                "SK": f"METADATA#{user_id}"
            },
            update_expression="SET last_login_at = :last_login_at",
            expression_attribute_values={
                ":last_login_at": datetime.now().isoformat()
            }
        )
        logger.info(f"Updated last login for user {user_id}")
    except Exception as e:
        logger.error(f"Error updating last login: {str(e)}")

def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Login handler for authentication API endpoint
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response with tokens
    """
    logger.info("Processing login request")
    
    try:
        # Parse and validate request body
        if not event.get("body"):
            raise ValidationError("Request body is required", error_code="E2001")
            
        body = json.loads(event.get("body", "{}"))
        
        # Validate against schema
        validate_schema(body, LOGIN_SCHEMA)
        
        username = body.get("username")
        password = body.get("password")
        remember_me = body.get("remember_me", False)
        
        # Find user by username or email
        user = get_user_by_username_or_email(username)
        
        if not user:
            logger.warning(f"User not found: {username}")
            raise UnauthorizedError("Sai tên đăng nhập hoặc mật khẩu", error_code="E1005")
            
        # Check if account is active
        if not user.get("is_active", False):
            logger.warning(f"Inactive account: {username}")
            raise UnauthorizedError("Tài khoản bị khóa", error_code="E1004")
            
        # Verify password
        if not AuthUtils.verify_password(user.get("password_hash", ""), password):
            logger.warning(f"Invalid password for user: {username}")
            # Optionally, you could implement a counter for failed login attempts here
            raise UnauthorizedError("Sai tên đăng nhập hoặc mật khẩu", error_code="E1005")
            
        user_id = user.get("id")
        
        # Get user role and permissions
        role, permissions = get_user_role_and_permissions(user_id)
        
        # Update last login timestamp
        update_last_login(user_id)
        
        # Generate JWT tokens
        # Adjust token expiration based on remember_me flag
        access_expires_in = 86400 if remember_me else 3600  # 24 hours vs 1 hour
        refresh_expires_in = 30 * 86400 if remember_me else 7 * 86400  # 30 days vs 7 days
        
        tokens = AuthUtils.create_tokens(
            user_id=user_id,
            name=user.get("full_name", ""),
            email=user.get("email", ""),
            roles=[role],
            permissions=permissions,
            access_expires_in=access_expires_in,
            refresh_expires_in=refresh_expires_in
        )
        
        logger.info(f"Login successful for user {username}")
        
        # Format response according to API specification
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "status": "success",
                "code": 200,
                "data": {
                    "token": tokens["accessToken"],
                    "token_type": "Bearer",
                    "expires_in": access_expires_in,
                    "user": {
                        "id": user_id,
                        "username": user.get("username", ""),
                        "email": user.get("email", ""),
                        "fullname": user.get("full_name", ""),
                        "role": role,
                        "permissions": permissions
                    }
                }
            })
        }
    except Exception as e:
        return handle_error(e) 