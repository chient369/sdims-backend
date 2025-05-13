**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-13 | Chiến Trần Văn | Định nghĩa chi tiết task triển khai Lambda function làm mới token | -           | Draft     |

---

## 1. Mục tiêu  
Định nghĩa chi tiết yêu cầu và các nhiệm vụ để triển khai Lambda function làm mới access token sử dụng refresh token, nhằm duy trì phiên đăng nhập của người dùng mà không yêu cầu đăng nhập lại.

# Định nghĩa Chi tiết Task Backend

## Thông tin chung

**Task ID:** BE-AUTH-004  
**Task Name:** Phát triển Lambda function làm mới token  
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
- API-AUTH-004: POST /api/v1/auth/refresh-token

## Mô tả

Task này tập trung vào việc triển khai Lambda function làm mới access token bằng cách sử dụng refresh token, bao gồm:
- Xác thực refresh token gửi lên từ người dùng
- Kiểm tra tính hợp lệ và thời hạn của refresh token
- Tạo access token mới (và tùy chọn refresh token mới)
- Vô hiệu hóa refresh token cũ (nếu cần, tùy theo cơ chế token rotation)
- Xử lý các trường hợp lỗi phù hợp

Kết quả đầu ra là một hàm Lambda được triển khai và tích hợp với API Gateway, có khả năng cung cấp access token mới cho người dùng khi access token cũ hết hạn mà không yêu cầu người dùng đăng nhập lại, miễn là refresh token vẫn còn hiệu lực.

## Chi tiết công việc

### Triển khai Lambda function refresh-token

- [ ] Tạo Lambda function cho endpoint làm mới token:
  - Location: src/auth/refresh_token.py
  - Định nghĩa handler function với cấu trúc chuẩn của AWS Lambda
  - Thiết lập input validation cho request body (refresh_token)
  - Thiết lập cơ chế xử lý lỗi và response format

### Xây dựng logic xác thực và làm mới token

- [ ] Triển khai logic xác thực refresh token:
  - Location: src/auth/refresh_token.py và src/common/auth.py
  - Xác minh chữ ký và giải mã refresh token
  - Kiểm tra thời hạn của refresh token
  - Kiểm tra refresh token có nằm trong danh sách blacklist không
  - Trích xuất thông tin người dùng từ refresh token

- [ ] Triển khai logic tạo token mới:
  - Location: src/auth/refresh_token.py và src/common/auth.py
  - Tạo access token mới với thời hạn ngắn (thông thường 1 giờ)
  - (Tùy chọn) Tạo refresh token mới (token rotation)
  - (Tùy chọn) Thêm refresh token cũ vào blacklist nếu áp dụng token rotation

### Xây dựng cơ chế token rotation (nếu cần)

- [ ] Triển khai cơ chế token rotation:
  - Location: src/auth/refresh_token.py và src/common/auth.py
  - Thiết kế chiến lược xoay vòng refresh token
  - Thêm refresh token cũ vào blacklist khi phát hành refresh token mới
  - Cung cấp cả access token mới và refresh token mới trong response

### Xử lý lỗi và response

- [ ] Triển khai xử lý các trường hợp lỗi:
  - Location: src/auth/refresh_token.py
  - Xử lý lỗi refresh token không hợp lệ
  - Xử lý lỗi refresh token đã hết hạn
  - Xử lý lỗi refresh token đã bị blacklist
  - Xử lý các lỗi khác trong quá trình xác thực và tạo token
  - Định dạng response theo chuẩn hệ thống

### Phát triển Unit Tests

- [ ] Phát triển unit tests cho function refresh-token:
  - Location: tests/unit/auth/test_refresh_token.py
  - Test làm mới token thành công
  - Test với refresh token không hợp lệ
  - Test với refresh token đã hết hạn
  - Test với refresh token đã bị blacklist
  - Test token rotation (nếu áp dụng)
  - Mocking DynamoDB cho việc testing

### Tạo Documentation

- [ ] Tài liệu API specification:
  - Cập nhật Swagger/OpenAPI documentation cho endpoint refresh-token
  - Mô tả request/response format
  - Liệt kê các mã lỗi có thể xảy ra

- [ ] Tài liệu technical implementation:
  - Mô tả chi tiết về cách xác thực refresh token
  - Mô tả chiến lược token rotation (nếu áp dụng)
  - Hướng dẫn cách frontend sử dụng API refresh token

## Ví dụ cách sử dụng cuối cùng

Request:
```json
// POST /api/v1/auth/refresh-token
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Response thành công (không áp dụng token rotation):
```json
{
  "status": "success",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 3600
  }
}
```

Response thành công (có áp dụng token rotation):
```json
{
  "status": "success",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 3600,
    "refreshExpiresIn": 604800
  }
}
```

Response lỗi:
```json
{
  "status": "error",
  "code": "E1000",
  "message": "Refresh token không hợp lệ hoặc đã hết hạn"
}
```

## Tiêu chí hoàn thành

1. Lambda function refresh-token hoạt động chính xác và được triển khai thành công
2. Refresh token được xác thực đúng cách
3. Access token mới được tạo và trả về đúng format
4. Token rotation được triển khai hiệu quả (nếu áp dụng)
5. Tất cả các trường hợp lỗi được xử lý phù hợp theo chuẩn API errors
6. Unit tests đạt coverage > 80%
7. Documentation đầy đủ (Swagger/OpenAPI và technical implementation)

## Ước tính thời gian

- 1-2 ngày làm việc

## Ghi chú

- Cần quyết định rõ về chiến lược token rotation: luôn tạo refresh token mới hay giữ nguyên refresh token cũ
- Nếu áp dụng token rotation, cần thiết kế cơ chế blacklist refresh token hiệu quả
- Thời gian sống của refresh token thường dài hơn access token nhiều lần (ví dụ: access token 1 giờ, refresh token 7 ngày)
- Refresh token cần được bảo vệ kỹ lưỡng hơn access token vì nó có thời gian sống dài hơn
- Frontend cần được hướng dẫn rõ về cách xử lý token hết hạn và khi nào cần gọi API refresh-token
- Có thể cân nhắc cơ chế "sliding expiration" cho refresh token (gia hạn thời gian mỗi khi sử dụng)
- Đảm bảo payload của access token chứa đủ thông tin cần thiết nhưng không quá lớn 