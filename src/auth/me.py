"""
Lambda function for getting current user information.
"""
import os
from typing import Dict, Any

from aws_lambda_powertools import Logger
from boto3.dynamodb.conditions import Key

from src.common.auth import AuthUtility
from src.common.errors import UnauthorizedError, handle_lambda_error
from src.common.utils import format_response
from src.auth.models import User, UserStatus

logger = Logger(service="auth-service")

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("DYNAMODB_TABLE", "SDIMS_Main"))

@handle_lambda_error
def me_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handler for getting current user information.
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response with user info
    """
    logger.info("Processing get current user request")
    
    # Get user context from the authorizer
    request_context = event.get("requestContext", {})
    authorizer_context = request_context.get("authorizer", {})
    
    user_id = authorizer_context.get("userId")
    if not user_id:
        logger.warning("User ID not found in authorizer context")
        raise UnauthorizedError("User not authenticated")
    
    # Query user from DynamoDB
    response = table.query(
        KeyConditionExpression=Key("id").eq(f"USER#{user_id}") & Key("metadata").eq("METADATA")
    )
    
    items = response.get("Items", [])
    if not items:
        logger.warning(f"User not found: {user_id}")
        raise UnauthorizedError("User not found")
    
    user_data = items[0]
    user = User.from_dynamodb(user_data)
    
    # Check if user is active
    if user.status != UserStatus.ACTIVE:
        logger.warning(f"User account is not active: {user_id}")
        raise UnauthorizedError("User account is not active")
    
    # Get role permissions
    permissions = get_permissions_for_role(user.role.value)
    
    # Format user info for response
    user_info = {
        "id": user.user_id,
        "username": user.username,
        "email": user.email,
        "fullName": user.full_name,
        "isActive": user.status == UserStatus.ACTIVE,
        "lastLoginAt": user.last_login.isoformat() if user.last_login else None,
        "role": {
            "id": user.role.value,
            "name": user.role.value.capitalize()
        },
        "permissions": permissions
    }
    
    logger.info(f"Retrieved user info for user {user_id}")
    
    return format_response(
        status_code=200,
        body={"user": user_info}
    )

def get_permissions_for_role(role: str) -> list:
    """
    Get permissions for a role.
    
    Args:
        role: Role name
        
    Returns:
        List of permissions
    """
    # Define permissions map for each role
    permissions_map = {
        "admin": [
            "user:read:all",
            "user:write:all",
            "employee:read:all",
            "employee:write:all",
            "contract:read:all",
            "contract:write:all",
            "opportunity:read:all",
            "opportunity:write:all",
            "margin:read:all",
            "report:read:all",
            "system:admin"
        ],
        "manager": [
            "user:read:own",
            "employee:read:all",
            "employee:write:department",
            "contract:read:department",
            "opportunity:read:department",
            "opportunity:write:department",
            "margin:read:department",
            "report:read:department"
        ],
        "leader": [
            "user:read:own",
            "employee:read:team",
            "employee:write:team",
            "contract:read:team",
            "opportunity:read:team",
            "margin:read:team",
            "report:read:team"
        ],
        "sales": [
            "user:read:own",
            "employee:read:basic",
            "contract:read:own",
            "contract:write:own",
            "opportunity:read:own",
            "opportunity:write:own",
            "report:read:sales"
        ],
        "employee": [
            "user:read:own",
            "employee:read:own",
            "employee:write:profile",
        ],
        "user": [
            "user:read:own"
        ]
    }
    
    return permissions_map.get(role, []) 