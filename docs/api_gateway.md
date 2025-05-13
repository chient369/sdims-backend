# API Gateway Documentation

## Overview

API Gateway là cổng vào trung tâm cho tất cả các API endpoints của SDIMS. API Gateway cung cấp một số tính năng quan trọng:

- Authentication & Authorization thông qua Lambda Authorizer
- Cấu hình CORS để hỗ trợ frontend app
- Logging và monitoring
- Bảo mật thông qua WAF (Web Application Firewall)
- Rate limiting và throttling

## API Endpoints

Tất cả các API endpoints được bắt đầu với: `/api/v1/`

### Authentication Endpoints

| Phương thức | Endpoint | Mô tả | Authorization Required |
|-------------|----------|-------|------------------------|
| POST | `/api/v1/auth/login` | Đăng nhập và nhận JWT token | No |
| POST | `/api/v1/auth/logout` | Đăng xuất (hủy token) | Yes |
| POST | `/api/v1/auth/refresh-token` | Làm mới access token | No |
| GET | `/api/v1/auth/me` | Lấy thông tin user hiện tại | Yes |

### HRM Endpoints

| Phương thức | Endpoint | Mô tả | Authorization Required |
|-------------|----------|-------|------------------------|
| GET | `/api/v1/employees` | Lấy danh sách nhân viên | Yes |
| POST | `/api/v1/employees` | Thêm nhân viên mới | Yes (Admin/Manager) |
| GET | `/api/v1/employees/{employeeId}` | Lấy thông tin chi tiết nhân viên | Yes |
| PUT | `/api/v1/employees/{employeeId}` | Cập nhật thông tin nhân viên | Yes |
| DELETE | `/api/v1/employees/{employeeId}` | Xóa nhân viên | Yes (Admin/Manager) |

Tham khảo tài liệu API chi tiết cho các endpoints khác.

## Authentication

### JWT Authentication

API Gateway sử dụng Lambda Authorizer để xác thực JWT token từ header `Authorization`. Quy trình làm việc:

1. Client gửi request `POST /api/v1/auth/login` với username và password
2. Nhận JWT token trong response
3. Thêm JWT token vào header `Authorization: Bearer {token}` cho các requests sau đó
4. Khi token hết hạn, sử dụng refresh token để lấy token mới qua `POST /api/v1/auth/refresh-token`

### Lambda Authorizer

Lambda Authorizer xử lý việc xác thực và phân quyền:

1. Trích xuất JWT token từ header Authorization
2. Xác thực JWT token sử dụng secret key
3. Trích xuất payload user và vai trò từ token
4. Tạo IAM policy document cho phép/từ chối truy cập
5. Chuyển thông tin user vào context được truyền đến Lambda function

## CORS

API Gateway được cấu hình với CORS để hỗ trợ frontend app từ origin `https://${WebsiteDomainName}`. Các thiết lập CORS:

- AllowMethods: GET, POST, PUT, DELETE, OPTIONS
- AllowHeaders: Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token
- AllowOrigin: Chỉ từ frontend domain
- AllowCredentials: true (cho phép cookies và credentials)

## Logging và Monitoring

API Gateway được cấu hình để ghi log truy cập vào CloudWatch Logs. Format log bao gồm:

- Request ID
- Source IP
- Caller information
- HTTP method
- Resource path
- Status code
- Response length
- Timestamp

## Web Application Firewall (WAF)

API Gateway được bảo vệ bởi AWS WAF với các rule sets:

- AWSManagedRulesCommonRuleSet: Bảo vệ chống lại các lỗ hổng web phổ biến
- AWSManagedRulesSQLiRuleSet: Bảo vệ chống lại SQL injection attacks

## Custom Domain (Tùy chọn)

API Gateway hỗ trợ custom domain `api.${WebsiteDomainName}` (cần SSL certificate). Điều này cho phép endpoints được truy cập thông qua:
- https://api.example.com/api/v1/...

## Triển khai và Tests

API Gateway được triển khai qua CloudFormation/SAM. Để triển khai:

```bash
sam build
sam deploy --guided
```

Để test API Gateway:

```bash
# Test login
curl -X POST https://api.example.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin", "password":"password"}'

# Test protected endpoint
curl -X GET https://api.example.com/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
``` 