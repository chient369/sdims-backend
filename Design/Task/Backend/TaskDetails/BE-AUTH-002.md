**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function đăng xuất | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function xử lý đăng xuất và vô hiệu hóa token của người dùng.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-AUTH-002  
**Task Name:** Phát triển Lambda function đăng xuất  
**Độ ưu tiên:** Trung bình  
**Phụ thuộc vào:** 
- BE-INF-001 (Thiết lập cấu trúc dự án SAM)
- BE-INF-003 (Định nghĩa IAM Roles và Policies)
- BE-INF-004 (Triển khai DynamoDB table)
- BE-INF-005 (Cấu hình API Gateway)
- BE-CORE-001 (Xây dựng lớp truy xuất DynamoDB)
- BE-CORE-002 (Service authentication và authorization)
- BE-AUTH-001 (Triển khai Lambda function đăng nhập)

**Các task phụ thuộc vào task này:** Không có

**Các API:**
- API-AUTH-002: POST /api/v1/auth/logout

## Mô tả

Task này tập trung vào việc triển khai Lambda function xử lý quá trình đăng xuất của người dùng, bao gồm:
- Nhận và xác thực JWT token hiện tại của người dùng
- Vô hiệu hóa (blacklist) token để ngăn sử dụng lại
- Xóa thông tin phiên đăng nhập hiện tại (nếu có)
- Xử lý các trường hợp lỗi phù hợp

Kết quả đầu ra là một hàm Lambda được triển khai và tích hợp với API Gateway, có khả năng xử lý đăng xuất người dùng một cách an toàn, vô hiệu hóa token để đảm bảo người dùng không thể tiếp tục sử dụng token đã đăng xuất.

## Chi tiết công việc

### Triển khai Lambda function logout

- [ ] Tạo Lambda function cho endpoint đăng xuất:
  - Location: src/auth/logout.py
  - Định nghĩa handler function với cấu trúc chuẩn của AWS Lambda
  - Tích hợp với Lambda Authorizer để xác thực token trước khi xử lý đăng xuất
  - Thiết lập cơ chế xử lý lỗi và response format

### Xây dựng cơ chế blacklist token

- [ ] Triển khai cơ chế blacklist token:
  - Location: src/auth/logout.py và src/common/auth.py
  - Thiết kế và triển khai giải pháp lưu trữ token đã vô hiệu hóa (DynamoDB hoặc Redis)
  - Tạo entity BLACKLISTED_TOKEN trong DynamoDB (hoặc sử dụng dịch vụ khác như Redis nếu phù hợp)
  - Cài đặt logic để thêm token vào danh sách blacklist với thời gian hết hạn
  - Đảm bảo hiệu suất cao khi kiểm tra token trong danh sách blacklist

### Tích hợp với Lambda Authorizer

- [ ] Cập nhật Lambda Authorizer để kiểm tra token blacklist:
  - Location: src/auth/authorizer.py
  - Bổ sung logic kiểm tra token có nằm trong danh sách blacklist hay không
  - Đảm bảo các token đã đăng xuất không thể tiếp tục sử dụng

### Xử lý lỗi và response

- [ ] Triển khai xử lý các trường hợp lỗi:
  - Location: src/auth/logout.py
  - Xử lý lỗi token không hợp lệ hoặc đã hết hạn
  - Xử lý lỗi người dùng chưa đăng nhập
  - Định dạng response theo chuẩn hệ thống

### Phát triển Unit Tests

- [ ] Phát triển unit tests cho function logout:
  - Location: tests/unit/auth/test_logout.py
  - Test đăng xuất thành công
  - Test đăng xuất với token không hợp lệ
  - Test đăng xuất khi chưa đăng nhập
  - Mocking DynamoDB/Redis cho việc testing blacklist

### Tạo Documentation

- [ ] Tài liệu API specification:
  - Cập nhật Swagger/OpenAPI documentation cho endpoint logout
  - Mô tả request/response format
  - Liệt kê các mã lỗi có thể xảy ra

- [ ] Tài liệu technical implementation:
  - Mô tả chi tiết về cách token được blacklist
  - Mô tả cơ chế kiểm tra token trong blacklist
  - Giải thích chiến lược quản lý và xóa token hết hạn khỏi blacklist

## Ví dụ cách sử dụng cuối cùng

Request:
```
// POST /api/v1/auth/logout
// Headers:
// Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Response thành công:
```json
{
  "status": "success",
  "message": "Đăng xuất thành công"
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

1. Lambda function logout hoạt động chính xác và được triển khai thành công
2. Token blacklisting được triển khai hiệu quả
3. Lambda Authorizer được cập nhật để kiểm tra token blacklist
4. Tất cả các trường hợp lỗi được xử lý phù hợp theo chuẩn API errors
5. Unit tests đạt coverage > 80%
6. Documentation đầy đủ (Swagger/OpenAPI và technical implementation)
7. Đảm bảo tính an toàn và hiệu suất của hệ thống blacklist

## Ước tính thời gian

- 1-2 ngày làm việc

## Ghi chú

- Cần cân nhắc giữa việc sử dụng DynamoDB hoặc Redis cho blacklist token, dựa trên yêu cầu hiệu suất và khả năng mở rộng
- Token blacklist cần có cơ chế tự động xóa khi token hết hạn để tránh tăng kích thước database không cần thiết
- Nếu sử dụng DynamoDB, cần thiết kế cấu trúc dữ liệu tối ưu cho việc kiểm tra nhanh token
- Nếu hệ thống có khả năng mở rộng lớn, cần đánh giá giải pháp blacklist phân tán
- Có thể cân nhắc sử dụng JWT với thời gian sống ngắn và quản lý refresh token để giảm rủi ro bảo mật 