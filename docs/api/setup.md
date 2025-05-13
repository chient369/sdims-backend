# API Gateway Integration Setup Guide

## Overview

Tài liệu này cung cấp hướng dẫn thiết lập và sử dụng API Gateway integration utilities với FastAPI và AWS Lambda. Các thành phần chính bao gồm:

- FastAPI framework cho phát triển API
- Mangum cho AWS Lambda integration 
- AWS Lambda Powertools cho logging và monitoring
- Custom middleware cho xử lý request/response
- JWT-based authentication

## Prerequisites

- Python 3.13
- AWS SAM CLI
- AWS CLI đã cấu hình với credentials phù hợp
- Docker (cho local testing)

## Installation

1. Cài đặt dependencies:
```bash
pip install -r layers/common-layer/python/requirements.txt
```

2. Cấu hình environment variables:
```bash
# Development
export ENVIRONMENT=dev
export LOG_LEVEL=DEBUG
export JWT_SECRET_KEY=your-secret-key
export ALLOWED_ORIGINS='["http://localhost:3000"]'

# Production
export ENVIRONMENT=prod
export LOG_LEVEL=INFO
export JWT_SECRET_KEY=$(aws secretsmanager get-secret-value --secret-id prod/jwt-secret --query SecretString --output text)
export ALLOWED_ORIGINS='["https://your-domain.com"]'
```

3. Deploy sử dụng SAM:
```bash
sam build
sam deploy --guided
```

## Project Structure

```
layers/
└── common-layer/
    └── python/
        ├── requirements.txt
        └── common/
            ├── api/
            │   ├── base.py      # FastAPI configuration
            │   ├── errors.py    # Error handlers
            │   └── response.py  # Response formatters
            ├── context/
            │   ├── business.py  # Business context
            │   └── request.py   # Request context
            └── monitoring/
                ├── logging.py   # Logging middleware
                └── metrics.py   # CloudWatch metrics
```

## Sử dụng Middleware

### 1. Request Logging Middleware

Middleware này tự động log thông tin request/response và thời gian xử lý:

```python
from common.monitoring.logging import RequestLoggingMiddleware

app = FastAPI()
app.add_middleware(RequestLoggingMiddleware)
```

### 2. Business Context Middleware

Middleware xử lý authentication và permissions:

```python
from common.context.business import get_business_context
from fastapi import Depends

@app.get("/api/v1/example")
async def example_endpoint(context: BusinessContext = Depends(get_business_context)):
    # Kiểm tra quyền
    context.require_permissions(["example:read"])
    
    # Lấy thông tin user
    user_id = context.user_id
    
    return APIResponse.success(data={"user_id": user_id})
```

### 3. Request Context Middleware

Middleware cung cấp thông tin về request và Lambda context:

```python
from common.context.request import get_request_context
from fastapi import Depends

@app.get("/api/v1/example")
async def example_endpoint(request_ctx: RequestContext = Depends(get_request_context)):
    # Lấy trace ID
    trace_id = request_ctx.trace_id
    
    # Lấy thông tin client
    client_ip = request_ctx.source_ip
    user_agent = request_ctx.user_agent
    
    return APIResponse.success(data={
        "trace_id": trace_id,
        "client_ip": client_ip
    })
```

### 4. Error Handling

Middleware xử lý lỗi theo chuẩn định nghĩa:

```python
from common.api.errors import NotFoundError, BusinessError, ValidationError

@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc):
    return await api_error_handler(request, exc)

@app.exception_handler(BusinessError)  
async def business_error_handler(request, exc):
    return await api_error_handler(request, exc)

@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc):
    return await api_error_handler(request, exc)
```

### 5. Metrics Middleware

Middleware thu thập metrics cho CloudWatch:

```python
from common.monitoring.metrics import request_metrics, business_metrics

# Record API metrics
request_metrics.record_request(
    path="/api/v1/example",
    method="GET", 
    status_code=200,
    duration=0.5
)

# Record business metrics
business_metrics.record_business_metric(
    name="OrdersCreated",
    value=1,
    unit="Count",
    context={
        "customer_type": "premium"
    }
)
```

## TODO List khi sử dụng Middleware

1. Authentication & Authorization:
- [ ] Cấu hình JWT secret key trong AWS Secrets Manager
- [ ] Implement logic load permissions từ DynamoDB trong BusinessContext
- [ ] Thêm cache cho permissions để giảm số lần query DynamoDB
- [ ] Xử lý refresh token
- [ ] Implement rate limiting cho API endpoints

2. Logging & Monitoring:
- [ ] Cấu hình log retention trong CloudWatch
- [ ] Thêm custom metrics cho business KPIs
- [ ] Setup alerts dựa trên metrics
- [ ] Implement distributed tracing với X-Ray
- [ ] Thêm correlation ID cho request tracking

3. Error Handling:
- [ ] Map tất cả business errors với error codes
- [ ] Implement global exception handler
- [ ] Thêm validation cho request parameters
- [ ] Xử lý graceful shutdown
- [ ] Setup error notifications

4. Security:
- [ ] Implement CORS policy theo environment
- [ ] Setup WAF rules
- [ ] Implement request sanitization
- [ ] Thêm audit logging
- [ ] Setup security headers

5. Performance:
- [ ] Optimize Lambda cold starts
- [ ] Implement caching strategy
- [ ] Configure Lambda concurrency
- [ ] Optimize layer size
- [ ] Setup performance monitoring

## Best Practices

1. Authentication & Authorization:
- Luôn sử dụng BusinessContext cho authentication
- Kiểm tra permissions trước khi thực hiện business logic
- Không hard-code JWT secret

2. Error Handling:
- Sử dụng error codes theo chuẩn định nghĩa
- Log đầy đủ thông tin lỗi
- Không expose internal errors ra response

3. Logging:
- Sử dụng log levels phù hợp
- Redact sensitive data
- Include request ID trong logs

4. Metrics:
- Thu thập metrics có ý nghĩa
- Setup alerts sớm
- Monitor Lambda performance

5. Security:
- Validate tất cả input
- Sử dụng HTTPS
- Follow least privilege principle

## Troubleshooting

1. Authentication Issues:
- Kiểm tra JWT token expiration
- Verify JWT secret key
- Check permissions configuration

2. Performance Issues:
- Monitor Lambda duration
- Check cold start frequency
- Analyze CloudWatch metrics

3. Error Handling:
- Review CloudWatch logs
- Check error response format
- Verify error codes

## Support

Khi gặp vấn đề:
1. Check CloudWatch logs
2. Review error responses
3. Contact development team 