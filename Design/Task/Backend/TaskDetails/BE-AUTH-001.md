**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function đăng nhập | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function xử lý xác thực người dùng (login) và tạo JWT token cho người dùng.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-AUTH-001  
**Task Name:** Triển khai Lambda function đăng nhập  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Service authentication và authorization)

**Các task phụ thuộc vào task này:** 
- BE-AUTH-002 (Phát triển Lambda function đăng xuất)
- BE-AUTH-003 (Lấy thông tin người dùng hiện tại)
- BE-AUTH-004 (Làm mới token)

**Các API:**
- API-AUTH-001: POST /api/v1/auth/login

## Mô tả

Task này tập trung vào việc triển khai Lambda function xử lý quá trình đăng nhập của người dùng, bao gồm:
- Xác thực người dùng dựa trên username/email và password
- Tạo JWT token (access token và refresh token) khi xác thực thành công
- Xử lý các trường hợp lỗi như tài khoản không tồn tại, sai mật khẩu, tài khoản bị khóa
- Lưu thông tin đăng nhập vào hệ thống để tracking

Kết quả đầu ra là một hàm Lambda được triển khai và tích hợp với API Gateway, có khả năng xác thực người dùng, tạo JWT token và xử lý các trường hợp lỗi phù hợp.

## Chi tiết công việc

### Triển khai Lambda function login

- [ ] Tạo Lambda function cho endpoint đăng nhập:
  - Location: src/auth/login.py
  - Định nghĩa handler function với cấu trúc chuẩn của AWS Lambda
  - Thiết lập input validation cho request body (username/email và password)
  - Tích hợp với middleware xử lý lỗi và response format

### Xây dựng logic xác thực

- [ ] Triển khai logic xác thực người dùng:
  - Location: src/auth/login.py và src/common/auth.py
  - Cài đặt kết nối với DynamoDB để truy xuất thông tin người dùng (qua GSI1 hoặc GSI2 của entity USER)
  - Thực hiện so sánh password hash với thông tin đã lưu
  - Kiểm tra trạng thái tài khoản (is_active, số lần đăng nhập sai)
  - Cập nhật thông tin last_login_at trong DynamoDB khi đăng nhập thành công

### Tạo và quản lý JWT token

- [ ] Phát triển logic tạo JWT tokens:
  - Location: src/common/auth.py
  - Cài đặt và cấu hình thư viện xử lý JWT (PyJWT)
  - Tạo access token chứa thông tin người dùng và quyền truy cập (từ entity ROLE và PERMISSION)
  - Tạo refresh token với thời gian sống dài hơn
  - Đảm bảo tính bảo mật bằng cách sử dụng secret key được cấu hình từ AWS Systems Manager Parameter Store

### Xử lý lỗi và response

- [ ] Triển khai xử lý các trường hợp lỗi:
  - Location: src/auth/login.py
  - Xử lý lỗi xác thực (username/email không tồn tại, sai mật khẩu)
  - Xử lý lỗi tài khoản bị khóa
  - Xử lý lỗi đăng nhập thất bại quá nhiều lần
  - Định dạng response theo chuẩn hệ thống (sử dụng mã lỗi từ tài liệu api_errors_list.md)

### Phát triển Unit Tests

- [ ] Phát triển unit tests cho function login:
  - Location: tests/unit/auth/test_login.py
  - Test xác thực thành công
  - Test xác thực thất bại (sai username/password)
  - Test tài khoản bị khóa
  - Test đăng nhập thất bại quá nhiều lần
  - Test validation lỗi input
  - Mocking DynamoDB cho việc testing

### Tạo Documentation

- [ ] Tài liệu API specification:
  - Cập nhật Swagger/OpenAPI documentation cho endpoint login
  - Mô tả request/response format
  - Liệt kê các mã lỗi có thể xảy ra

- [ ] Tài liệu technical implementation:
  - Mô tả chi tiết về cách JWT token được tạo
  - Hướng dẫn cấu hình secret keys và các tham số liên quan
  - Thời gian sống của token và cách quản lý

## Ví dụ cách sử dụng cuối cùng

Request:
```json
// POST /api/v1/auth/login
{
  "username": "user@example.com",
  "password": "Password123"
}
```

Response thành công:
```json
{
  "status": "success",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 3600,
    "user": {
      "id": "123",
      "username": "user@example.com",
      "fullName": "Nguyễn Văn A",
      "role": "Admin",
      "permissions": ["user:read", "user:write"]
    }
  }
}
```

Response lỗi:
```json
{
  "status": "error",
  "code": "E1005",
  "message": "Sai tên đăng nhập hoặc mật khẩu"
}
```

## Tiêu chí hoàn thành

1. Lambda function login hoạt động chính xác và được triển khai thành công
2. Xác thực người dùng đúng thông tin từ DynamoDB
3. JWT tokens được tạo đúng format và chứa đầy đủ thông tin cần thiết
4. Tất cả các trường hợp lỗi được xử lý phù hợp theo chuẩn API errors
5. Unit tests đạt coverage > 80%
6. Documentation đầy đủ (Swagger/OpenAPI và technical implementation)
7. Đảm bảo tính bảo mật của mật khẩu và JWT tokens

## Ước tính thời gian

- 2-3 ngày làm việc

## Ghi chú

- JWT secret key phải được lưu trữ an toàn trong AWS Systems Manager Parameter Store hoặc AWS Secrets Manager
- Cần cấu hình thời gian sống của token hợp lý (access token: 1 giờ, refresh token: 7 ngày)
- Cần tránh lưu sensitive information như password và token trong logs
- Sử dụng thuật toán mã hóa mạnh (bcrypt) cho password và bảo vệ chống brute force attacks
- Nên triển khai rate limiting để ngăn chặn các nỗ lực tấn công brute-force login 