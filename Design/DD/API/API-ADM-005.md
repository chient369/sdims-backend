# API Details: Xóa người dùng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép quản trị viên xóa tài khoản người dùng khỏi hệ thống (soft delete), đảm bảo việc quản lý người dùng hiệu quả và an toàn. Việc xóa sẽ không mất dữ liệu vĩnh viễn mà chỉ đánh dấu người dùng đã bị xóa, đảm bảo tính toàn vẹn của hệ thống.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-ADM-005                                  |
| **Tên API**        | Xóa người dùng                               |
| **Mô tả**          | API xóa (soft delete) người dùng khỏi hệ thống |
| **Module**         | Quản trị Hệ thống (Admin)                   |
| **Phương thức**    | `DELETE`                                     |
| **Endpoint**       | `/api/v1/admin/users/{userId}`               |
| **Quyền truy cập** | user:delete                                  |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |

### 3.2 Path Parameters

| Tên        | Kiểu dữ liệu | Bắt buộc | Mô tả |
|------------|--------------|----------|-------|
| `userId`   | Integer      | Có       | ID của người dùng cần xóa |

### 3.3 Validate Rule
| Trường     | Điều kiện hợp lệ |
|------------|------------------|
| `userId`   | Số nguyên dương, phải tồn tại trong hệ thống, không phải là tài khoản đang đăng nhập |

---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin về kết quả xóa người dùng |

#### Delete Result Object (data)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng đã xóa |
| `username` | String | Tên đăng nhập của người dùng đã xóa |
| `message` | String | Thông báo kết quả thao tác |
| `deletedAt` | DateTime | Thời gian xóa (ISO 8601) |
| `deletedBy` | Object | Thông tin người thực hiện xóa |

#### Deleter Reference Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người thực hiện xóa |
| `username` | String | Tên đăng nhập của người thực hiện xóa |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "id": 3,
    "username": "user1",
    "message": "Người dùng đã được xóa thành công",
    "deletedAt": "2025-05-01T13:15:20Z",
    "deletedBy": {
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

#### 400 Bad Request
```json
{
  "status": "error",
  "code": "E2003",
  "message": "Không thể xóa tài khoản đang đăng nhập"
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

#### 409 Conflict
```json
{
  "status": "error",
  "code": "E4001",
  "message": "Không thể xóa người dùng này vì đang có liên kết với dữ liệu khác trong hệ thống"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "E6000",
  "message": "Lỗi hệ thống khi xóa người dùng"
}
``` 