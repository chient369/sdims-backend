import json
import os
import logging
from typing import Dict, Any
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.validation import validate_event_or_fail
from aws_lambda_powertools.utilities.validation.exceptions import SchemaValidationError
import jwt

from common.errors import BaseError, AuthenticationError, ValidationError, DatabaseError
from common.models.api_response import APIResponse
from services.auth_service import AuthService

# Set up logger and tracer
logger = Logger(service="logout-service")
tracer = Tracer(service="logout-service")
app = APIGatewayRestResolver()

# Validation schema for logout request
LOGOUT_SCHEMA = {
    "type": "object",
    "properties": {
        "token": {"type": "string", "minLength": 1}
    },
    "required": ["token"],
    "additionalProperties": False
}

@app.post("/api/v1/auth/logout")
@tracer.capture_method
def logout():
    """
    Handle logout request, invalidate the token by adding it to a blacklist.
    """
    try:
        # Get request body
        body = app.current_event.json_body
        
        # Get token from Authorization header if not in body
        if not body or not body.get("token"):
            auth_header = app.current_event.get_header_value("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.replace("Bearer ", "")
                body = {"token": token}
        
        # Validate request body against schema
        try:
            validate_event_or_fail(body, LOGOUT_SCHEMA)
        except SchemaValidationError as e:
            logger.warning("Invalid logout request format")
            errors = [{"field": ".".join(err["path"]), "message": err["message"]} for err in e.validation_errors]
            return APIResponse.error(
                status_code=400, 
                message="Thiếu tham số bắt buộc", 
                error_code="E2001",
                errors=errors
            )
            
        # Extract token
        token = body.get("token")
        
        # Invalidate token
        auth_service = AuthService()
        auth_service.logout(token)
        
        # Return successful logout response
        return APIResponse.success(
            status_code=200,
            message="Đăng xuất thành công"
        )
    except AuthenticationError as e:
        logger.warning(f"Authentication error during logout: {str(e)}")
        return APIResponse.error(
            status_code=401,
            message=str(e),
            error_code="E1000"
        )
    except DatabaseError as e:
        logger.error(f"Database error during logout: {str(e)}")
        return APIResponse.error(
            status_code=500,
            message=str(e),
            error_code="E6001"
        )
    except BaseError as e:
        logger.error(f"Known error in logout: {e.error_code} - {str(e)}")
        return APIResponse.error(
            status_code=e.status_code,
            message=str(e),
            error_code=e.error_code
        )
    except jwt.InvalidTokenError:
        logger.warning("Invalid token provided for logout")
        return APIResponse.error(
            status_code=401,
            message="Token không hợp lệ",
            error_code="E1000"
        )
    except Exception as e:
        logger.error(f"Unexpected error in logout: {str(e)}", exc_info=True)
        return APIResponse.error(
            status_code=500,
            message="Lỗi hệ thống, vui lòng thử lại sau",
            error_code="E6000"
        )


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Lambda handler function for logout API.
    
    Args:
        event: AWS Lambda event
        context: AWS Lambda context
        
    Returns:
        API Gateway response
    """
    return app.resolve(event, context) 