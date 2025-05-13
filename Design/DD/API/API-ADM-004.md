# API Details: Cập nhật thông tin người dùng

**Version Control:**

| Version | Date       | Author         | Changes                        | Approved By | Status    |
| :--- | :--- | :---- | :----- | :---- | :----- |
| 1.0     | 2025-05-01 | Chiến Trần Văn | Tạo mới | -           | Draft     |

---

## 1. Mục tiêu  
API này cho phép quản trị viên cập nhật thông tin của người dùng trong hệ thống, bao gồm cập nhật thông tin cá nhân, trạng thái tài khoản, quyền truy cập và khôi phục mật khẩu, giúp quản lý tài khoản người dùng một cách hiệu quả.

---

## 2. Overview

| Thuộc tính         | Giá trị                                      |
|--------------------|----------------------------------------------|
| **API Code**       | API-ADM-004                                  |
| **Tên API**        | Cập nhật thông tin người dùng                |
| **Mô tả**          | API cập nhật thông tin của người dùng trong hệ thống, bao gồm khóa/mở tài khoản, phân quyền |
| **Module**         | Quản trị Hệ thống (Admin)                   |
| **Phương thức**    | `PUT`                                        |
| **Endpoint**       | `/api/v1/admin/users/{userId}`               |
| **Quyền truy cập** | user:update                                  |

---

## 3. Parameters

### 3.1 Header Parameters

| Tên             | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----------------|--------------|----------|-------|
| `Authorization` | String       | Có       | Định dạng: `Bearer {token}` |
| `Content-Type`  | String       | Có       | Phải là `application/json` |

### 3.2 Path Parameters

| Tên        | Kiểu dữ liệu | Bắt buộc | Mô tả |
|------------|--------------|----------|-------|
| `userId`   | Integer      | Có       | ID của người dùng cần cập nhật |

### 3.3 Request Body

| Tên            | Kiểu dữ liệu         | Bắt buộc | Mô tả |
|----------------|----------------------|----------|-------|
| `email`        | String               | Không    | Email mới của người dùng |
| `fullname`     | String               | Không    | Họ và tên đầy đủ mới của người dùng |
| `roleId`       | Integer              | Không    | ID vai trò mới được gán cho người dùng |
| `employeeId`   | Integer              | Không    | ID của nhân viên liên kết mới (nếu có) |
| `status`       | String               | Không    | Trạng thái mới: `Active`, `Inactive`, `Locked` |
| `resetPassword`| Boolean              | Không    | Đặt lại mật khẩu về giá trị mặc định và bắt đổi lần đầu (mặc định: `false`) |

### 3.4 Validate Rule
| Trường         | Điều kiện hợp lệ |
|----------------|------------------|
| `userId`       | Số nguyên dương, phải tồn tại trong hệ thống |
| `email`        | Định dạng email hợp lệ, phải duy nhất trong hệ thống |
| `fullname`     | Độ dài 1-100 ký tự |
| `roleId`       | Phải tồn tại trong hệ thống |
| `employeeId`   | Phải tồn tại trong hệ thống, chưa liên kết với người dùng khác |
| `status`       | Một trong: `Active`, `Inactive`, `Locked` |
---

## 4. Response

### 4.1 Success - 200 OK

#### Response Structure

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `status` | String | Trạng thái của request, giá trị: "success" |
| `code` | Integer | Mã HTTP status code: 200 |
| `data` | Object | Đối tượng chứa thông tin chi tiết người dùng sau khi cập nhật |

#### User Object (data)

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người dùng |
| `username` | String | Tên đăng nhập của người dùng (không thay đổi) |
| `email` | String | Địa chỉ email đã cập nhật của người dùng |
| `fullname` | String | Họ tên đầy đủ đã cập nhật của người dùng |
| `employee` | Object/null | Thông tin nhân viên liên kết (null nếu không liên kết) |
| `role` | Object | Thông tin vai trò của người dùng (đã cập nhật) |
| `status` | String | Trạng thái tài khoản: "Active", "Inactive", "Locked" |
| `lastLogin` | DateTime | Thời gian đăng nhập gần nhất (ISO 8601) |
| `resetPassword` | Boolean | Trạng thái đặt lại mật khẩu (true nếu yêu cầu đặt lại) |
| `createdAt` | DateTime | Thời gian tạo tài khoản (ISO 8601) |
| `updatedAt` | DateTime | Thời gian cập nhật gần nhất (ISO 8601) |
| `updatedBy` | Object | Thông tin người cập nhật tài khoản |

#### Employee Reference Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của nhân viên liên kết |
| `code` | String | Mã nhân viên |

#### Role Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của vai trò |
| `name` | String | Tên vai trò |

#### Updater Reference Object

| Trường | Kiểu dữ liệu | Mô tả |
|--------|--------------|-------|
| `id` | Integer | ID của người cập nhật |
| `username` | String | Tên đăng nhập của người cập nhật |

#### Ví dụ:

```json
{
  "status": "success",
  "code": 200,
  "data": {
    "id": 3,
    "username": "user1",
    "email": "user1.updated@company.com",
    "fullname": "Nguyễn Văn A Updated",
    "employee": {
      "id": 1,
      "code": "NV001"
    },
    "role": {
      "id": 4,
      "name": "Manager"
    },
    "status": "Active",
    "lastLogin": "2025-04-15T10:20:30Z",
    "resetPassword": true,
    "createdAt": "2025-01-20T14:15:00Z",
    "updatedAt": "2025-05-01T11:30:45Z",
    "updatedBy": {
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
  "code": "E2000",
  "message": "Dữ liệu đầu vào không hợp lệ",
  "errors": [
    {
      "field": "email",
      "message": "Email đã tồn tại trong hệ thống"
    },
    {
      "field": "status",
      "message": "Giá trị 'Deactivated' không hợp lệ. Các giá trị cho phép: Active, Inactive, Locked"
    }
  ]
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
  "message": "Lỗi hệ thống khi cập nhật thông tin người dùng"
}
``` 