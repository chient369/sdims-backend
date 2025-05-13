# API Details: Lấy thông tin người dùng hiện tại

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo tài liệu API lấy thông tin người dùng | -           | Draft     |

---

## 1. Mục tiêu  
Cung cấp API để lấy thông tin và quyền của người dùng hiện tại đã đăng nhập.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-AUTH-003                                 |
| **Tên API**        | Lấy thông tin người dùng hiện tại           |
| **Mô tả**          | API lấy thông tin và quyền của người dùng đã đăng nhập |
| **Module**         | Authentication & Authorization               |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/auth/me`                           |
| **Quyền truy cập** | auth:read:own                                |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin chi tiết của người dùng |

#### Data Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `user` | Object | Thông tin chi tiết người dùng |
| `permissions` | Array of String | Danh sách các quyền được cấp cho người dùng |
| `settings` | Object | Cài đặt cá nhân của người dùng |

#### User Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng |
| `username` | String | Tên đăng nhập |
| `email` | String | Địa chỉ email của người dùng |
| `fullname` | String | Họ tên đầy đủ của người dùng |
| `avatar` | String | URL ảnh đại diện của người dùng |
| `role` | String | Vai trò của người dùng trong hệ thống |
| `employee_id` | Integer | ID liên kết đến hồ sơ nhân viên (nếu có) |
| `created_at` | DateTime | Thời điểm tạo tài khoản (ISO 8601) |
| `last_login` | DateTime | Thời điểm đăng nhập gần nhất (ISO 8601) |

#### Settings Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `notification_enabled` | Boolean | Trạng thái bật/tắt thông báo |
| `theme` | String | Chủ đề giao diện người dùng (light, dark) |
| `language` | String | Ngôn ngữ hiển thị (vi, en, ja) |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@company.com",
      "fullname": "System Administrator",
      "avatar": "https://example.com/avatars/admin.jpg",
      "role": "Admin",
      "employee_id": 101,
      "created_at": "2025-01-01T08:00:00Z",
      "last_login": "2025-05-01T09:30:00Z"
    },
    "permissions": [
      "user:create",
      "user:read",
      "user:update",
      "user:delete",
      "employee:read",
      "employee:create",
      "employee:update",
      "employee:delete",
      "opportunity:read",
      "opportunity:create",
      "opportunity:update",
      "opportunity:delete",
      "contract:read",
      "contract:create",
      "contract:update",
      "contract:delete",
      "..."
    ],
    "settings": {
      "notification_enabled": true,
      "theme": "light",
      "language": "vi"
    }
  }
}
```

### 4.2 Error Responses

#### 401 Unauthorized
```json
{
  "status": "error",
  "code": "E1000",
  "message": "Token không hợp lệ hoặc đã hết hạn"
}
```

#### 401 Unauthorized
```json
{
  "status": "error",
  "code": "E1001",
  "message": "Chưa đăng nhập"
}
``` 