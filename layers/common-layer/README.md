# Common Utilities Layer

## Overview

This layer provides common utilities and services used across all Lambda functions in the SDIMS backend system. It is designed to standardize implementation patterns and reduce code duplication.

## Installation

The common layer is automatically attached to all Lambda functions through the SAM template configuration.

## Components

### DynamoDB Repository (`common.dynamodb`)

A class for interacting with DynamoDB tables, providing standard operations and best practices.

```python
from common.dynamodb import DynamoDBRepository

# Create a repository instance
repo = DynamoDBRepository()  # Uses TABLE_NAME from environment
# or
repo = DynamoDBRepository(table_name="my-table")

# Basic operations
item = repo.get_item({"PK": "USER#123", "SK": "PROFILE"})
repo.put_item({"PK": "USER#123", "SK": "PROFILE", "name": "John Doe"})
repo.delete_item({"PK": "USER#123", "SK": "PROFILE"})

# Query operations
response = repo.query(
    key_condition_expression="PK = :pk",
    expression_attribute_values={":pk": "USER#123"}
)
items = response.get('Items', [])

# Update operations
updated = repo.update_item(
    key={"PK": "USER#123", "SK": "PROFILE"},
    update_expression="SET #name = :name",
    expression_attribute_values={":name": "Jane Doe"},
    expression_attribute_names={"#name": "name"}
)

# Batch operations
items = repo.batch_get_items([
    {"PK": "USER#123", "SK": "PROFILE"},
    {"PK": "USER#456", "SK": "PROFILE"}
])
```

### Response Utilities (`common.response`)

Utilities for creating standardized API Gateway responses.

```python
from common.response import Response

# Success response
return Response.success({"message": "Operation successful"})
return Response.success({"id": "new-id"}, status_code=201)  # Created

# Error response
return Response.error("Not found", status_code=404, error_code="E3000")

# Response with validation errors
details = {"email": ["Invalid format"], "password": ["Too short"]}
return Response.error("Validation error", status_code=400, error_code="E2001", details=details)

# Paginated response
return Response.paginated(
    items=[{"id": 1}, {"id": 2}],
    count=10,
    page=1,
    page_size=2,
    has_more=True
)

# Binary response (files, images)
return Response.binary(file_content, content_type="application/pdf")

# Redirect response
return Response.redirect("https://example.com/new-location")
```

### Validation Utilities (`common.validation`)

Utilities for validating input data with detailed error reporting.

```python
from common.validation import Validator, ValidationResult, ValidationError

# Define schema for validation
user_schema = {
    "name": {
        "type": "string",
        "required": True,
        "min_length": 2,
        "max_length": 50
    },
    "email": {
        "type": "email",
        "required": True
    },
    "age": {
        "type": "integer",
        "min_value": 18
    }
}

# Validate API Gateway event body
def handler(event, context):
    validation_result = Validator.validate_json_body(event, user_schema)
    if not validation_result.is_valid:
        error_details = validation_result.to_dict()
        return Response.error("Validation error", 400, "E2001", error_details)
    
    # Process valid request...

# Validate query parameters
params_schema = {
    "page": {
        "type": "integer",
        "required": True,
        "min_value": 1
    },
    "limit": {
        "type": "integer",
        "required": True,
        "min_value": 1,
        "max_value": 100
    }
}

result = Validator.validate_query_parameters(event, params_schema)
```

### Authentication Utilities (`common.auth`)

Utilities for JWT token generation, validation, and authorization.

```python
from common.auth import AuthUtils, TokenType, InvalidTokenError, TokenExpiredError

# Create tokens
token = AuthUtils.create_token(
    user_id="user123",
    name="John Doe",
    email="john@example.com",
    roles=["admin"],
    permissions=["users:read", "users:write"]
)

# Create access and refresh tokens
tokens = AuthUtils.create_tokens(
    user_id="user123",
    name="John Doe",
    email="john@example.com",
    roles=["admin"],
    permissions=["users:read", "users:write"]
)
# tokens = { "accessToken": "...", "refreshToken": "...", "expiresIn": 3600 }

# Verify token
try:
    payload = AuthUtils.verify_token(token, required_type=TokenType.ACCESS)
    # Use payload data...
except TokenExpiredError:
    # Handle expired token
except InvalidTokenError:
    # Handle invalid token

# Extract token from Authorization header
try:
    token = AuthUtils.extract_token_from_header(event['headers'].get('Authorization'))
except InvalidTokenError:
    # Handle missing or invalid Authorization header

# Check permissions
if AuthUtils.has_permissions(user_permissions, ["users:write", "users:delete"]):
    # User has all required permissions
    
if AuthUtils.has_any_permission(user_permissions, ["users:write", "users:delete"]):
    # User has at least one of the required permissions

# Authorization
try:
    AuthUtils.authorize(
        token_payload=payload,
        required_permissions=["users:write"],
        required_roles=["admin"]
    )
    # User is authorized
except InsufficientPermissionsError:
    # User is not authorized

# Password handling
password_hash = AuthUtils.generate_password_hash("securepassword")
is_valid = AuthUtils.verify_password(password_hash, "securepassword")
```

### Error Handling (`common.errors`)

Standard error classes and a handler for consistent error responses.

```python
from common.errors import (
    BadRequestError, UnauthorizedError, ForbiddenError, 
    NotFoundError, ResourceNotFoundError, ConflictError,
    DuplicateResourceError, handle_error, http_error_handler
)

# Using error classes
try:
    user = get_user(user_id)
    if not user:
        raise ResourceNotFoundError("User", user_id)
    
    if not has_permission(user, "admin"):
        raise ForbiddenError("Admin access required")
        
    if email_exists(email):
        raise DuplicateResourceError("User", email, field="email")
except Exception as e:
    return handle_error(e)

# Using decorator
@http_error_handler
def handler(event, context):
    # This function's errors will be automatically handled
    # No try/except needed
    user_id = event['pathParameters']['id']
    user = get_user(user_id)
    if not user:
        raise ResourceNotFoundError("User", user_id)
    return Response.success(user)
```

### Logging Utilities (`common.logger`)

Extended logging with AWS Lambda Powertools.

```python
from common.logger import Logger

# Create a logger
logger = Logger(service="user-service")

# Log with different levels
logger.info("Processing request", user_id="123")
logger.error("Failed to process request", exc=exception)
logger.warning("Resource near limit", usage_percent=95)
logger.debug("Detailed information", request=event)

# Lambda context injection
@logger.inject_lambda_context
def handler(event, context):
    # Now all logs will contain Lambda context information
    logger.info("Handler started")
    # ...

# Log API Gateway event (sanitizes sensitive information)
logger.log_event(event)

# Log API Gateway response
logger.log_response(response)
```

### S3 Utilities (`common.s3`)

Utilities for working with S3 buckets.

```python
from common.s3 import S3Utils

# Create S3 utilities instance
s3_utils = S3Utils(bucket_name="my-bucket")
# or use S3_BUCKET_NAME from environment
s3_utils = S3Utils()

# Generate presigned URL
upload_url = s3_utils.generate_presigned_url(
    key="uploads/file.pdf",
    expiration=3600,
    http_method="PUT",
    content_type="application/pdf"
)

download_url = s3_utils.generate_presigned_url(
    key="uploads/file.pdf",
    expiration=3600
)

# Upload files
key = s3_utils.upload_file(
    file_path="/tmp/file.pdf",
    key="uploads/file.pdf",
    content_type="application/pdf"
)

# Download files
s3_utils.download_file(
    key="uploads/file.pdf",
    destination_path="/tmp/downloaded.pdf"
)

# Check if object exists
if s3_utils.object_exists("uploads/file.pdf"):
    # Object exists
    
# Generate unique key
key = s3_utils.generate_unique_key(prefix="uploads", extension="pdf")
# e.g. "uploads/550e8400-e29b-41d4-a716-446655440000.pdf"
```

## Best Practices

1. Always use the common utilities instead of direct AWS SDK calls
2. Handle exceptions appropriately using the error classes
3. Log with appropriate severity levels
4. Validate all user inputs
5. Return standardized responses
6. Follow the repository pattern for data access

## Testing

The utilities can be easily mocked for unit testing:

```python
from unittest.mock import patch, MagicMock

# Example: Mocking DynamoDB Repository
@patch('common.dynamodb.DynamoDBRepository')
def test_function(mock_repo):
    # Setup mock
    mock_instance = MagicMock()
    mock_repo.return_value = mock_instance
    mock_instance.get_item.return_value = {"id": "123", "name": "Test"}
    
    # Call function that uses the repository
    result = my_function()
    
    # Verify
    mock_instance.get_item.assert_called_with({"PK": "123", "SK": "DETAIL"})
    assert result == {"id": "123", "name": "Test"}
``` 