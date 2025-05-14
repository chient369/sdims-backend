**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-07-28 | AI Assistant | Tài liệu triển khai API đăng nhập | -           | Draft     |

---

## 1. Mục tiêu  
Tài liệu triển khai chi tiết API đăng nhập (API-AUTH-001) cho hệ thống SDIMS, đảm bảo theo đúng thiết kế và đạt các yêu cầu đã định nghĩa.

---

## 2. Các thành phần đã triển khai

### 2.1. Models
- **User**: Model đại diện cho người dùng, map với entity USER trong DynamoDB
  - File: `src/layers/commonLayer/python/common/models/user.py`
  - Chức năng: Biểu diễn đối tượng người dùng và chuyển đổi giữa object và dictionary

- **Role**: Model đại diện cho vai trò người dùng, map với entity ROLE trong DynamoDB
  - File: `src/layers/commonLayer/python/common/models/role.py`
  - Chức năng: Biểu diễn đối tượng vai trò và chuyển đổi giữa object và dictionary

- **APIResponse**: Model chuẩn hóa format response API
  - File: `src/layers/commonLayer/python/common/models/api_response.py`
  - Chức năng: Đảm bảo format nhất quán cho response API

### 2.2. Errors
- **BaseError và các error cụ thể**: Hệ thống các exception xử lý lỗi
  - File: `src/layers/commonLayer/python/common/errors/__init__.py`
  - Chức năng: Đưa ra các exception tương ứng với các trường hợp lỗi khác nhau

### 2.3. Utils
- **password_utils**: Utility xử lý mật khẩu
  - File: `src/layers/commonLayer/python/common/utils/password_utils.py`
  - Chức năng: Băm và xác thực mật khẩu sử dụng PBKDF2 với SHA-256

- **jwt_utils**: Utility xử lý JWT
  - File: `src/layers/commonLayer/python/common/utils/jwt_utils.py`
  - Chức năng: Tạo, xác thực và kiểm tra JWT token

### 2.4. Repository
- **BaseRepository**: Lớp cơ sở cho các repository
  - File: `src/layers/repositorylayer/python/repositories/base_repository.py`
  - Chức năng: Cung cấp các phương thức cơ bản để tương tác với DynamoDB

- **UserRepository**: Repository xử lý nghiệp vụ liên quan đến User
  - File: `src/layers/repositorylayer/python/repositories/user_repository.py`
  - Chức năng: Cung cấp các phương thức truy vấn và cập nhật dữ liệu User trong DynamoDB

### 2.5. Service
- **AuthService**: Service xử lý nghiệp vụ xác thực
  - File: `src/layers/serviceLayer/python/services/auth_service.py`
  - Chức năng: Xử lý business logic cho việc xác thực, tạo JWT token

### 2.6. Lambda Handler
- **login.py**: Lambda handler cho API đăng nhập
  - File: `src/functions/auth/login.py`
  - Chức năng: Xử lý request đăng nhập, validate input, gọi service, trả về response

### 2.7. Cấu hình
- **template.yaml**: Cấu hình SAM/CloudFormation
  - Chức năng: Định nghĩa resources AWS, thêm Lambda function, API Gateway và DynamoDB table

---

## 3. Cách sử dụng API

### 3.1. Endpoint

```
POST /api/v1/auth/login
```

### 3.2. Request

```json
{
  "username": "admin",
  "password": "your_password",
  "remember_me": false
}
```

### 3.3. Response thành công (200 OK)

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "user-id",
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "Administrator",
      "role": "Admin",
      "permissions": ["permission1", "permission2", "..."]
    }
  }
}
```

### 3.4. Response lỗi (401 Unauthorized)

```json
{
  "status": "error",
  "code": "E1005",
  "message": "Sai tên đăng nhập hoặc mật khẩu"
}
```

---

## 4. Testing

Đã chuẩn bị cấu trúc cho việc testing, các test sẽ được triển khai trong các phiên bản tiếp theo:

- Unit tests cho password_utils
- Unit tests cho jwt_utils
- Unit tests cho UserRepository
- Unit tests cho AuthService
- Integration tests cho Lambda handler

---

## 5. Tài liệu tham khảo

1. API Design: `Design/DD/API/API-AUTH-001.md`
2. Database Structure: `Design/BD/DB/dynamodb_structure.json`
3. AWS Lambda Powertools: https://awslabs.github.io/aws-lambda-powertools-python/
4. PyJWT Documentation: https://pyjwt.readthedocs.io/
5. AWS Serverless Application Model (SAM): https://docs.aws.amazon.com/serverless-application-model/

---

## 6. Các lưu ý tổng hợp

1. JWT Secret nên được lưu trong AWS Secrets Manager hoặc AWS Parameter Store trong môi trường production.
2. Password được lưu trữ ở dạng hash với salt ngẫu nhiên, không lưu plaintext.
3. Kiểm tra và cập nhật last_login_at mỗi lần đăng nhập thành công.
4. Kiểm tra trạng thái tài khoản (is_active) trước khi xác thực. 