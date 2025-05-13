# API Details: Đăng nhập

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo tài liệu API đăng nhập | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API cho việc xác thực người dùng và cấp token truy cập hệ thống.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-AUTH-001                                 |
| **Tên API**        | Đăng nhập                                    |
| **Mô tả**          | API xác thực người dùng và trả về token (JWT) |
| **Module**         | Authentication & Authorization               |
| **Phương thức**    | `POST`                                       |
| **Endpoint**       | `/api/v1/auth/login`                         |
| **Quyền truy cập** | Public                                       |

---

## 3. Parameters

### 3.1 Request Body

| Tên            | Kiểu dữ liệu | Bắt buộc | Mô tả |
|----------------|--------------|----------|-------|
| `username`     | String       | Có       | Tên đăng nhập của người dùng |
| `password`     | String       | Có       | Mật khẩu của người dùng |
| `remember_me`  | Boolean      | Không    | Ghi nhớ đăng nhập (mặc định: `false`) |

### 3.2 Validate Rule
| Trường      | Điều kiện hợp lệ |
|-------------|------------------|
| `username`  | Không được rỗng  |
| `password`  | Không được rỗng  |

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin đăng nhập thành công |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `token` | String | JWT token dùng để xác thực các request tiếp theo |
| `token_type` | String | Loại token, giá trị: "Bearer" |
| `expires_in` | Integer | Thời gian hiệu lực của token (giây) |
| `user` | Object | Thông tin người dùng đã đăng nhập |

#### User Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng |
| `username` | String | Tên đăng nhập |
| `email` | String | Địa chỉ email của người dùng |
| `fullname` | String | Họ tên đầy đủ của người dùng |
| `role` | String | Vai trò của người dùng trong hệ thống |
| `permissions` | Array of String | Danh sách các quyền được cấp cho người dùng |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@company.com",
      "fullname": "System Administrator",
      "role": "Admin",
      "permissions": [
        "user:create",
        "user:read",
        "user:update",
        "user:delete",
        "..."
      ]
    }
  }
}
```

### 4.2 Error Responses

#### 401 Unauthorized
```json
{
  "status": "error",
  "code": "E1005",
  "message": "Sai tên đăng nhập hoặc mật khẩu"
}
```

#### 401 Unauthorized (Account Locked)
```json
{
  "status": "error",
  "code": "E1004",
  "message": "Tài khoản bị khóa"
}
```

#### 429 Too Many Requests
```json
{
  "status": "error",
  "code": "E1006",
  "message": "Đăng nhập thất bại quá nhiều lần. Vui lòng thử lại sau 10 phút"
}
```

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2001",
  "message": "Thiếu tham số bắt buộc",
  "errors": [
    {
      "field": "username",
      "message": "Tên đăng nhập không được để trống"
    }
  ]
}
``` 