**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function lấy thông tin người dùng hiện tại | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function lấy thông tin người dùng đã đăng nhập và quyền truy cập của họ.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-AUTH-003  
**Task Name:** Triển khai Lambda function lấy thông tin người dùng hiện tại  
**Độ ưu tiên:** Cao  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Service authentication và authorization)
- BE-AUTH-001 (Triển khai Lambda function đăng nhập)

**Các task phụ thuộc vào task này:** Không có (nhưng nhiều task khác sẽ sử dụng thông tin người dùng)

**Các API:**
- API-AUTH-003: GET /api/v1/auth/me

## Mô tả

Task này tập trung vào việc triển khai Lambda function lấy thông tin chi tiết của người dùng đã đăng nhập, bao gồm:
- Xác thực JWT token hiện tại của người dùng
- Lấy thông tin chi tiết người dùng từ DynamoDB
- Lấy thông tin vai trò và quyền truy cập của người dùng
- Định dạng dữ liệu trả về theo chuẩn API
- Xử lý các trường hợp lỗi phù hợp

Kết quả đầu ra là một hàm Lambda được triển khai và tích hợp với API Gateway, có khả năng trả về thông tin chi tiết về người dùng đã đăng nhập. Thông tin này sẽ được sử dụng bởi frontend để hiển thị và kiểm soát quyền truy cập.

## Chi tiết công việc

### Triển khai Lambda function me

- [ ] Tạo Lambda function cho endpoint lấy thông tin người dùng:
  - Location: src/auth/me.py
  - Định nghĩa handler function với cấu trúc chuẩn của AWS Lambda
  - Tích hợp với Lambda Authorizer để xác thực token và lấy thông tin user_id từ token
  - Thiết lập cơ chế xử lý lỗi và response format

### Xây dựng logic lấy thông tin người dùng

- [ ] Triển khai logic truy vấn thông tin người dùng từ DynamoDB:
  - Location: src/auth/me.py và src/common/auth.py
  - Sử dụng user_id từ token để truy vấn thông tin chi tiết người dùng từ DynamoDB
  - Lấy các thuộc tính cần thiết của người dùng (id, username, email, full_name, is_active, last_login_at, ...)
  - Triển khai cơ chế cache (nếu cần) để tối ưu hiệu suất

### Xây dựng logic lấy thông tin vai trò và quyền

- [ ] Triển khai logic truy vấn thông tin vai trò và quyền:
  - Location: src/auth/me.py và src/common/auth.py
  - Dựa trên role_id của người dùng, truy vấn thông tin vai trò từ DynamoDB
  - Lấy danh sách permissions được gán cho vai trò
  - Đảm bảo hiệu suất tốt bằng cách áp dụng cơ chế truy vấn tối ưu thông qua Global Secondary Index

### Định dạng dữ liệu trả về

- [ ] Triển khai chuẩn định dạng dữ liệu trả về:
  - Location: src/auth/me.py
  - Tạo response object với đầy đủ thông tin người dùng
  - Đảm bảo không trả về thông tin nhạy cảm (như password_hash)
  - Chuẩn hóa dữ liệu permissions để frontend dễ dàng sử dụng

### Xử lý lỗi và response

- [ ] Triển khai xử lý các trường hợp lỗi:
  - Location: src/auth/me.py
  - Xử lý lỗi token không hợp lệ hoặc đã hết hạn
  - Xử lý lỗi người dùng chưa đăng nhập
  - Xử lý lỗi không tìm thấy thông tin người dùng
  - Xử lý lỗi tài khoản bị khóa
  - Định dạng response theo chuẩn hệ thống

### Phát triển Unit Tests

- [ ] Phát triển unit tests cho function me:
  - Location: tests/unit/auth/test_me.py
  - Test lấy thông tin người dùng thành công
  - Test với token không hợp lệ
  - Test trường hợp không tìm thấy người dùng
  - Test trường hợp tài khoản bị khóa
  - Mocking DynamoDB cho việc testing

### Tạo Documentation

- [ ] Tài liệu API specification:
  - Cập nhật Swagger/OpenAPI documentation cho endpoint me
  - Mô tả response format chi tiết
  - Liệt kê các mã lỗi có thể xảy ra

- [ ] Tài liệu technical implementation:
  - Mô tả cách lấy và định dạng dữ liệu người dùng
  - Mô tả cách lấy và định dạng dữ liệu vai trò và quyền
  - Mô tả cách frontend sử dụng thông tin quyền truy cập

## Ví dụ cách sử dụng cuối cùng

Request:
```
// GET /api/v1/auth/me
// Headers:
// Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Response thành công:
```json
{
  "status": "success",
  "data": {
    "user": {
      "id": "123",
      "username": "user@example.com",
      "email": "user@example.com",
      "fullName": "Nguyễn Văn A",
      "isActive": true,
      "lastLoginAt": "2025-05-13T08:30:45Z",
      "role": {
        "id": "role-1",
        "name": "Admin"
      },
      "permissions": [
        "user:read",
        "user:write",
        "employee:read",
        "employee:write",
        "contract:read"
      ]
    }
  }
}
```

Response lỗi:
```json
{
  "status": "error",
  "code": "E1000",
  "message": "Token không hợp lệ hoặc đã hết hạn"
}
```

## Tiêu chí hoàn thành

1. Lambda function me hoạt động chính xác và được triển khai thành công
2. Thông tin người dùng được truy vấn đầy đủ từ DynamoDB
3. Thông tin vai trò và quyền được truy vấn và định dạng chính xác
4. Tất cả các trường hợp lỗi được xử lý phù hợp theo chuẩn API errors
5. Không có thông tin nhạy cảm được trả về trong response
6. Unit tests đạt coverage > 80%
7. Documentation đầy đủ (Swagger/OpenAPI và technical implementation)

## Ước tính thời gian

- 1-2 ngày làm việc

## Ghi chú

- API này rất quan trọng vì nó được sử dụng bởi hầu hết các chức năng khác để kiểm tra quyền truy cập
- Cần đảm bảo hiệu suất cao, có thể xem xét việc sử dụng cache
- Quyền truy cập (permissions) nên được định dạng theo chuẩn resource:action[:scope]
- Không trả về quá nhiều thông tin không cần thiết để tránh tăng kích thước response
- Cần đảm bảo bảo mật và không để lộ thông tin nhạy cảm
- Cung cấp đầy đủ thông tin (đặc biệt là permissions) cho frontend để xây dựng UI phù hợp với quyền của người dùng 