**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-07-28 | AI Assistant | Tạo quy tắc triển khai task | -           | Draft     |

---

## 1. Mục tiêu  
Tài liệu này định nghĩa các quy tắc cụ thể cho việc triển khai từng loại task trong dự án serverless SDIMS, nhằm đảm bảo tính nhất quán và chất lượng cao trong toàn bộ codebase.

---

## 2. Quy tắc chung cho mọi task

### 2.1. Quy tắc git
- Tạo branch riêng cho mỗi API với format: `feature/BE-<Task-ID>-<short-description>`
- Commit message phải có task ID: `feat(BE-xxx): implement xxx function`
- Không commit trực tiếp vào branch main
- Pull request phải được review bởi ít nhất 1 người

### 2.2. Coding style
- Tuân thủ PEP 8 cho Python
- Sử dụng 4 spaces cho indentation
- Maximum line length: 100 characters
- Đặt tên biến/hàm theo snake_case
- Đặt tên class theo PascalCase
- Docstring theo Google style (tiếng Anh)
- Comment code phức tạp (tiếng Anh)

### 2.3. Logging
- Sử dụng aws_lambda_powertools.Logger
- Log level phù hợp:
  - ERROR: Lỗi ảnh hưởng đến chức năng
  - INFO: Thông tin quan trọng vận hành
  - DEBUG: Chi tiết kỹ thuật (chỉ dùng trong dev)
- Không log thông tin nhạy cảm (token, password)

### 2.4. Error handling
- Sử dụng custom exception từ common.errors
- Phân loại lỗi theo API errors list
- Catch specific exception, tránh bare except
- Return HTTP status code phù hợp

---

## 3. Quy tắc cho từng loại task

### 3.1. Định nghĩa model

```python
# Ví dụ mẫu
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Employee:
    employee_id: str
    name: str
    email: str  
    department: str
    position: str
    manager_id: Optional[str] = None
    hire_date: datetime = None
    is_active: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Employee":
        return cls(
            employee_id=data.get("employee_id"),
            name=data.get("name"),
            email=data.get("email"),
            department=data.get("department"),
            position=data.get("position"),
            manager_id=data.get("manager_id"),
            hire_date=datetime.fromisoformat(data.get("hire_date")) if data.get("hire_date") else None,
            is_active=data.get("is_active", True)
        )
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "position": self.position,
            "manager_id": self.manager_id,
            "hire_date": self.hire_date.isoformat() if self.hire_date else None,
            "is_active": self.is_active
        }
```

#### Quy tắc:
- Sử dụng dataclass hoặc Pydantic model
- Type hints đầy đủ cho tất cả các field
- Implement từ_dict và to_dict method
- Khai báo field mặc định cuối cùng
- Mapping chính xác với cấu trúc DynamoDB
- Tên model phải rõ ràng, phản ánh entity

### 3.2. Tạo repository

```python
# Ví dụ mẫu
from typing import Dict, List, Optional, Any
from botocore.exceptions import ClientError
from common.errors import DatabaseError, NotFoundException
from logger import get_logger

class EmployeeRepository:
    def __init__(self, table_name: str, dynamodb_client=None):
        self.table_name = table_name
        self.dynamodb = dynamodb_client or boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)
        self.logger = get_logger(__name__)
        
    def get_all(self, limit: int = 20, last_evaluated_key: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            params = {
                "Limit": limit
            }
            if last_evaluated_key:
                params["ExclusiveStartKey"] = last_evaluated_key
                
            response = self.table.scan(**params)
            return {
                "items": response.get("Items", []),
                "last_evaluated_key": response.get("LastEvaluatedKey")
            }
        except ClientError as e:
            self.logger.error(f"Failed to get all employees: {str(e)}")
            raise DatabaseError("Failed to retrieve employees") from e
            
    def get_by_id(self, employee_id: str) -> Dict[str, Any]:
        try:
            response = self.table.get_item(Key={"employee_id": employee_id})
            if "Item" not in response:
                raise NotFoundException(f"Employee with ID {employee_id} not found")
            return response["Item"]
        except ClientError as e:
            self.logger.error(f"Failed to get employee {employee_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve employee {employee_id}") from e
            
    def create(self, employee: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.table.put_item(Item=employee)
            return employee
        except ClientError as e:
            self.logger.error(f"Failed to create employee: {str(e)}")
            raise DatabaseError("Failed to create employee") from e
```

#### Quy tắc:
- Repository chỉ chứa logic truy cập database
- Không chứa business logic
- Catch và log tất cả database exceptions
- Trả về custom exceptions
- Method names rõ ràng (get_*, create_*, update_*, delete_*)
- Đặt tham số paginate, query mặc định hợp lý
- Dùng index thích hợp cho các truy vấn phổ biến
- Tối ưu hóa RCU/WCU

### 3.3. Tạo service

```python
# Ví dụ mẫu
from typing import Dict, List, Optional, Any
from common.errors import BusinessLogicError, ValidationError
from models.employee import Employee
from repositories.employee_repository import EmployeeRepository
from logger import get_logger

class EmployeeService:
    def __init__(self, employee_repository: Optional[EmployeeRepository] = None):
        self.repository = employee_repository or EmployeeRepository(table_name="employees-table")
        self.logger = get_logger(__name__)
        
    def get_employees(self, page_size: int = 20, page_token: Optional[str] = None,
                      filters: Optional[Dict] = None) -> Dict[str, Any]:
        # Xử lý business logic
        last_key = self._decode_page_token(page_token) if page_token else None
        
        # Xử lý filters nếu có
        filter_params = {}
        if filters:
            # Logic xử lý filters
            pass
            
        # Gọi repository
        result = self.repository.get_all(limit=page_size, last_evaluated_key=last_key)
        
        # Convert từ dict database sang model
        employees = [Employee.from_dict(item) for item in result["items"]]
        
        # Tạo next_page_token nếu có
        next_token = self._encode_page_token(result["last_evaluated_key"]) if result.get("last_evaluated_key") else None
        
        return {
            "items": [emp.to_dict() for emp in employees],
            "next_page_token": next_token,
            "count": len(employees)
        }
```

#### Quy tắc:
- Service chỉ chứa business logic
- Không truy cập database trực tiếp, chỉ qua repository
- Xác thực input trước khi xử lý
- Convert giữa model và DTO
- Handling pagination
- Tất cả logic phải có error handling
- Unit test đầy đủ

### 3.4. Tạo Lambda handler

```python
# Ví dụ mẫu
import json
from typing import Dict, Any
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from common.errors import BaseError, ValidationError, AuthorizationError
from common.models import APIResponse
from services.employee_service import EmployeeService

logger = Logger()
tracer = Tracer()
app = APIGatewayRestResolver()
employee_service = EmployeeService()

@app.get("/employees")
@tracer.capture_method
def get_employees():
    try:
        # Lấy query parameters
        page_size = app.current_event.query_string_parameters.get("page_size", "20")
        page_token = app.current_event.query_string_parameters.get("page_token")
        
        # Xác thực input
        try:
            page_size = int(page_size)
            if page_size < 1 or page_size > 100:
                raise ValidationError("page_size must be between 1 and 100")
        except ValueError:
            raise ValidationError("Invalid page_size, must be integer")
            
        # Xác thực quyền
        current_user = app.current_event.request_context.authorizer.get("claims", {})
        permissions = current_user.get("permissions", [])
        
        if "employee:read:all" not in permissions:
            raise AuthorizationError("Insufficient permissions to list employees")
            
        # Gọi service
        result = employee_service.get_employees(page_size=page_size, page_token=page_token)
        
        # Trả về response
        return APIResponse.success(
            status_code=200,
            data=result
        ).to_dict()
    except BaseError as e:
        logger.error(f"Error in get_employees: {str(e)}")
        return APIResponse.error(
            status_code=e.status_code,
            message=str(e),
            error_code=e.error_code
        ).to_dict()
    except Exception as e:
        logger.error(f"Unexpected error in get_employees: {str(e)}")
        return APIResponse.error(
            status_code=500,
            message="Internal server error",
            error_code="INTERNAL_ERROR"
        ).to_dict()

@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    return app.resolve(event, context)
```

#### Quy tắc:
- Sử dụng APIGatewayRestResolver
- Validate tất cả input trước khi xử lý
- Kiểm tra quyền đầy đủ
- Lambda hạn chế xử lý business logic, chỉ gọi service
- Trả về response theo format chuẩn
- Sử dụng Lambda Powertools cho logging và tracing
- Xử lý tất cả exception gracefully

### 3.5. Validate input

```python
# Ví dụ mẫu với Pydantic
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional

class CreateEmployeeRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    department: str = Field(..., min_length=2, max_length=50)
    position: str = Field(..., min_length=2, max_length=50)
    manager_id: Optional[str] = None
    
    @validator('name')
    def name_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v
    
    @validator('department')
    def department_must_be_valid(cls, v):
        valid_departments = ['IT', 'HR', 'Finance', 'Marketing', 'Sales']
        if v not in valid_departments:
            raise ValueError(f'Department must be one of: {", ".join(valid_departments)}')
        return v

# Sử dụng trong handler
@app.post("/employees")
def create_employee():
    try:
        body = app.current_event.json_body
        
        # Validate input
        try:
            request_data = CreateEmployeeRequest(**body)
        except ValidationError as e:
            return APIResponse.error(
                status_code=400,
                message="Invalid request data",
                error_code="VALIDATION_ERROR",
                errors=e.errors()
            ).to_dict()
        
        # Tiếp tục xử lý với dữ liệu đã validate
        employee = employee_service.create_employee(request_data.dict())
        
        return APIResponse.success(
            status_code=201,
            data=employee
        ).to_dict()
    except Exception as e:
        # Error handling
```

#### Quy tắc:
- Sử dụng Pydantic hoặc Marshmallow
- Validate cả kiểu dữ liệu và business rules
- Custom validators cho logic phức tạp
- Trả về lỗi validation chi tiết
- Bổ sung các ràng buộc như min/max length

### 3.6. Xử lý phân quyền

```python
# Ví dụ mẫu
from common.errors import AuthorizationError

def authorize(required_permissions, authorizer_claims):
    user_permissions = authorizer_claims.get("permissions", [])
    
    # Check có permission chính xác không
    for permission in required_permissions:
        if permission in user_permissions:
            return True
            
    # Nếu không có quyền, check xem có phải quyền có scope không
    for required in required_permissions:
        if required.endswith(":all"):
            # Nếu yêu cầu quyền :all nhưng user có :own hoặc :team
            base_permission = required.replace(":all", "")
            if f"{base_permission}:own" in user_permissions or f"{base_permission}:team" in user_permissions:
                return True
                
    # Không có quyền phù hợp
    return False

# Sử dụng trong handler
@app.get("/employees/{employee_id}")
def get_employee(employee_id):
    try:
        # Lấy thông tin user từ token
        claims = app.current_event.request_context.authorizer.get("claims", {})
        user_id = claims.get("sub")
        
        # Xác định required permissions
        required_permissions = ["employee:read:all"]
        
        # Kiểm tra quyền
        if not authorize(required_permissions, claims):
            # Kiểm tra xem có phải nhân viên đang xem chính mình không
            employee = employee_service.get_employee_by_id(employee_id)
            if employee.get("employee_id") != user_id and "employee:read:own" in claims.get("permissions", []):
                raise AuthorizationError("You don't have permission to view this employee")
            
        # Gọi service
        employee = employee_service.get_employee_by_id(employee_id)
        
        return APIResponse.success(
            status_code=200,
            data=employee
        ).to_dict()
    except Exception as e:
        # Error handling
```

#### Quy tắc:
- Check quyền trước khi thực hiện bất kỳ thao tác nào
- Implement phân quyền theo BD/permissions_definition.md
- Phân biệt rõ các scope (all/team/own)
- Quyền phải được check ở tất cả API cần xác thực
- Đối với quyền :own, phải kiểm tra resource ownership

### 3.7. Logging và error handling

```python
# Ví dụ mẫu
from aws_lambda_powertools import Logger
from common.errors import BaseError, NotFoundException, DatabaseError

logger = Logger(service="employee-service")

@app.get("/employees/{employee_id}")
def get_employee(employee_id):
    logger.info(f"Request to get employee with ID: {employee_id}")
    try:
        # Validate input
        if not employee_id or len(employee_id) < 5:
            logger.warning(f"Invalid employee ID format: {employee_id}")
            return APIResponse.error(
                status_code=400,
                message="Invalid employee ID format",
                error_code="VALIDATION_ERROR"
            ).to_dict()
            
        # Kiểm tra quyền (code bỏ qua)
        
        # Gọi service
        try:
            employee = employee_service.get_employee_by_id(employee_id)
            logger.info(f"Successfully retrieved employee with ID: {employee_id}")
            return APIResponse.success(
                status_code=200,
                data=employee
            ).to_dict()
        except NotFoundException as e:
            logger.warning(f"Employee not found: {employee_id}")
            return APIResponse.error(
                status_code=404,
                message=str(e),
                error_code="RESOURCE_NOT_FOUND"
            ).to_dict()
        except DatabaseError as e:
            logger.error(f"Database error when retrieving employee {employee_id}: {str(e)}")
            return APIResponse.error(
                status_code=500,
                message="Failed to retrieve employee data",
                error_code="DATABASE_ERROR"
            ).to_dict()
    except BaseError as e:
        logger.error(f"Known error in get_employee: {e.error_code} - {str(e)}")
        return APIResponse.error(
            status_code=e.status_code,
            message=str(e),
            error_code=e.error_code
        ).to_dict()
    except Exception as e:
        logger.error(f"Unexpected error in get_employee: {str(e)}", exc_info=True)
        return APIResponse.error(
            status_code=500,
            message="Internal server error",
            error_code="INTERNAL_ERROR"
        ).to_dict()
```

#### Quy tắc:
- Sử dụng Lambda Powertools cho logging
- Log ở mức độ phù hợp (INFO, ERROR, WARNING)
- Không log thông tin nhạy cảm
- Sử dụng custom exceptions, tránh generic exceptions
- Catch từng loại exception riêng biệt
- Trả về mã lỗi HTTP phù hợp
- Error response có error_code rõ ràng


### 3.8. Cập nhật template.yaml

```yaml
# Ví dụ mẫu
Resources:
  # Lambda function
  GetEmployeesFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: handlers/employee_handler.lambda_handler
      Runtime: python3.13
      Architectures:
        - x86_64
      MemorySize: 128
      Timeout: 5
      Environment:
        Variables:
          EMPLOYEES_TABLE: !Ref EmployeesTable
          LOG_LEVEL: INFO
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref EmployeesTable
      Events:
        GetEmployees:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /employees
            Method: get
            Auth:
              Authorizer: LambdaTokenAuthorizer
      Layers:
        - !Ref CommonLayer
        - !Ref RepositoryLayer

  # DynamoDB Table
  EmployeesTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: employees-table
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: employee_id
          AttributeType: S
        - AttributeName: department
          AttributeType: S
      KeySchema:
        - AttributeName: employee_id
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: DepartmentIndex
          KeySchema:
            - AttributeName: department
              KeyType: HASH
          Projection:
            ProjectionType: ALL
```

#### Quy tắc:
- Function name phải có prefix từ API ID (GetEmployeesFunction)
- Đặt memory và timeout phù hợp (thường 128MB, 5s)
- IAM policy tuân theo least privilege
- Đảm bảo path/method khớp với API design
- Authorizer cho tất cả API yêu cầu xác thực
- Khai báo đủ environment variables
- Thêm đúng các layers cần thiết

### 3.9. Cập nhật documentation

#### Quy tắc:
- Cập nhật checklist tiến độ khi hoàn thành task  . `Task\TaskStatus\API-development-status.md`