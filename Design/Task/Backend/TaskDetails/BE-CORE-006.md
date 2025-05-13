**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-06 | Chiến Trần Văn | Định nghĩa chi tiết task API Gateway Integration Utilities | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để phát triển các tiện ích tích hợp API Gateway cho backend system. Các tiện ích này sẽ chuẩn hóa việc xử lý request và response giữa API Gateway và Lambda functions.

# Chi tiết Task: BE-CORE-006 - API Gateway Integration Utilities

## Thông tin chung

**Task ID:** BE-CORE-006  
**Task Name:** Phát triển API Gateway Integration Utilities  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** BE-CORE-001, BE-CORE-003  
**Các task phụ thuộc vào task này:** Tất cả các Lambda functions API

## Mô tả

Task này bao gồm việc phát triển các tiện ích để chuẩn hóa và đơn giản hóa tương tác giữa API Gateway và Lambda functions. Các tiện ích này sẽ xử lý parse và transform request từ API Gateway, cũng như format response trả về. Việc triển khai các tiện ích này giúp giảm code trùng lặp trong các Lambda handlers, đảm bảo xử lý request/response nhất quán, và hỗ trợ các tính năng như request context, tracing, và error handling.

## Chi tiết công việc

### Thiết kế API Gateway Handler Framework

- [ ] Thiết kế framework tổng thể cho API Gateway integration:
  - Xác định kiến trúc và luồng xử lý request/response
  - Tạo mô hình lambda handler decorator
  - Thiết kế cơ chế middleware để xử lý cross-cutting concerns
  - Đảm bảo tích hợp với các module khác (validation, authentication, event bus)

### Xây dựng Request Parser Component

- [ ] Phát triển các tiện ích parse request API Gateway:
  - Xử lý và chuẩn hóa các loại event từ API Gateway (REST API, HTTP API)
  - Parse path parameters, query string parameters, và headers
  - Xử lý request body với nhiều content types (application/json, form data, etc.)
  - Parse và xác thực JWT tokens từ Authorization header
  - Xử lý multipart/form-data cho file uploads
  - Đảm bảo xử lý các trường hợp đặc biệt (null values, encoded characters, etc.)

### Xây dựng Response Formatter Component

- [ ] Phát triển các tiện ích format response:
  - Tạo cấu trúc response chuẩn (status, body, headers)
  - Hỗ trợ các content types khác nhau
  - Xử lý response pagination
  - Đảm bảo CORS headers
  - Xử lý binary responses
  - Tối ưu hóa kích thước response cho API Gateway

### Phát triển API Handler Decorator

- [ ] Xây dựng decorator `@api_handler` cho Lambda functions:
  - Tự động parse request
  - Tích hợp với validation framework (BE-CORE-003)
  - Xử lý authentication và authorization
  - Tích hợp error handling
  - Request logging and tracing
  - Tích hợp với CloudWatch metrics
  - Xử lý các trường hợp đặc biệt (warm start, cold start, timeout)

### Xây dựng API Middleware System

- [ ] Phát triển hệ thống middleware:
  - Tạo middleware framework cho các Lambda handlers
  - Xây dựng các middleware phổ biến:
    - Authentication middleware
    - Logging middleware
    - Tracing middleware
    - Rate limiting middleware
    - Request/response transformation middleware
  - Cơ chế đăng ký và sắp xếp thứ tự middleware
  - Tích hợp middleware vào API handler decorator

### Xây dựng Request Context

- [ ] Phát triển lớp RequestContext:
  - Lưu trữ thông tin về request hiện tại
  - Lưu trữ thông tin về user đã xác thực
  - Cung cấp các helpers cho access control
  - Tích hợp với DynamoDB để load thêm data khi cần
  - Cơ chế lưu trữ và truy xuất dữ liệu context trong quá trình xử lý request

### Phát triển API Security Utilities

- [ ] Triển khai các tiện ích bảo mật API:
  - Cơ chế validate và verify tokens
  - CSRF protection (nếu cần)
  - Rate limiting implementation
  - IP filtering helpers
  - Tích hợp với WAF (nếu cần)
  - Xử lý OAuth 2.0 flows (nếu cần)

### Phát triển API Versioning Support

- [ ] Xây dựng cơ chế hỗ trợ versioning API:
  - Content negotiation (`Accept` header)
  - URL path versioning (`/v1/resource`)
  - Query parameter versioning (`?version=1`)
  - Content-Type header versioning
  - Backward compatibility helpers

### Xây dựng API Documentation Utilities

- [ ] Phát triển tiện ích tự động tạo API documentation:
  - Tự động generate OpenAPI/Swagger documentation
  - Tích hợp với API handler decorators
  - Trích xuất validation schemas làm API schemas
  - Cập nhật documentation khi code thay đổi

### Phát triển Testing Utilities

- [ ] Xây dựng các tiện ích để test API:
  - Local invocation của API handlers
  - Mocking API Gateway events
  - Unit và integration testing helpers
  - API verification utils
  - Load testing helpers

### Viết Unit Tests

- [ ] Phát triển test suites cho API Gateway Integration Utilities:
  - Tests cho Request Parser
  - Tests cho Response Formatter
  - Tests cho API Handler Decorator
  - Tests cho Middleware System
  - Tests cho Security Utilities
  - Tests cho các use cases phổ biến

### Tạo Documentation và Examples

- [ ] Phát triển documentation và examples:
  - API documentation cho tất cả các components
  - Hướng dẫn sử dụng API Handler Decorator
  - Hướng dẫn tạo custom middlewares
  - Best practices cho API development
  - Các templates và starter code

## Ví dụ cách sử dụng cuối cùng

Dưới đây là ví dụ về cách mong muốn sử dụng API Gateway Integration Utilities khi hoàn thành:

### Defining an API Handler

```python
from common.api import api_handler, RequestContext
from common.validation import StringRule, IntegerRule
from common.models import Employee

# Định nghĩa schema validation cho API
employee_list_schema = {
    "query_string": {
        "page": IntegerRule(min_value=1, default=1),
        "limit": IntegerRule(min_value=1, max_value=100, default=20),
        "search": StringRule(max_length=100),
        "department": StringRule(max_length=50),
        "status": StringRule(enum=["active", "inactive", "all"])
    }
}

# Sử dụng api_handler decorator
@api_handler(
    path="/employees",
    method="GET",
    schema=employee_list_schema,
    requires_auth=True,
    permissions=["employee:list"]
)
def list_employees(context: RequestContext):
    """
    List employees API handler
    
    RequestContext đã chứa thông tin được parse từ API Gateway event
    """
    # Access parsed and validated query parameters
    page = context.query_params.get("page")
    limit = context.query_params.get("limit")
    search = context.query_params.get("search")
    department = context.query_params.get("department")
    status = context.query_params.get("status", "active")
    
    # Access authenticated user info
    current_user = context.user
    
    # Use DynamoDB Repository
    from common.dynamodb import DynamoDBRepository
    repo = DynamoDBRepository()
    
    # Build query parameters based on filters
    query_params = {
        "IndexName": "GSI1",
        "KeyConditionExpression": "GSI1PK = :pk",
        "ExpressionAttributeValues": {
            ":pk": "EMPLOYEE"
        }
    }
    
    if status != "all":
        query_params["FilterExpression"] = "employee_status = :status"
        query_params["ExpressionAttributeValues"][":status"] = status
    
    if department:
        if "FilterExpression" in query_params:
            query_params["FilterExpression"] += " AND department = :dept"
        else:
            query_params["FilterExpression"] = "department = :dept"
        query_params["ExpressionAttributeValues"][":dept"] = department
        
    # Calculate pagination
    offset = (page - 1) * limit
    
    # Execute query
    result = repo.query(**query_params)
    
    # Process items
    items = result.get("Items", [])
    total = len(items)  # In a real app, you would get the total count differently
    
    # Apply pagination in memory (in a real app, you would use LastEvaluatedKey)
    paginated_items = items[offset:offset+limit]
    
    # Return results - api_handler automatically formats the response
    return {
        "items": paginated_items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    }
```

### Creating a Custom Middleware

```python
from common.api import Middleware, RequestContext, NextHandler
import time
import uuid

class PerformanceMiddleware(Middleware):
    """
    Middleware to track API performance
    """
    
    async def process(self, context: RequestContext, next_handler: NextHandler):
        # Generate request ID if not exists
        if "X-Request-ID" not in context.headers:
            request_id = str(uuid.uuid4())
            context.set_header("X-Request-ID", request_id)
        
        # Record start time
        start_time = time.time()
        
        # Call next middleware or handler
        response = await next_handler(context)
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Add execution time to response headers
        response.headers["X-Execution-Time"] = f"{execution_time * 1000:.2f}ms"
        
        # Log performance metrics
        context.logger.info(
            "API Performance",
            extra={
                "path": context.path,
                "method": context.method,
                "execution_time_ms": execution_time * 1000,
                "request_id": context.headers.get("X-Request-ID")
            }
        )
        
        return response
```

### Registering Middlewares

```python
from common.api import ApiGatewayHandler, LoggingMiddleware, AuthMiddleware, PerformanceMiddleware

# Create handler with middlewares
handler = ApiGatewayHandler(
    middlewares=[
        LoggingMiddleware(),
        PerformanceMiddleware(),
        AuthMiddleware(jwt_secret="your-secret-here"),
        # Add more middlewares as needed
    ]
)

# Lambda handler function
def lambda_handler(event, context):
    return handler.handle(event, context)
```

## Tiêu chí hoàn thành

- API Gateway Integration Utilities được thiết kế và phát triển đầy đủ
- API Handler Decorator hoạt động chính xác với tất cả các tính năng
- Middleware System được triển khai và có thể mở rộng
- Request Parser và Response Formatter xử lý tất cả các use cases
- Security utilities được triển khai đầy đủ
- Tất cả các components được unit test kỹ lưỡng
- Documentation và examples được tạo

## Ước tính thời gian

- 4-5 ngày làm việc

## Ghi chú

- Tiện ích nên hỗ trợ cả API Gateway REST API và HTTP API
- Cần đảm bảo hiệu suất tối ưu, đặc biệt là cold start time
- Cần xem xét backward compatibility khi update các utilities này
- Documentation là vô cùng quan trọng vì tất cả các API sẽ sử dụng tiện ích này
- Cần có cơ chế để debug và troubleshoot khi có vấn đề
- Nên thiết kế để dễ dàng tích hợp với các tools khác như X-Ray, AppSync, etc. 