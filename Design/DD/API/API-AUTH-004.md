# API-AUTH-004: Refresh Token

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2024-05-03 | Chiến Trần Văn | Tạo tài liệu chi tiết API refresh token | -           | Draft     |

---

## 1. Mục tiêu  
Cho phép client làm mới access token của người dùng khi token hết hạn mà không yêu cầu người dùng đăng nhập lại, bằng cách sử dụng refresh token.

## 2. Endpoint

- **URL**: `/api/v1/auth/refresh-token`
- **Method**: `POST`
- **Auth required**: No (Sử dụng refresh token trong request)

## 3. Request Parameters

### 3.1. Header Parameters

N/A

### 3.2. Path Parameters

N/A

### 3.3. Query String Parameters

N/A

### 3.4. Request Body

```json
{
  "refresh_token": "string" // Refresh token nhận được khi đăng nhập
}
```

## 4. Response

### 4.1. Success Response (200 OK)

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `data` | Object | Đối tượng chứa thông tin token mới |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `access_token` | String | JWT token mới dùng để xác thực các request tiếp theo |
| `refresh_token` | String | Refresh token mới (nếu áp dụng chiến lược rotation) |
| `token_type` | String | Loại token, giá trị: "Bearer" |
| `expires_in` | Integer | Thời gian hiệu lực của access token mới (giây) |

#### Ví dụ:

```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJpYXQiOjE2MTc3NzU2NjQsImV4cCI6MTYxNzc3OTI2NH0.ABC",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJpYXQiOjE2MTc3NzU2NjQsImV4cCI6MTYxODM4MDQ2NH0.DEF",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

### 4.2. Error Responses

#### 4.2.1. Invalid token (401 Unauthorized)

```json
{
  "status": "error",
  "code": "AUTH004001",
  "message": "Refresh token không hợp lệ hoặc đã hết hạn"
}
```

#### 4.2.2. Token blacklisted (401 Unauthorized)

```json
{
  "status": "error",
  "code": "AUTH004002",
  "message": "Refresh token đã bị vô hiệu hóa"
}
```

#### 4.2.3. Server Error (500 Internal Server Error)

```json
{
  "status": "error",
  "code": "AUTH004003",
  "message": "Lỗi server khi xử lý refresh token"
}
```

## 5. Ví dụ

### 5.1. Request Example

```http
POST /api/v1/auth/refresh-token HTTP/1.1
Host: api.sdims.com
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJpYXQiOjE2MTc3NzU2NjQsImV4cCI6MTYxNzg2MjA2NH0.XYZ"
}
```

### 5.2. Response Example

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJpYXQiOjE2MTc3NzU2NjQsImV4cCI6MTYxNzc3OTI2NH0.ABC",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJpYXQiOjE2MTc3NzU2NjQsImV4cCI6MTYxODM4MDQ2NH0.DEF",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

## 6. Notes

1. Refresh token có thời gian sống dài hơn access token, giúp giảm số lần người dùng phải đăng nhập lại.
2. Mỗi lần refresh token được sử dụng, tùy theo chiến lược, hệ thống có thể:
   - Tiếp tục sử dụng refresh token cũ
   - Tạo refresh token mới và vô hiệu hóa token cũ (kỹ thuật rotation)
3. Nên lưu trữ danh sách refresh token đã bị vô hiệu hóa (blacklist) để ngăn chặn việc tái sử dụng.
4. Nên cấu hình thời gian sống của access token và refresh token phù hợp với yêu cầu bảo mật của ứng dụng.