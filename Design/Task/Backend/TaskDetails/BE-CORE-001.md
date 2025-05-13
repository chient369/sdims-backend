**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-01 | Chiến Trần Văn | Định nghĩa chi tiết task Common Services Utilities | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để phát triển các tiện ích và dịch vụ common (dùng chung) cho toàn bộ backend system. Các tiện ích này sẽ được sử dụng trong tất cả các Lambda functions.

# Chi tiết Task: BE-CORE-001 - Common Services Utilities

## Thông tin chung

**Task ID:** BE-CORE-001  
**Task Name:** Phát triển Common Services Utilities  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** BE-INF-001, BE-INF-003, BE-INF-004  
**Các task phụ thuộc vào task này:** Tất cả các Lambda functions API

## Mô tả

Task này bao gồm việc phát triển các tiện ích (utilities) và dịch vụ common sử dụng Python 13.3 cho toàn bộ hệ thống backend. Các tiện ích này sẽ được sử dụng lại trong tất cả các Lambda functions để đảm bảo tính nhất quán và giảm thiểu code trùng lặp. Các tiện ích bao gồm xử lý DynamoDB, xử lý response, error handling, logging, validation, authentication, và các chức năng hỗ trợ khác.

## Chi tiết công việc

### Thiết lập Lambda Layer cho Common Utilities

- [ ] Tạo cấu trúc thư mục cho Lambda Layer:
  ```
  layers/
  └── common-layer/
      └── python/
          ├── common/
          │   ├── __init__.py
          │   ├── dynamodb.py
          │   ├── response.py
          │   ├── validation.py
          │   ├── logger.py
          │   ├── auth.py
          │   └── errors.py
          └── requirements.txt
  ```

- [ ] Cập nhật template.yaml để định nghĩa Lambda Layer:
  ```yaml
  CommonUtilitiesLayer:
    Type: AWS::Serverless::LayerVersion
    Properties:
      LayerName: !Sub "sdims-common-utilities-${Stage}"
      Description: Common utilities for SDIMS Lambda functions
      ContentUri: layers/common-layer/
      CompatibleRuntimes:
        - python3.13
      RetentionPolicy: Retain
  ```

### Phát triển DynamoDB Utilities

- [ ] Tạo lớp DynamoDB Repository trong `common/dynamodb.py`:
  ```python
  # common/dynamodb.py
  import os
  import boto3
  import json
  from typing import Dict, Any, List, Optional, TypeVar, Generic
  from aws_lambda_powertools import Logger
  from botocore.exceptions import ClientError
  
  logger = Logger(service="dynamodb-utils")
  T = TypeVar('T')
  
  class DynamoDBRepository(Generic[T]):
      """
      Repository class for interacting with DynamoDB
      """
      
      def __init__(self, table_name: Optional[str] = None):
          """
          Initialize DynamoDB repository
          
          Parameters:
          -----------
          table_name: str, optional
              Name of the DynamoDB table. If not provided, will use TABLE_NAME from environment.
          """
          self.table_name = table_name or os.environ.get('TABLE_NAME')
          self.dynamodb = boto3.resource('dynamodb')
          self.table = self.dynamodb.Table(self.table_name)
          
      def get_item(self, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
          """
          Get item from DynamoDB table
          
          Parameters:
          -----------
          key: Dict[str, Any]
              Key for retrieving the item, e.g. {"PK": "USER#123", "SK": "PROFILE"}
              
          Returns:
          --------
          Optional[Dict[str, Any]]
              Item from DynamoDB, or None if not found
          """
          try:
              response = self.table.get_item(Key=key)
              return response.get('Item')
          except ClientError as e:
              logger.exception(f"Error getting item with key {key}")
              raise
      
      def put_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
          """
          Put item into DynamoDB table
          
          Parameters:
          -----------
          item: Dict[str, Any]
              Item to store in DynamoDB
              
          Returns:
          --------
          Dict[str, Any]
              Response from DynamoDB
          """
          try:
              response = self.table.put_item(Item=item)
              return item
          except ClientError as e:
              logger.exception(f"Error putting item {item}")
              raise
      
      def query(self, 
                key_condition_expression, 
                expression_attribute_values: Optional[Dict[str, Any]] = None,
                expression_attribute_names: Optional[Dict[str, str]] = None,
                index_name: Optional[str] = None,
                limit: Optional[int] = None,
                scan_index_forward: bool = True) -> Dict[str, Any]:
          """
          Query DynamoDB table or index
          
          Parameters:
          -----------
          key_condition_expression: str
              The condition that specifies the key values for items to be retrieved
          expression_attribute_values: Dict[str, Any], optional
              Values that are substituted in the expression
          expression_attribute_names: Dict[str, str], optional
              Names that are substituted in the expression
          index_name: str, optional
              Name of the index to query
          limit: int, optional
              Maximum number of items to return
          scan_index_forward: bool
              Specifies the order for index traversal (True for forward, False for backwards)
              
          Returns:
          --------
          Dict[str, Any]
              Response from DynamoDB
          """
          try:
              params = {
                  'KeyConditionExpression': key_condition_expression,
              }
              
              if expression_attribute_values:
                  params['ExpressionAttributeValues'] = expression_attribute_values
                  
              if expression_attribute_names:
                  params['ExpressionAttributeNames'] = expression_attribute_names
                  
              if index_name:
                  params['IndexName'] = index_name
                  
              if limit:
                  params['Limit'] = limit
                  
              params['ScanIndexForward'] = scan_index_forward
              
              response = self.table.query(**params)
              return response
          except ClientError as e:
              logger.exception(f"Error querying with condition {key_condition_expression}")
              raise
      
      # Additional methods for update_item, delete_item, scan, batch operations, etc.
  ```

### Phát triển Response Utilities

- [ ] Tạo lớp Response trong `common/response.py`:
  ```python
  # common/response.py
  import json
  from typing import Dict, Any, List, Optional, Union
  
  class Response:
      """
      Class for handling API Gateway responses
      """
      
      @staticmethod
      def success(data: Any = None, status_code: int = 200) -> Dict[str, Any]:
          """
          Create a successful API response
          
          Parameters:
          -----------
          data: Any
              Data to include in the response
          status_code: int
              HTTP status code
              
          Returns:
          --------
          Dict[str, Any]
              API Gateway response
          """
          body = {}
          if data is not None:
              body = data
              
          return {
              'statusCode': status_code,
              'headers': {
                  'Content-Type': 'application/json',
                  'Access-Control-Allow-Origin': '*',
                  'Access-Control-Allow-Credentials': True
              },
              'body': json.dumps(body)
          }
      
      @staticmethod
      def error(message: str, status_code: int = 400, error_code: Optional[str] = None) -> Dict[str, Any]:
          """
          Create an error API response
          
          Parameters:
          -----------
          message: str
              Error message
          status_code: int
              HTTP status code
          error_code: str, optional
              Custom error code
              
          Returns:
          --------
          Dict[str, Any]
              API Gateway response
          """
          body = {
              'message': message
          }
          
          if error_code:
              body['code'] = error_code
              
          return {
              'statusCode': status_code,
              'headers': {
                  'Content-Type': 'application/json',
                  'Access-Control-Allow-Origin': '*',
                  'Access-Control-Allow-Credentials': True
              },
              'body': json.dumps(body)
          }
  ```

### Phát triển Validation Utilities

- [ ] Tạo lớp Validator trong `common/validation.py`:
  ```python
  # common/validation.py
  from typing import Dict, Any, List, Optional, Callable
  import re
  
  class ValidationError(Exception):
      """Exception raised for validation errors"""
      
      def __init__(self, field: str, message: str):
          self.field = field
          self.message = message
          super().__init__(self.message)
          
  class Validator:
      """
      Class for validating request inputs
      """
      
      @staticmethod
      def validate_required(data: Dict[str, Any], required_fields: List[str]) -> List[ValidationError]:
          """
          Validate that all required fields are present
          
          Parameters:
          -----------
          data: Dict[str, Any]
              Data to validate
          required_fields: List[str]
              List of fields that must be present
              
          Returns:
          --------
          List[ValidationError]
              List of validation errors, empty if validation passed
          """
          errors = []
          for field in required_fields:
              if field not in data or data[field] is None:
                  errors.append(ValidationError(field, f"Field '{field}' is required"))
          return errors
      
      @staticmethod
      def validate_string(value: str, field: str, min_length: int = 0, max_length: Optional[int] = None, 
                          pattern: Optional[str] = None) -> Optional[ValidationError]:
          """
          Validate a string field
          
          Parameters:
          -----------
          value: str
              Value to validate
          field: str
              Field name for the error message
          min_length: int
              Minimum length of the string
          max_length: int, optional
              Maximum length of the string
          pattern: str, optional
              Regular expression pattern the string must match
              
          Returns:
          --------
          Optional[ValidationError]
              ValidationError if validation fails, None otherwise
          """
          if not isinstance(value, str):
              return ValidationError(field, f"Field '{field}' must be a string")
              
          if len(value) < min_length:
              return ValidationError(field, f"Field '{field}' must be at least {min_length} characters")
              
          if max_length is not None and len(value) > max_length:
              return ValidationError(field, f"Field '{field}' must be at most {max_length} characters")
              
          if pattern is not None and not re.match(pattern, value):
              return ValidationError(field, f"Field '{field}' must match pattern: {pattern}")
              
          return None
      
      # Additional validation methods for different types (numbers, emails, dates, etc.)
  ```

### Phát triển Logging Utilities

- [ ] Tạo lớp Logger trong `common/logger.py`:
  ```python
  # common/logger.py
  import os
  import json
  import traceback
  from aws_lambda_powertools import Logger as PowertoolsLogger
  from aws_lambda_powertools.logging import correlation_paths
  from typing import Dict, Any, Optional
  
  class Logger:
      """
      Extended logger based on AWS Lambda Powertools
      """
      
      def __init__(self, service: str, level: Optional[str] = None):
          """
          Initialize logger
          
          Parameters:
          -----------
          service: str
              Service name
          level: str, optional
              Log level (INFO, DEBUG, etc.)
          """
          log_level = level or os.environ.get('LOG_LEVEL', 'INFO')
          self.logger = PowertoolsLogger(
              service=service,
              level=log_level,
              correlation_id_path=correlation_paths.API_GATEWAY_REST
          )
          
      def info(self, message: str, **kwargs):
          """Log info message with additional context"""
          self.logger.info(message, **kwargs)
          
      def error(self, message: str, exc: Optional[Exception] = None, **kwargs):
          """
          Log error message with exception details if provided
          
          Parameters:
          -----------
          message: str
              Error message
          exc: Exception, optional
              Exception object
          """
          if exc:
              kwargs['exception'] = str(exc)
              kwargs['traceback'] = traceback.format_exc()
          self.logger.error(message, **kwargs)
          
      def warning(self, message: str, **kwargs):
          """Log warning message with additional context"""
          self.logger.warning(message, **kwargs)
          
      def debug(self, message: str, **kwargs):
          """Log debug message with additional context"""
          self.logger.debug(message, **kwargs)
          
      # Add more methods as needed
  ```

### Phát triển Authentication Utilities

- [ ] Tạo các tiện ích xác thực trong `common/auth.py`:
  ```python
  # common/auth.py
  import os
  import json
  import time
  from typing import Dict, Any, List, Optional, Union
  import jwt
  from aws_lambda_powertools import Logger
  
  logger = Logger(service="auth-utils")
  
  class AuthUtils:
      """
      Utilities for authentication and authorization
      """
      
      @staticmethod
      def create_token(user_id: str, name: str, email: str, roles: List[str], 
                      expires_in: int = 3600) -> str:
          """
          Create JWT token
          
          Parameters:
          -----------
          user_id: str
              User ID
          name: str
              User name
          email: str
              User email
          roles: List[str]
              User roles
          expires_in: int
              Token expiration time in seconds
              
          Returns:
          --------
          str
              JWT token
          """
          current_time = int(time.time())
          jwt_secret = os.environ.get('JWT_SECRET')
          
          if not jwt_secret:
              raise ValueError("JWT_SECRET environment variable is not set")
              
          payload = {
              'sub': user_id,
              'name': name,
              'email': email,
              'roles': roles,
              'iat': current_time,
              'exp': current_time + expires_in
          }
          
          return jwt.encode(payload, jwt_secret, algorithm='HS256')
      
      @staticmethod
      def verify_token(token: str) -> Dict[str, Any]:
          """
          Verify JWT token
          
          Parameters:
          -----------
          token: str
              JWT token
              
          Returns:
          --------
          Dict[str, Any]
              Token payload
          
          Raises:
          -------
          jwt.InvalidTokenError
              If token is invalid
          """
          jwt_secret = os.environ.get('JWT_SECRET')
          
          if not jwt_secret:
              raise ValueError("JWT_SECRET environment variable is not set")
              
          return jwt.decode(token, jwt_secret, algorithms=['HS256'])
      
      @staticmethod
      def has_permission(user_roles: List[str], required_roles: List[str]) -> bool:
          """
          Check if user has required roles
          
          Parameters:
          -----------
          user_roles: List[str]
              User roles
          required_roles: List[str]
              Required roles
              
          Returns:
          --------
          bool
              True if user has at least one of the required roles
          """
          return any(role in required_roles for role in user_roles)
  ```

### Phát triển Error Handling Utilities

- [ ] Tạo các lớp xử lý lỗi trong `common/errors.py`:
  ```python
  # common/errors.py
  from typing import Dict, Any, List, Optional, Union
  
  class ApplicationError(Exception):
      """Base exception for application errors"""
      
      def __init__(self, message: str, status_code: int = 500, error_code: Optional[str] = None):
          self.message = message
          self.status_code = status_code
          self.error_code = error_code
          super().__init__(self.message)
  
  class BadRequestError(ApplicationError):
      """Exception for bad requests"""
      
      def __init__(self, message: str, error_code: Optional[str] = None):
          super().__init__(message, 400, error_code or 'E2000')
  
  class UnauthorizedError(ApplicationError):
      """Exception for unauthorized access"""
      
      def __init__(self, message: str = "Unauthorized", error_code: Optional[str] = None):
          super().__init__(message, 401, error_code or 'E1000')
  
  class ForbiddenError(ApplicationError):
      """Exception for forbidden access"""
      
      def __init__(self, message: str = "Forbidden", error_code: Optional[str] = None):
          super().__init__(message, 403, error_code or 'E1002')
  
  class NotFoundError(ApplicationError):
      """Exception for resource not found"""
      
      def __init__(self, message: str = "Resource not found", error_code: Optional[str] = None):
          super().__init__(message, 404, error_code or 'E3000')
  
  class ConflictError(ApplicationError):
      """Exception for resource conflict"""
      
      def __init__(self, message: str, error_code: Optional[str] = None):
          super().__init__(message, 409, error_code or 'E4004')
  
  def handle_error(error: Exception) -> Dict[str, Any]:
      """
      Handle exceptions and return appropriate API response
      
      Parameters:
      -----------
      error: Exception
          Exception to handle
          
      Returns:
      --------
      Dict[str, Any]
          API Gateway response
      """
      from common.response import Response
      
      if isinstance(error, ApplicationError):
          return Response.error(
              message=error.message,
              status_code=error.status_code,
              error_code=error.error_code
          )
      
      # Handle other exceptions
      return Response.error(
          message="Internal server error",
          status_code=500,
          error_code="E6000"
      )
  ```

### Cập nhật template.yaml

- [ ] Cập nhật template.yaml để sử dụng Common Layer trong tất cả Lambda functions:
  ```yaml
  Globals:
    Function:
      Timeout: 30
      MemorySize: 256
      Runtime: python3.13
      Layers:
        - !Ref CommonUtilitiesLayer
      Environment:
        Variables:
          LOG_LEVEL: INFO
          STAGE: !Ref Stage
          TABLE_NAME: !Ref SDIMSTable
  ```

### Viết unit tests

- [ ] Tạo unit tests cho các tiện ích common:
  ```
  tests/
  └── unit/
      └── common/
          ├── __init__.py
          ├── test_dynamodb.py
          ├── test_response.py
          ├── test_validation.py
          ├── test_logger.py
          ├── test_auth.py
          └── test_errors.py
  ```

### Tài liệu hóa

- [ ] Tạo tài liệu hướng dẫn sử dụng Common Utilities:
  - Cách sử dụng DynamoDB Repository
  - Cách xử lý response
  - Cách validate input
  - Cách xử lý lỗi
  - Cách sử dụng logging
  - Cách xác thực và ủy quyền

## Tiêu chí hoàn thành

- Common Utilities Layer được triển khai và cấu hình
- Tất cả các tiện ích common (DynamoDB, Response, Validation, Logger, Auth, Error) được phát triển
- Unit tests cho các tiện ích common được viết
- Tài liệu hướng dẫn sử dụng Common Utilities được tạo

## Ước tính thời gian

- 3-4 ngày làm việc

## Ghi chú

- Sử dụng Python 13.3 cho tất cả các tiện ích
- Triển khai Lambda Layer giúp giảm kích thước của mỗi Lambda function và tái sử dụng code
- Sử dụng AWS Lambda Powertools để cải thiện logging, tracing và monitoring
- Đảm bảo xử lý lỗi thống nhất trong toàn bộ hệ thống
- Các tiện ích common cần được thiết kế để dễ dàng mở rộng và bảo trì 