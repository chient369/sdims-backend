# API Details: Lấy chi tiết người dùng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
API này cung cấp thông tin chi tiết về một người dùng cụ thể trong hệ thống, bao gồm thông tin cá nhân, phân quyền, lịch sử đăng nhập và các thông tin liên quan, giúp quản trị viên kiểm tra và quản lý người dùng một cách hiệu quả.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-ADM-003                                  |
| **Tên API**        | Lấy chi tiết người dùng                      |
| **Mô tả**          | API cung cấp thông tin chi tiết của một người dùng cụ thể |
| **Module**         | Quản trị Hệ thống (Admin)                   |
| **Phương thức**    | `GET`                                        |
| **Endpoint**       | `/api/v1/admin/users/{userId}`               |
| **Quyền truy cập** | user:read                                    |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên        | Kiểu dữ liệu | Bắt buộc | Mô tả |
|------------|--------------|----------|-------|
| `userId`   | Integer      | Có       | ID của người dùng cần xem thông tin |

### 3.3 Validate Rule
| Trường     | Điều kiện hợp lệ |
|------------|------------------|
| `userId`   | Số nguyên dương  |

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin chi tiết người dùng |

#### User Object (data)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng |
| `username` | String | Tên đăng nhập của người dùng |
| `email` | String | Địa chỉ email của người dùng |
| `fullname` | String | Họ tên đầy đủ của người dùng |
| `employee` | Object/null | Thông tin nhân viên liên kết (null nếu là tài khoản riêng biệt) |
| `role` | Object | Thông tin vai trò và quyền hạn của người dùng |
| `status` | String | Trạng thái tài khoản: "Active", "Inactive", "Locked" |
| `lastLogin` | DateTime | Thời gian đăng nhập gần nhất (ISO 8601) |
| `loginHistory` | Array | Lịch sử các lần đăng nhập gần đây |
| `createdAt` | DateTime | Thời gian tạo tài khoản (ISO 8601) |
| `updatedAt` | DateTime | Thời gian cập nhật gần nhất (ISO 8601) |
| `createdBy` | Object | Thông tin người tạo tài khoản |

#### Employee Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên liên kết |
| `code` | String | Mã nhân viên |
| `name` | String | Tên nhân viên |
| `team` | Object | Thông tin team của nhân viên |
| `position` | String | Vị trí công việc của nhân viên |

#### Team Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của team |
| `name` | String | Tên team |

#### Role Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của vai trò |
| `name` | String | Tên vai trò |
| `permissions` | Array of String | Danh sách các quyền được cấp cho vai trò |

#### Login History Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `timestamp` | DateTime | Thời gian đăng nhập (ISO 8601) |
| `ipAddress` | String | Địa chỉ IP đăng nhập |
| `userAgent` | String | Thông tin trình duyệt/thiết bị đăng nhập |

#### Creator Reference Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người tạo tài khoản |
| `username` | String | Tên đăng nhập của người tạo |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "id": 2,
    "username": "leader1",
    "email": "leader1@company.com",
    "fullname": "Trần Văn B",
    "employee": {
      "id": 5,
      "code": "NV005",
      "name": "Trần Văn B",
      "team": {
        "id": 1,
        "name": "Team Alpha"
      },
      "position": "Leader"
    },
    "role": {
      "id": 2,
      "name": "Leader",
      "permissions": [
        "employee:read",
        "employee:update",
        "project:read",
        "project:update",
        "margin:read",
        "report:read"
      ]
    },
    "status": "Active",
    "lastLogin": "2025-04-30T14:20:15Z",
    "loginHistory": [
      {
        "timestamp": "2025-04-30T14:20:15Z",
        "ipAddress": "192.168.1.25",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0"
      },
      {
        "timestamp": "2025-04-29T09:15:10Z",
        "ipAddress": "192.168.1.25",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0"
      },
      {
        "timestamp": "2025-04-28T08:30:45Z",
        "ipAddress": "192.168.1.25",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0"
      }
    ],
    "createdAt": "2025-01-15T09:30:00Z",
    "updatedAt": "2025-04-30T14:20:15Z",
    "createdBy": {
      "id": 1,
      "username": "admin"
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

#### 403 Forbidden
```json
{
  "status": "error", 
  "code": "E1002",
  "message": "Không có quyền truy cập chức năng này"
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "code": "E3002",
  "message": "Không tìm thấy người dùng với ID: 999"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống khi truy vấn thông tin người dùng"
}
``` 