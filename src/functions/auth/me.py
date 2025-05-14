import json
import os
import logging
from typing import Dict, Any
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
import jwt

from common.errors import BaseError, AuthenticationError, ValidationError, DatabaseError, AccountLockedError
from common.models.api_response import APIResponse
from services.auth_service import AuthService

# Set up logger and tracer
logger = Logger(service="current-user-service")
tracer = Tracer(service="current-user-service")
app = APIGatewayRestResolver()

@app.get("/api/v1/auth/me")
@tracer.capture_method
def get_current_user():
    """
    Get the current authenticated user from the JWT token.
    """
    try:
        # Get token from Authorization header
        auth_header = app.current_event.get_header_value("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("Missing or invalid Authorization header")
            return APIResponse.error(
                status_code=401,
                message="Chưa đăng nhập",
                error_code="E1001"
            )
            
        # Extract token
        token = auth_header.replace("Bearer ", "")
        
        # Get current user
        auth_service = AuthService()
        user_data = auth_service.get_current_user(token)
        
        # Return current user info
        return APIResponse.success(
            status_code=200,
            data=user_data
        )
    except AuthenticationError as e:
        logger.warning(f"Authentication error: {str(e)}")
        return APIResponse.error(
            status_code=401,
            message=str(e),
            error_code="E1000"
        )
    except AccountLockedError as e:
        logger.warning(f"Account locked error: {str(e)}")
        return APIResponse.error(
            status_code=401,
            message=str(e),
            error_code="E1004"
        )
    except DatabaseError as e:
        logger.error(f"Database error when getting current user: {str(e)}")
        return APIResponse.error(
            status_code=500,
            message=str(e),
            error_code="E6001"
        )
    except BaseError as e:
        logger.error(f"Known error in get_current_user: {e.error_code} - {str(e)}")
        return APIResponse.error(
            status_code=e.status_code,
            message=str(e),
            error_code=e.error_code
        )
    except jwt.InvalidTokenError:
        logger.warning("Invalid token provided")
        return APIResponse.error(
            status_code=401,
            message="Token không hợp lệ",
            error_code="E1000"
        )
    except jwt.ExpiredSignatureError:
        logger.warning("Expired token provided")
        return APIResponse.error(
            status_code=401,
            message="Token đã hết hạn",
            error_code="E1000"
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_current_user: {str(e)}", exc_info=True)
        return APIResponse.error(
            status_code=500,
            message="Lỗi hệ thống, vui lòng thử lại sau",
            error_code="E6000"
        )


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Lambda handler function for getting current user API.
    
    Args:
        event: AWS Lambda event
        context: AWS Lambda context
        
    Returns:
        API Gateway response
    """
    return app.resolve(event, context) 