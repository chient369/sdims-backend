**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-08-06 | Chiến Trần Văn | Định nghĩa chi tiết task API Gateway Integration Utilities | -           | Draft     |
| 1.1     | 2024-08-07 | Chiến Trần Văn | Cập nhật lại task sử dụng FastAPI và Mangum | -           | Draft     |
| 1.2     | 2024-08-07 | Chiến Trần Văn | Cập nhật cấu trúc file theo sys-structure | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết các công việc cần thực hiện để phát triển các tiện ích tích hợp API Gateway cho backend system, sử dụng FastAPI làm base framework và mở rộng các tính năng cần thiết cho business logic.

# Chi tiết Task: BE-CORE-006 - API Gateway Integration Utilities

## Thông tin chung

**Task ID:** BE-CORE-006  
**Task Name:** Phát triển API Gateway Integration Utilities với FastAPI  
**Độ ưu tiên:** Cao (High Priority)  
**Phụ thuộc vào:** BE-CORE-001, BE-CORE-003  
**Các task phụ thuộc vào task này:** Tất cả các Lambda functions API

## Mô tả

Task này tập trung vào việc thiết lập và cấu hình FastAPI framework để làm nền tảng cho các API Lambda functions, đồng thời phát triển các tiện ích bổ sung cần thiết cho business logic. Việc sử dụng FastAPI sẽ giúp tận dụng các tính năng có sẵn như validation, documentation, dependency injection, trong khi vẫn cho phép tùy chỉnh và mở rộng theo yêu cầu cụ thể của dự án.

## Chi tiết công việc

### 1. Thiết lập FastAPI Framework trong Lambda Layer

- [ ] Tạo common layer cho FastAPI và các dependencies:
  ```
  layers/
  └── common-layer/
      └── python/
          ├── requirements.txt  # FastAPI, Mangum và các dependencies
          └── common/
              └── api/
                  ├── __init__.py
                  ├── base.py    # FastAPI app configuration
                  ├── errors.py  # Error handlers
                  └── response.py # Response formatters
  ```

- [ ] Cấu hình FastAPI và Mangum trong base.py:
  ```python
  # layers/common-layer/python/common/api/base.py
  from fastapi import FastAPI
  from mangum import Mangum
  from fastapi.middleware.cors import CORSMiddleware
  
  def create_app():
      app = FastAPI(
          title="SDIMS API",
          description="Internal Management System API",
          version="1.0.0"
      )
      
      app.add_middleware(
          CORSMiddleware,
          allow_origins=["*"],  # Cấu hình theo environment
          allow_credentials=True,
          allow_methods=["*"],
          allow_headers=["*"],
      )
      
      return app
  
  app = create_app()
  handler = Mangum(app)
  ```

### 2. Phát triển Business Context Layer

- [ ] Tạo cấu trúc context trong common layer:
  ```
  layers/
  └── common-layer/
      └── python/
          └── common/
              └── context/
                  ├── __init__.py
                  ├── business.py  # Business context
                  └── request.py   # Request context
  ```

- [ ] Implement BusinessContext:
  ```python
  # layers/common-layer/python/common/context/business.py
  from fastapi import Request
  from typing import Optional, Dict, Any
  
  class BusinessContext:
      def __init__(self, request: Request):
          self.request = request
          self.user: Optional[Dict[str, Any]] = None
          self.permissions: list = []
          self._loaded = False
      
      async def load(self):
          if not self._loaded:
              await self._load_user()
              await self._load_permissions()
              self._loaded = True
  ```

### 3. Phát triển API Response Handlers

- [ ] Tạo response handlers trong common layer:
  ```python
  # layers/common-layer/python/common/api/response.py
  from typing import Optional, Dict, Any
  
  class APIResponse:
      @staticmethod
      def success(data: Any, message: Optional[str] = None, meta: Optional[Dict[str, Any]] = None):
          return {
              "status": "success",
              "data": data,
              "message": message,
              "meta": meta
          }
  ```

### 4. Phát triển Security Components

- [ ] Tạo security components trong common layer:
  ```
  layers/
  └── common-layer/
      └── python/
          └── common/
              └── security/
                  ├── __init__.py
                  ├── permissions.py  # Permission decorators
                  └── auth.py        # Authentication utilities
  ```

- [ ] Implement permission decorator:
  ```python
  # layers/common-layer/python/common/security/permissions.py
  from functools import wraps
  from fastapi import HTTPException
  
  def require_permissions(permissions: list):
      def decorator(func):
          @wraps(func)
          async def wrapper(context: BusinessContext, *args, **kwargs):
              await context.load()
              if not all(p in context.permissions for p in permissions):
                  raise HTTPException(status_code=403)
              return await func(context, *args, **kwargs)
          return wrapper
      return decorator
  ```

### 5. Phát triển Monitoring Components

- [ ] Tạo monitoring components trong common layer:
  ```
  layers/
  └── common-layer/
      └── python/
          └── common/
              └── monitoring/
                  ├── __init__.py
                  ├── logging.py   # Logging middleware
                  └── metrics.py   # CloudWatch metrics
  ```

- [ ] Implement logging middleware:
  ```python
  # layers/common-layer/python/common/monitoring/logging.py
  import time
  import logging
  from fastapi import Request
  
  logger = logging.getLogger("api")
  
  async def logging_middleware(request: Request, call_next):
      start_time = time.time()
      response = await call_next(request)
      duration = time.time() - start_time
      
      logger.info(
          "Request completed",
          extra={
              "path": request.url.path,
              "method": request.method,
              "duration": duration
          }
      )
      
      return response
  ```

### 6. Phát triển Testing Framework

- [ ] Tạo testing utilities:
  ```
  tests/
  ├── unit/
  │   └── common/
  │       └── api/
  │           ├── test_response.py
  │           └── test_context.py
  └── integration/
      └── api/
          └── test_endpoints.py
  ```

- [ ] Implement test client:
  ```python
  # tests/integration/api/test_client.py
  from fastapi.testclient import TestClient
  from typing import Dict, Any
  
  class APITestClient:
      def __init__(self, app):
          self.client = TestClient(app)
          self.token = None
  ```

### 7. Cập nhật Template SAM

- [ ] Cập nhật template.yaml để include common layer:
  ```yaml
  Resources:
    CommonLayer:
      Type: AWS::Serverless::LayerVersion
      Properties:
        LayerName: common-layer
        Description: Common utilities for API Gateway integration
        ContentUri: layers/common-layer/
        CompatibleRuntimes:
          - python3.13
        RetentionPolicy: Retain
  ```

### 8. Tạo Documentation

- [ ] Tạo documentation trong thư mục docs:
  ```
  docs/
  └── api/
      ├── setup.md       # Hướng dẫn setup
      ├── examples.md    # Ví dụ sử dụng
      └── reference.md   # API reference
  ```

## Ví dụ Sử dụng trong Lambda Function

```python
# src/hrm/employees.py
from common.api.base import app
from common.context import BusinessContext
from common.security.permissions import require_permissions
from common.api.response import APIResponse

@app.get("/employees")
@require_permissions(["employee:list"])
async def list_employees(context: BusinessContext, page: int = 1, limit: int = 20):
    await context.load()
    
    # Business logic here
    employees = await get_employees(page, limit)
    
    return APIResponse.success(
        data=employees,
        meta={
            "page": page,
            "limit": limit,
            "total": len(employees)
        }
    )
```

## Tiêu chí hoàn thành

1. Common layer được triển khai đầy đủ với FastAPI và các utilities
2. Tất cả các components được tổ chức theo đúng cấu trúc dự án
3. Permission system hoạt động hiệu quả
4. Error handling xử lý tất cả các trường hợp
5. Monitoring và logging được tích hợp
6. Test coverage đạt ít nhất 90%
7. Documentation đầy đủ và rõ ràng

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

1. Sử dụng FastAPI version 0.100.0 trở lên
2. Đảm bảo Mangum version tương thích với FastAPI
3. Cần test kỹ cold start time của Lambda với common layer
4. Tối ưu package size của layer
5. Cân nhắc sử dụng FastAPI background tasks cho các tác vụ async
6. Đảm bảo tất cả error responses tuân theo chuẩn định nghĩa trong api_errors_list.md 