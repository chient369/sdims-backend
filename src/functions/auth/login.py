import json
import os
import logging
from typing import Dict, Any
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.validation import validate_event_or_fail
from aws_lambda_powertools.utilities.validation.exceptions import SchemaValidationError

from common.errors import BaseError, AuthenticationError, ValidationError, AccountLockedError
from common.models.api_response import APIResponse
from services.auth_service import AuthService

# Set up logger and tracer
logger = Logger(service="login-service")
tracer = Tracer(service="login-service")
app = APIGatewayRestResolver()

# Validation schema for login request
LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 1},
        "password": {"type": "string", "minLength": 1},
        "remember_me": {"type": "boolean"}
    },
    "required": ["username", "password"],
    "additionalProperties": False
}

@app.post("/api/v1/auth/login")
@tracer.capture_method
def login():
    """
    Handle login request, validate credentials and return JWT token.
    """
    try:
        # Get request body
        body = app.current_event.json_body
        
        # Validate request body against schema
        try:
            validate_event_or_fail(body, LOGIN_SCHEMA)
        except SchemaValidationError as e:
            logger.warning("Invalid login request format")
            errors = [{"field": ".".join(err["path"]), "message": err["message"]} for err in e.validation_errors]
            return APIResponse.error(
                status_code=400, 
                message="Thiếu tham số bắt buộc", 
                error_code="E2001",
                errors=errors
            )
            
        # Extract login credentials
        username = body.get("username")
        password = body.get("password")
        remember_me = body.get("remember_me", False)
        
        # Authenticate user
        auth_service = AuthService()
        auth_result = auth_service.login(username, password, remember_me)
        
        # Return successful login response
        return APIResponse.success(
            status_code=200,
            data=auth_result
        )
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        return APIResponse.error(
            status_code=400,
            message=str(e),
            error_code="E2001",
            errors=e.errors
        )
    except AuthenticationError as e:
        logger.warning(f"Authentication error: {str(e)}")
        return APIResponse.error(
            status_code=401,
            message=str(e),
            error_code="E1005"
        )
    except AccountLockedError as e:
        logger.warning(f"Account locked error: {str(e)}")
        return APIResponse.error(
            status_code=401,
            message=str(e),
            error_code="E1004"
        )
    except BaseError as e:
        logger.error(f"Known error in login: {e.error_code} - {str(e)}")
        return APIResponse.error(
            status_code=e.status_code,
            message=str(e),
            error_code=e.error_code
        )
    except Exception as e:
        logger.error(f"Unexpected error in login: {str(e)}", exc_info=True)
        return APIResponse.error(
            status_code=500,
            message="Lỗi hệ thống, vui lòng thử lại sau",
            error_code="E5000"
        )


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Lambda handler function for login API.
    
    Args:
        event: AWS Lambda event
        context: AWS Lambda context
        
    Returns:
        API Gateway response
    """
    return app.resolve(event, context) 