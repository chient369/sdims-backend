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

from common.errors import BaseError, AuthenticationError, ValidationError, DatabaseError, AccountLockedError
from common.models.api_response import APIResponse
from services.auth_service import AuthService

# Set up logger and tracer
logger = Logger(service="refresh-token-service")
tracer = Tracer(service="refresh-token-service")
app = APIGatewayRestResolver()

# Validation schema for refresh token request
REFRESH_TOKEN_SCHEMA = {
    "type": "object",
    "properties": {
        "refresh_token": {"type": "string", "minLength": 1}
    },
    "required": ["refresh_token"],
    "additionalProperties": False
}

@app.post("/api/v1/auth/refresh-token")
@tracer.capture_method
def refresh_token():
    """
    Handle refresh token request, validate refresh token and return new access token.
    """
    try:
        # Get request body
        body = app.current_event.json_body
        
        # Validate request body against schema
        try:
            validate_event_or_fail(body, REFRESH_TOKEN_SCHEMA)
        except SchemaValidationError as e:
            logger.warning("Invalid refresh token request format")
            errors = [{"field": ".".join(err["path"]), "message": err["message"]} for err in e.validation_errors]
            return APIResponse.error(
                status_code=400, 
                message="Thiếu tham số bắt buộc", 
                error_code="E2001",
                errors=errors
            )
            
        # Extract refresh token
        refresh_token = body.get("refresh_token")
        
        # Refresh token
        auth_service = AuthService()
        token_result = auth_service.refresh_token(refresh_token)
        
        # Return new tokens
        return APIResponse.success(
            status_code=200,
            data=token_result
        )
    except AuthenticationError as e:
        logger.warning(f"Authentication error during token refresh: {str(e)}")
        return APIResponse.error(
            status_code=401,
            message=str(e),
            error_code="E1000"
        )
    except AccountLockedError as e:
        logger.warning(f"Account locked error during token refresh: {str(e)}")
        return APIResponse.error(
            status_code=401,
            message=str(e),
            error_code="E1004"
        )
    except DatabaseError as e:
        logger.error(f"Database error during token refresh: {str(e)}")
        return APIResponse.error(
            status_code=500,
            message=str(e),
            error_code="E6001"
        )
    except BaseError as e:
        logger.error(f"Known error in refresh_token: {e.error_code} - {str(e)}")
        return APIResponse.error(
            status_code=e.status_code,
            message=str(e),
            error_code=e.error_code
        )
    except jwt.InvalidTokenError:
        logger.warning("Invalid refresh token provided")
        return APIResponse.error(
            status_code=401,
            message="Refresh token không hợp lệ",
            error_code="E1000"
        )
    except jwt.ExpiredSignatureError:
        logger.warning("Expired refresh token provided")
        return APIResponse.error(
            status_code=401,
            message="Refresh token đã hết hạn",
            error_code="E1000"
        )
    except Exception as e:
        logger.error(f"Unexpected error in refresh_token: {str(e)}", exc_info=True)
        return APIResponse.error(
            status_code=500,
            message="Lỗi hệ thống, vui lòng thử lại sau",
            error_code="E6000"
        )


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Lambda handler function for refresh token API.
    
    Args:
        event: AWS Lambda event
        context: AWS Lambda context
        
    Returns:
        API Gateway response
    """
    return app.resolve(event, context) 